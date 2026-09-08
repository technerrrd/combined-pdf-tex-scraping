"""Real compiler acceptance test. Run explicitly with pytest -m integration."""
import hashlib
import io
import json
from pathlib import Path
import pytest
import pymupdf
from PIL import Image
from build_support import atomic_write, cache_path
from scrape_chapters import main


@pytest.mark.integration
def test_complete_module_and_reference_rejection(tmp_path):
    url='https://example.org/t/1/Chapter-Notes-Scientific-Notation'
    image_url='https://example.org/science_lg.jpg'
    links=tmp_path/'CHAPTER-LINKS'; links.write_text(url+' - Chapter1\n')
    cache=tmp_path/'cache'; output=tmp_path/'output'
    html=(Path(__file__).parent/'fixtures/chapter.html').read_bytes()
    atomic_write(cache_path(cache,url,'pages'),html)
    buf=io.BytesIO(); Image.new('RGB',(420,200),'orange').save(buf,format='JPEG')
    atomic_write(cache_path(cache,image_url,'images'),buf.getvalue())
    args=['--links',str(links),'--module','fixture','--title','Scientific Notation','--cache-dir',str(cache),'--output-dir',str(output),'--offline']
    assert main(args)==0
    module=output/'fixture'
    for kind in ('tex','lyx'):
        with pymupdf.open(module/f'fixture-{kind}.pdf') as doc:
            assert doc.get_toc()
            assert 'Scientific notation' in ''.join(p.get_text() for p in doc)
    reference=tmp_path/'reference.pdf'; reference.write_bytes((module/'fixture-tex.pdf').read_bytes())
    assert main(args+['--pdf',str(reference)])==0
    report=json.loads((module/'report.json').read_text())
    assert report['reference_status']=='passed'
    assert len(report['coverage'])==3
    old={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in module.glob('*') if p.is_file()}
    bad=tmp_path/'bad.pdf'
    with pymupdf.open(reference) as doc:
        page=doc[-1]
        # Distinct reference lines that cannot match either output.
        for i in range(15): page.insert_text((30,30+i*12),f'Absent validation statement {i} with unique wording')
        doc.save(bad)
    assert main(args+['--pdf',str(bad)])==2
    assert old=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in module.glob('*') if p.is_file()}
    # A required cached asset disappearing must also preserve the successful output.
    cache_path(cache,image_url,'images').unlink()
    assert main(args)==1
    assert old=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in module.glob('*') if p.is_file()}
