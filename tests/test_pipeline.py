import io
from pathlib import Path
from unittest.mock import Mock
import pytest
import requests
from PIL import Image
import build_support as support
import inline_content as inline
from html_source import fit_image_scale, parse_html
from scrape_chapters import arguments, module_name, rendered_text, select_chapters
from validate_against_pdf import coverage, map_pdf, reference_lines, validate_ranges, norm


def response(status=200, content=b'good', headers=None):
    r = Mock(status_code=status, content=content, headers=headers or {})
    if status >= 400: r.raise_for_status.side_effect = requests.HTTPError(str(status))
    return r


def test_cache_validated_atomic_and_offline(tmp_path):
    session = Mock(); session.get.return_value = response()
    path = support.cache_path(tmp_path, 'https://a/ch1', 'pages')
    validate = lambda data: None if data == b'good' else (_ for _ in ()).throw(ValueError('bad'))
    assert support.cached_fetch(session, 'https://a/ch1', path, validate) == b'good'
    session.get.reset_mock()
    assert support.cached_fetch(session, 'https://a/ch1', path, validate, offline=True) == b'good'
    session.get.assert_not_called()
    path.write_bytes(b'bad')
    with pytest.raises(support.BuildError, match='invalid cached'): support.cached_fetch(session, 'url', path, validate, offline=True)
    assert support.cache_path(tmp_path, 'https://b/ch1', 'pages') != path


def test_retries_and_refresh(tmp_path, monkeypatch):
    sleeps = []; monkeypatch.setattr(support.time, 'sleep', sleeps.append)
    session = Mock(); session.get.side_effect = [response(429, headers={'Retry-After':'3'}), requests.Timeout(), response()]
    path = tmp_path/'page'; path.write_bytes(b'old')
    assert support.cached_fetch(session, 'url', path, lambda d: None, refresh=True) == b'good'
    assert sleeps == [3, 2]
    assert session.get.call_count == 3


@pytest.mark.parametrize('status', [401,403,404,500])
def test_failed_download_does_not_replace_cache(tmp_path, monkeypatch, status):
    monkeypatch.setattr(support.time, 'sleep', lambda _: None)
    session=Mock(); session.get.return_value=response(status)
    path=tmp_path/'page'; path.write_bytes(b'old')
    with pytest.raises(support.BuildError): support.cached_fetch(session,'url',path,lambda _:None,refresh=True)
    assert path.read_bytes() == b'old'
    assert session.get.call_count == (3 if status == 500 else 1)


def test_atomic_write_failure_preserves_old(tmp_path,monkeypatch):
    path=tmp_path/'cache'; path.write_bytes(b'old')
    monkeypatch.setattr(support.os,'replace',Mock(side_effect=OSError('interrupted')))
    with pytest.raises(OSError): support.atomic_write(path,b'new')
    assert path.read_bytes()==b'old'
    assert list(tmp_path.iterdir())==[path]


def test_offline_missing_and_corrupt_image(tmp_path):
    with pytest.raises(support.BuildError,match='offline cache miss'): support.cached_fetch(Mock(),'url',tmp_path/'none',lambda _:None,offline=True)
    with pytest.raises(OSError): support.validate_image(b'html error')
    data=io.BytesIO(); Image.new('RGB',(10,10)).save(data,format='PNG'); support.validate_image(data.getvalue())


@pytest.mark.parametrize('html',['<title>Access denied</title><p>paywall</p>','<h2>Empty</h2>','<input type=password><p>Login</p>'])
def test_blocked_and_empty(html):
    with pytest.raises(ValueError): parse_html(html)


def test_html_order_spacing_tables_and_lists():
    els=parse_html('<article><h2>1. Heading</h2><p><strong>active</strong> and plain<p>Before<img src="https://x/a_lg.jpg">After<ul><li>Parent<ol><li>Nested</ol><li>Last</ul><table><tr><td>CO<sub>2</sub></td></tr></table></article>')
    assert els[0]['text']=='Heading'
    assert els[1]['text']=='active and plain'
    assert [e['type'] for e in els[2:5]]==['body','image','body']
    lists=[e for e in els if e['type']=='list']
    assert [(e['ordered'],e['items'][0][0]) for e in lists]==[(False,0),(True,1),(False,0)]
    assert els[-1]['rows'][0][0][-1]['kind']=='sub'


def test_sparse_legacy_images_use_article_content_and_skip_promotions():
    html = '''<div class="contenttextdiv"><table><tr><td>Clear all your doubts with EduRev</td></tr></table>
    <div class="contenttextdiv"><h2>1. Real topic</h2><p>Substantive notes.</p>
    <img src="https://cn.edurev.in/ApplicationImages/Temp/abc_sp.png"></div></div>'''
    els = parse_html(html)
    assert [e['type'] for e in els] == ['heading', 'body', 'image']
    assert els[-1]['filename'] == 'abc_sp.png'


def test_number_prefixed_content_images_are_kept_but_decorations_are_skipped():
    html = '''<article><h2>Topic</h2><p>Substantive notes.</p>
    <img alt="Thermometer" src="https://cn.edurev.in/ApplicationImages/Temp/1421561_75514512-4eb3-45e9-9b2b-656447055db2_lg.png">
    <img alt="Decoration" src="https://cn.edurev.in/cdn_lib/Vector.png"></article>'''
    images = [element for element in parse_html(html) if element['type'] == 'image']
    assert len(images) == 1
    assert images[0]['filename'].startswith('1421561_')


def test_instructional_gif_is_accepted_for_static_frame_conversion():
    html = '''<article><h2>Nutrition</h2><p>Substantive notes.</p>
    <img alt="Nutrition" src="https://cn.edurev.in/ApplicationImages/Temp/27602a0a-ab1d-4a9b-8222-62c0e350892f_lg.gif"></article>'''
    images = [element for element in parse_html(html) if element['type'] == 'image']
    assert len(images) == 1
    assert images[0]['filename'].endswith('_lg.gif')


def test_promo_table_is_skipped_before_span_validation():
    html = '<article><table class="coursedatatable"><tr><td colspan="2">Science for Class 6 91 videos | 431 docs</td></tr></table><h2>Topic</h2><p>Notes.</p></article>'
    assert [e['type'] for e in parse_html(html)] == ['heading', 'body']


@pytest.mark.parametrize('source,expected', [('CO₂','textsubscript{2}'),('x²','textsuperscript{2}'),('α → β',r'\alpha'),(r'\(\frac{a}{b}\)',r'\frac{a}{b}'),(r'\[\sqrt{x}\]',r'\sqrt{x}'),('Price $5 and 50%','\\$5')])
def test_notation(source,expected):
    runs=inline.text_runs(source)
    assert expected in inline.tex(runs)
    if any(s['kind']=='math' for s in runs): assert '\\begin_inset Formula' in inline.lyx(runs)


def test_mathml_and_annotation():
    html='<p><math><mfrac><mi>a</mi><msqrt><mi>b</mi></msqrt></mfrac></math></p>'
    assert r'\frac{a}{\sqrt{b}}' in inline.tex(parse_html(html)[0]['segments'])
    html='<p><span class="katex"><span>duplicate</span><math><semantics><mi>x</mi><annotation encoding="application/x-tex">x^2</annotation></semantics></math></span></p>'
    runs=parse_html(html)[0]['segments']; assert len(runs)==1 and runs[0]['text']=='x^2'


@pytest.mark.parametrize('formula',[r'\input{secret}',r'\write18{bad}',r'\begin{document}x\end{document}','{x',r'\newcommand{x}{y}'])
def test_unsupported_math(formula):
    with pytest.raises(ValueError): inline.check_math(formula)


def test_unknown_mathml():
    with pytest.raises(ValueError,match='Unsupported MathML'): parse_html('<p><math><maction><mi>x</mi></maction></math></p>')


def test_full_line_coverage_and_boundary():
    prefix='A sufficiently long sentence with a common beginning '
    result=coverage([prefix+'correct ending'],prefix+'wrong ending',1,'tex',{})
    assert result['coverage']==0
    lines=[f'Unique statement number {i} ends here' for i in range(20)]
    assert coverage(lines,' '.join(lines[:19]),1,'tex',{})['coverage']==.95
    assert norm('CO₂  ﬁne')==norm('CO2 fine')
    with pytest.raises(support.ValidationError): coverage([], '',1,'tex',{})


def test_mapping_never_guesses():
    doc=Mock(); doc.get_toc.return_value=[[1,'Other',1]]; doc.__len__=Mock(return_value=10)
    with pytest.raises(support.ValidationError,match='Ambiguous'): map_pdf(doc,[{'num':1,'name':'Missing'}])
    chapters=[{'num':1,'name':'One'},{'num':2,'name':'Two'}]
    ranges=[dict(chapter=1,start_page=1,end_page=2),dict(chapter=2,start_page=3,end_page=5)]
    assert validate_ranges(ranges,chapters,5)==ranges
    ranges[1]['start_page']=2
    with pytest.raises(support.ValidationError): validate_ranges(ranges,chapters,5)


def test_cli_selection_and_module():
    chapters=[dict(num=i) for i in [3,1,2]]
    assert [c['num'] for c in select_chapters(chapters,'1,3')]==[3,1]
    with pytest.raises(ValueError): select_chapters(chapters,'4')
    with pytest.raises(ValueError): select_chapters([dict(num=1),dict(num=1)],None)
    with pytest.raises(ValueError): module_name(arguments(['--module','../bad']))
    with pytest.raises(ValueError): module_name(arguments(['old','--module','new']))
    assert module_name(arguments(['--links','MyNotes.txt']))=='MyNotes'


def test_publication_rollback(tmp_path,monkeypatch):
    old=tmp_path/'module'; old.mkdir(); (old/'good').write_text('old')
    staged=tmp_path/'staged'; staged.mkdir()
    original=Path.rename
    def fail(self,target):
        if self==staged: raise OSError('publication interrupted')
        return original(self,target)
    monkeypatch.setattr(Path,'rename',fail)
    with pytest.raises(OSError): support.publish(staged,old)
    assert (old/'good').read_text()=='old'

def test_compiler_timeout_retains_diagnostics(tmp_path,monkeypatch):
    import subprocess
    monkeypatch.setattr(support.subprocess,'run',Mock(side_effect=subprocess.TimeoutExpired('compiler',1,output=b'partial')))
    with pytest.raises(support.BuildError,match='timed out'): support.command(['compiler'],tmp_path,tmp_path/'compiler.log',timeout=1)
    assert b'partial' in (tmp_path/'compiler.log').read_bytes()


def test_compiler_missing_is_not_skipped(monkeypatch):
    monkeypatch.setattr(support.shutil,'which',lambda _:None)
    with pytest.raises(support.BuildError,match='Missing compiler'): support.executable('nonexistent-compiler')


def test_headless_linux_compiler_environment():
    linux = support.compiler_environment({'PATH': '/usr/bin'}, platform_name='posix')
    assert linux['QT_QPA_PLATFORM'] == 'offscreen'
    assert linux['openin_any'] == linux['openout_any'] == 'p'
    desktop = support.compiler_environment({'DISPLAY': ':0'}, platform_name='posix')
    assert 'QT_QPA_PLATFORM' not in desktop
    explicit = support.compiler_environment({'QT_QPA_PLATFORM': 'minimal'}, platform_name='posix')
    assert explicit['QT_QPA_PLATFORM'] == 'minimal'


def test_unsupported_and_matrix_mathml():
    for markup,expected in [('<mroot><mi>x</mi><mn>3</mn></mroot>',r'\sqrt[3]{x}'),('<msubsup><mi>x</mi><mn>1</mn><mn>2</mn></msubsup>','{x}_{1}^{2}'),('<mfenced><mi>x</mi><mi>y</mi></mfenced>',r'\left(x,y\right)'),('<mover><mi>x</mi><mo>^</mo></mover>',r'\hat{x}')]:
        runs=parse_html('<p><math>'+markup+'</math></p>')[0]['segments']
        assert expected in inline.tex(runs)
    assert norm('a ≤ b') != norm('a ≥ b')
    assert norm(r'a \leq b') == norm('a ≤ b')


def test_mathjax_script_and_literal_escaping():
    elements=parse_html('<p>Equation <script type="math/tex">x^2</script> here.</p>')
    assert r'$x^2$' in inline.tex(elements[0]['segments'])
    assert inline.escape('\\{50%}')==r'\textbackslash{}\{50\%\}'
    assert inline.plain(parse_html('<p>Visible<!-- hidden --> text.</p>')[0]['segments'])=='Visible text.'


def test_docx_fallback_legacy_segments(tmp_path):
    from docx import Document
    import convert
    document=Document(); document.add_paragraph('A plain paragraph with '); document.paragraphs[0].add_run('bold text').bold=True
    source=tmp_path/'source.docx'; document.save(source)
    elements,*_=convert.parse_docx(source)
    media=tmp_path/'media'; media.mkdir()
    convert.write_tex(elements,tmp_path/'fallback.tex',media)
    convert.write_lyx(elements,tmp_path/'fallback.lyx',media)
    assert r'\textbf{bold text}' in (tmp_path/'fallback.tex').read_text()
    assert '\\series bold' in (tmp_path/'fallback.lyx').read_text()
    assert r'\raggedbottom' in (tmp_path/'fallback.tex').read_text()
    assert r'\raggedbottom' in (tmp_path/'fallback.lyx').read_text()


def test_original_chapter_numbers_compact_spacing_and_unicode_rupee(tmp_path):
    import convert
    media = tmp_path/'media'; media.mkdir()
    elements = [dict(type='heading', level='chapter', text='Seven', number=7),
                dict(type='body', text='₹ 7', segments=[dict(kind='text', text='₹ 7')])]
    tex_path = tmp_path/'numbered.tex'; lyx_path = tmp_path/'numbered.lyx'
    convert.write_tex(elements, tex_path, media)
    convert.write_lyx(elements, lyx_path, media)
    tex = tex_path.read_text(encoding='utf-8'); lyx = lyx_path.read_text(encoding='utf-8')
    assert r'\setcounter{chapter}{6}' in tex
    assert r'\newunicodechar{₹}{\rupee}' in tex
    assert r'\titlespacing*{\section}{0pt}{1.25ex' in tex
    assert '\\begin_layout Standard\n\\begin_inset ERT' in lyx
    assert 'setcounter{chapter}{6}' in lyx
    assert r'\newunicodechar{₹}{\rupee}' in lyx
    assert '₹ 7' in tex and '₹ 7' in lyx


@pytest.mark.parametrize(('requested','width','height','expected'), [
    (.75, 1200, 400, .39),   # landscape: width cap, then 25% reduction
    (.60, 600, 600, .346),   # square: height cap, then 25% reduction
    (.60, 300, 600, .173),   # portrait: height cap, then 25% reduction
    (.60, 150, 900, .058),   # extremely tall: height cap, then 25% reduction
    (.25, 1200, 400, .188),  # smaller source-requested size is also reduced
])
def test_balanced_image_scale(requested, width, height, expected):
    assert fit_image_scale(requested, width, height) == expected


def test_publication_keeps_previous_snapshot(tmp_path):
    destination=tmp_path/'module';destination.mkdir();(destination/'file').write_text('old')
    staged=tmp_path/'staged';staged.mkdir();(staged/'file').write_text('new')
    support.publish(staged,destination)
    assert (destination/'file').read_text()=='new'
    assert next(tmp_path.glob('module.previous-*')).joinpath('file').read_text()=='old'


def test_duplicate_pdf_markers_and_scanned_reference(tmp_path):
    import pymupdf
    from validate_against_pdf import validate_reference
    path=tmp_path/'empty.pdf'
    with pymupdf.open() as doc:
        doc.new_page();doc.set_toc([[1,'Chapter Notes: One',1],[1,'Chapter Notes: One',1]])
        assert map_pdf(doc,[dict(num=1,name='One')])==[dict(chapter=1,start_page=1,end_page=1)]
        doc.save(path)
    with pytest.raises(support.ValidationError,match='no extractable'):
        validate_reference(path,[dict(num=1,name='One',elements=[])],{})

def test_images_inside_formatted_lists_are_not_lost():
    elements=parse_html('<article><p>Introduction.</p><ul><li><strong>Before <span><img src="https://x/test_lg.jpg"></span> after</strong></li></ul></article>')
    assert [e['type'] for e in elements]==['body','list','image','list']
    assert elements[1]['items'][0][1][0]['bold']
    assert elements[3]['items'][0][1][0]['bold']


def test_table_spans_fail_instead_of_flattening():
    with pytest.raises(ValueError,match='Complex table'):
        parse_html('<table><tr><td colspan="2">Merged cell</td></tr></table>')


def test_compiler_failure_does_not_publish(tmp_path,monkeypatch):
    import scrape_chapters
    from build_support import atomic_write,cache_path
    url='https://example.org/t/1/Chapter-Notes-One'
    links=tmp_path/'links';links.write_text(url+' - Chapter1')
    output=tmp_path/'out';good=output/'notes';good.mkdir(parents=True);(good/'original').write_text('keep')
    cache=tmp_path/'cache';atomic_write(cache_path(cache,url,'pages'),b'<p>A complete sample paragraph.</p>')
    monkeypatch.setattr(support,'preflight',lambda: {})
    monkeypatch.setattr(support,'compile_documents',Mock(side_effect=support.BuildError('compiler failure')))
    args=['--links',str(links),'--module','notes','--cache-dir',str(cache),'--output-dir',str(output),'--offline']
    assert scrape_chapters.main(args)==1
    assert (good/'original').read_text()=='keep'
    assert any('compiler failure' in p.read_text() for p in output.glob('notes-*/report.txt'))


def test_html_invalid_fetch_not_cached(tmp_path):
    session=Mock();session.get.return_value=response(content=b'<title>Access denied</title><p>Blocked</p>')
    path=tmp_path/'cache'
    with pytest.raises(support.BuildError):support.cached_fetch(session,'url',path,lambda data:parse_html(data.decode()))
    assert not path.exists()


def test_retry_after_http_date():
    from datetime import datetime,timezone,timedelta
    from email.utils import format_datetime
    delay=support.retry_delay(format_datetime(datetime.now(timezone.utc)+timedelta(seconds=20)),0)
    assert 18 <= delay <= 20

def test_legacy_currency_rendering():
    assert inline.tex([('Rs. 250',False)])==r'\rupee~ 250'
    assert inline.lyx([('₹250',False)]) == '₹250'

def test_two_currency_amounts_are_not_inferred_as_equations():
    runs=inline.text_runs('Prices are $5 and $10.')
    assert all(s['kind']=='text' for s in runs)
    assert inline.tex(runs)==r'Prices are \$5 and \$10.'

def test_reference_counts_the_generated_chapter_title(tmp_path):
    import pymupdf
    from validate_against_pdf import validate_reference
    source=tmp_path/'reference.pdf'
    with pymupdf.open() as doc:
        page=doc.new_page();page.insert_text((72,72),'Unique Heading\nA substantive body sentence.')
        doc.set_toc([[1,'Unique Heading',1]]);doc.save(source)
    chapters=[dict(num=1,name='Unique Heading',elements=[dict(type='body',text='A substantive body sentence.',segments=[('A substantive body sentence.',False)])])]
    assert validate_reference(source,chapters,{})[0]['coverage']==1

def test_edurev_navigation_table_is_skipped_before_span_validation():
    result=parse_html('<article><table class="tbl_cntnt"><tr><td>Table of Contents</td></tr><tr><td colspan="2">Navigation</td></tr></table><h2>Chapter topic</h2><p>Substantive chapter content.</p></article>')
    assert [e['type'] for e in result]==['heading','body']

def test_notes_exclude_embedded_quiz_widgets():
    elements=parse_html('<article><p>Real notes.</p><div id="content_questions"><p>Question and solution widget</p></div><p>More notes.</p></article>')
    assert [e['text'] for e in elements]==['Real notes.','More notes.']


def test_notes_exclude_optional_fact_callouts_and_all_quiz_variants():
    html = '''<article>
      <p>Real notes before.</p>
      <blockquote><p><strong>Fun fact!</strong></p><p>Optional thermometer fact.</p></blockquote>
      <div class="question_block_42"><p>Try yourself: A question?</p><p>Option A</p></div>
      <blockquote><strong>Do you know?</strong><p>Optional seed fact.</p></blockquote>
      <p>The teacher asked, "Do you know the answer?" This is ordinary prose.</p>
    </article>'''
    elements = parse_html(html)
    assert [e['text'] for e in elements] == [
        'Real notes before.',
        'The teacher asked, "Do you know the answer?" This is ordinary prose.',
    ]


def test_typographic_dashes_match_tex_punctuation():
    assert norm('Health—not just disease')==norm('Health---not just disease')
    assert norm('20 °C') == norm('20 ◦C')


def test_reference_lines_exclude_embedded_quiz():
    page = Mock()
    page.rect.height = 800
    def line(text, y): return {'bbox': (0, y, 100, y + 10), 'spans': [{'text': text, 'size': 10, 'font': 'Arial'}]}
    page.get_text.return_value = {'blocks': [{'lines': [
        line('Notes before quiz.', 100), line('MULTIPLE CHOICE QUESTION', 120),
        line('Try yourself: A question?', 140), line('An option.', 160),
        line('View Solution', 180), line('Notes after quiz.', 200),
    ]}]}
    assert reference_lines(page) == ['Notes before quiz.', 'Notes after quiz.']


def test_rendered_text_ignores_page_furniture_inside_a_paragraph():
    class Rect:
        height = 800

    class Page:
        rect = Rect()
        def __init__(self, lines): self.lines = lines
        def get_text(self, kind):
            assert kind == 'dict'
            return {'blocks': [{'lines': [
                {'bbox': (0, y, 100, y + 10), 'spans': [{'text': text}]}
                for y, text in self.lines
            ]}]}

    doc = [
        Page([(700, 'Temperature often affects how much solute a solvent can dissolve.')]),
        Page([(40, '10'), (60, 'Chapter 1. Solutes and Solutions'),
              (90, 'solubility increases with temperature.'), (300, 'Effect of temperature')]),
    ]
    page_range = {'start_page': 1, 'end_page': 2}
    text = rendered_text(doc, page_range, ['Solutes and Solutions', 'Effect of temperature'])
    assert norm('Temperature often affects how much solute a solvent can dissolve. solubility increases with temperature.') in text
    assert norm('Chapter 1. Solutes and Solutions') not in text
    assert norm('Effect of temperature') in text
