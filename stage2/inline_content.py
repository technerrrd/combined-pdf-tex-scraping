"""Typed inline content shared by HTML, TeX and LyX; legacy pairs remain accepted."""
import re
import unicodedata

SYMBOLS = dict(zip('αβγδεζηθικλμνξπρστυφχψωΓΔΘΛΞΠΣΦΨΩ',
    ['\\'+s for s in 'alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi pi rho sigma tau upsilon phi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Phi Psi Omega'.split()]))
SYMBOLS.update(dict(zip('→←↔⇌⟶×÷±≈≤≥≠∞∴°·',
    ['\\'+s for s in 'to leftarrow leftrightarrow rightleftharpoons longrightarrow times div pm approx leq geq neq infty therefore circ cdot'.split()])))
COMMANDS = set('frac dfrac tfrac sqrt text mathrm mathbf mathit mathcal mathbb operatorname left right overline underline hat widehat bar vec dot ddot tilde widetilde sin cos tan log ln exp lim sum prod int iint partial nabla cdots ldots vdots ddots quad qquad space begin end cases matrix pmatrix bmatrix vmatrix aligned array displaystyle textstyle limits nonumber'.split()) | {v[1:] for v in SYMBOLS.values()}
COMMANDS |= set('epsilon varepsilon vartheta varphi varrho varsigma omega degree angle perp parallel cup cap subset subseteq in notin forall exists emptyset lbrace rbrace langle rangle vert Vert'.split())
ENVIRONMENTS = {'matrix', 'pmatrix', 'bmatrix', 'vmatrix', 'cases', 'aligned'}


def check_math(value):
    if not value.strip(): raise ValueError('Empty explicit equation')
    for symbol, command in SYMBOLS.items():
        value = value.replace(symbol, command + ' ')
    if '%' in value or '#' in value or '$' in value:
        raise ValueError('Unsupported math character (%, # or $); review expression')
    depth = 0
    for token in re.findall(r'\\[A-Za-z]+|\\.|[{}]', value):
        if token.startswith('\\'):
            name = token[1:]
            if name not in COMMANDS and name not in '{}_,;:! |\\':
                raise ValueError(f'Unsupported LaTeX command: {token}')
        elif token == '{':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                raise ValueError('Unbalanced math braces')
    if depth:
        raise ValueError('Unbalanced math braces')
    stack = []
    for kind, env in re.findall(r'\\(begin|end)\{([^}]+)\}', value):
        if env not in ENVIRONMENTS:
            raise ValueError(f'Unsupported math environment: {env}')
        if kind == 'begin':
            stack.append(env)
        elif not stack or stack.pop() != env:
            raise ValueError('Unbalanced math environments')
    if stack:
        raise ValueError('Unbalanced math environments')
    return value


def run(text, bold=False, kind='text', display=False):
    return dict(kind=kind, text=text, bold=bold, display=display)


def adapt(segments):
    return [s if isinstance(s, dict) else run(s[0], s[1]) for s in segments]


def plain(segments):
    return ''.join(s['text'] for s in adapt(segments))


def text_runs(text, bold=False):
    # Dollar pairs require explicit matching; standalone currency remains plain text.
    pattern = r'(?<!\\)(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)|\$[^$\n]+?\$(?!\d))'
    result = []
    for part in re.split(pattern, text):
        if not part:
            continue
        if re.fullmatch(pattern, part):
            display = part.startswith(('$$', r'\['))
            size = 2 if part.startswith(('$$', r'\[', r'\(')) else 1
            result.append(run(check_math(part[size:-size]), bold, 'math', display))
            continue
        if any(x in part for x in (r'\(', r'\)', r'\[', r'\]', '$$')):
            raise ValueError('Unclosed explicit math delimiter')
        buffer = ''
        for c in part:
            name = unicodedata.name(c, '')
            kind = 'sub' if 'SUBSCRIPT' in name else 'sup' if 'SUPERSCRIPT' in name else None
            if c in SYMBOLS or kind:
                if buffer:
                    result.append(run(buffer, bold)); buffer = ''
                result.append(run(SYMBOLS[c], bold, 'math') if c in SYMBOLS else run(unicodedata.normalize('NFKC', c), bold, kind))
            else:
                buffer += c
        if buffer:
            result.append(run(buffer, bold))
    return result


def escape(text):
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
                    '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}', '_': r'\_'}
    return ''.join(replacements.get(c, c) for c in text)


def tex(segments):
    parts = []
    for s in adapt(segments):
        kind, value = s['kind'], s['text']
        if kind == 'math':
            value = check_math(value)
            rendered = (r'\[' + value + r'\]') if s.get('display') else '$' + value + '$'
        elif kind in ('sub', 'sup'):
            rendered = '\\text' + ('subscript' if kind == 'sub' else 'superscript') + '{' + escape(value) + '}'
        else:
            rendered = escape(value).replace('₹', r'\rupee~').replace('Rs.', r'\rupee~').replace('INR', r'\rupee~')
        if s.get('bold'):
            rendered = r'\textbf{' + rendered + '}'
        parts.append(rendered)
    return ''.join(parts)


def lyx(segments):
    parts = []
    for s in adapt(segments):
        if s.get('bold'):
            parts.append('\\series bold\n')
        kind, value = s['kind'], s['text']
        if kind == 'math':
            delim = '$$' if s.get('display') else '$'
            parts.append('\\begin_inset Formula ' + delim + check_math(value) + delim + '\n\\end_inset\n')
        elif kind in ('sub', 'sup'):
            parts.append('\\begin_inset script ' + ('subscript' if kind == 'sub' else 'superscript') + '\n\\begin_layout Plain Layout\n' + value.replace('\\', '\\backslash\n') + '\n\\end_layout\n\\end_inset\n')
        else:
            currency = '\\begin_inset ERT\nstatus collapsed\n\n\\begin_layout Plain Layout\n\\backslash\nrupee~\n\\end_layout\n\n\\end_inset\n'
            escaped = value.replace('\\', '\\backslash\n')
            parts.append(escaped.replace('₹', currency).replace('Rs.', currency).replace('INR', currency))
        if s.get('bold'):
            parts.append('\n\\series default\n')
    return ''.join(parts)


def mathml(node):
    """Conservative Presentation MathML conversion; never flatten unknown constructs."""
    tag = node.name.split(':')[-1]
    children = [c for c in node.children if getattr(c, 'name', None)]
    if tag == 'semantics':
        annotation = node.find('annotation', attrs={'encoding': re.compile('tex', re.I)})
        return check_math(annotation.get_text()) if annotation else mathml(children[0])
    if tag in ('math', 'mrow', 'mstyle', 'mpadded'):
        return ' '.join(mathml(c) for c in children)
    if tag in ('mi', 'mn', 'mo'):
        return check_math(node.get_text().strip())
    if tag == 'mtext':
        return r'\text{' + escape(node.get_text()) + '}'
    if tag in ('msub', 'msup', 'msubsup', 'mfrac', 'mroot'):
        expected = 3 if tag == 'msubsup' else 2
        if len(children) != expected:
            raise ValueError(f'Invalid MathML {tag} child count')
        values = [mathml(c) for c in children]
        if tag == 'mfrac': return r'\frac{' + values[0] + '}{' + values[1] + '}'
        if tag == 'mroot': return r'\sqrt[' + values[1] + ']{' + values[0] + '}'
        result = '{' + values[0] + '}'
        if tag in ('msub', 'msubsup'): result += '_{' + values[1] + '}'
        if tag in ('msup', 'msubsup'): result += '^{' + values[-1] + '}'
        return result
    if tag == 'msqrt': return r'\sqrt{' + ' '.join(mathml(c) for c in children) + '}'
    if tag == 'mfenced':
        opening, closing = node.get('open', '('), node.get('close', ')')
        if opening not in ('(', '[', '|') or closing not in (')', ']', '|'):
            raise ValueError('Unsupported MathML fence')
        return r'\left' + opening + ','.join(mathml(c) for c in children) + r'\right' + closing
    if tag in ('mover', 'munder') and len(children) == 2:
        accent = children[1].get_text().strip()
        command = {'^': 'hat', 'ˆ': 'hat', '~': 'tilde', '¯': 'bar', '→': 'vec', '.': 'dot', '˙': 'dot', '_': 'underline'}.get(accent)
        if command: return '\\' + command + '{' + mathml(children[0]) + '}'
        return '{' + mathml(children[0]) + '}' + ('^' if tag == 'mover' else '_') + '{' + mathml(children[1]) + '}'
    if tag == 'mtable':
        return r'\begin{matrix}' + r' \\ '.join(mathml(c) for c in children) + r'\end{matrix}'
    if tag == 'mtr': return ' & '.join(mathml(c) for c in children)
    if tag == 'mtd': return ' '.join(mathml(c) for c in children)
    raise ValueError(f'Unsupported MathML element: {tag}')


def from_html(node, bold=False):
    """Walk inline markup once, ignoring duplicate accessible/visual math trees."""
    from bs4 import Comment
    if isinstance(node, Comment): return []
    name = getattr(node, 'name', None)
    if name is None:
        return text_runs(re.sub(r'\s+', ' ', str(node)), bold)
    if name in ('ul', 'ol', 'img', 'style'):
        return []
    if name == 'script':
        if not node.get('type', '').startswith('math/tex'): return []
        return [run(check_math(str(node.string or '')), bold, 'math', 'mode=display' in node.get('type', ''))]
    if name == 'math':
        return [run(check_math(mathml(node)), bold, 'math', node.get('display') == 'block')]
    if name == 'mjx-container' or 'katex' in node.get('class', []):
        source = node.find('math')
        if source is None: raise ValueError('Rendered math lacks a recoverable equation source')
        return from_html(source, bold)
    if name in ('sub', 'sup'):
        return [run(node.get_text(), bold, name)]
    if name == 'br': return [run(' ', bold)]
    result = []
    for child in node.children:
        result.extend(from_html(child, bold or name in ('strong', 'b')))
    return result
