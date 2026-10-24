RUNNING_HEADERS = r'''
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\thepage}
\fancyhead[LO]{\parbox[b]{.88\textwidth}{\raggedright\small\rightmark}}
\fancyhead[RE]{\parbox[b]{.88\textwidth}{\raggedleft\small\leftmark}}
\setlength{\headheight}{32pt}
\renewcommand{\headrulewidth}{0pt}
'''


def tex_content(elements, render, tex_escape):
    output = []
    for element in elements:
        kind = element['type']
        if kind == 'body':
            rendered = render(element['segments'])
            if element.get('answer_blank'):
                rendered = (r'\parbox[t]{\dimexpr\linewidth-8em\relax}{' + rendered
                            + r'}\hfill\mbox{\_\_\_\_\_\_\_\_}')
            output.append(('{\\raggedright ' + rendered + '\\par}\n') if element.get('ragged_right') else rendered + '\\par\n')
        elif kind == 'answer_lines':
            output.extend('\\par\\noindent\\rule{\\linewidth}{0.3pt}\\par\\vspace{0.55em}\n' for _ in range(element['count']))
        elif kind == 'image':
            output.append('\\par\\begin{center}\\includegraphics[width=' + str(element['scale']) + '\\textwidth]{media/' + element['filename'] + '}\\end{center}\n')
        elif kind == 'subquestions':
            output.append('\\begin{enumerate}[label=(\\alph*)]\n')
            for item in element['items']:
                output.append('\\item ' + tex_content(item['content'], render, tex_escape))
            output.append('\\end{enumerate}\n')
        elif kind == 'table':
            widths = element.get('widths', [1 / len(element['rows'][0])] * len(element['rows'][0]))
            columns = '|' + '|'.join('p{\\dimexpr ' + str(width) + '\\linewidth-2\\tabcolsep-2\\arrayrulewidth\\relax}' for width in widths) + '|'
            output.append('\\par\\noindent\\begin{tabular}{' + columns + '}\\hline\n')
            for row_number, row in enumerate(element['rows']):
                if row_number == 0 and element.get('merged_header'):
                    output.append('\\multicolumn{' + str(len(row)) + '}{|c|}{' + tex_escape(row[0]) + '}')
                else:
                    output.append(' & '.join(tex_escape(cell) for cell in row))
                output.append('\\\\\\hline\n')
            output.append('\\end{tabular}\\par\\medskip\n')
        elif kind == 'options':
            from inline_content import tex, text_runs
            # Options need the same typed scripts as question prompts; escaping
            # flat text alone loses the supplied superscript letter-o notation.
            options = [tex(text_runs(value)) for value in element['values']]
            output.append('\\par\\begin{tabular}{@{}p{.48\\linewidth}p{.48\\linewidth}@{}}\n')
            output.append('$\\square$ A) ' + options[0] + ' & $\\square$ B) ' + options[1] + '\\\\\n')
            output.append('$\\square$ C) ' + options[2] + ' & $\\square$ D) ' + options[3] + '\n\\end{tabular}\\par\n')
        else:
            raise ValueError('Unsupported question content: ' + kind)
    return ''.join(output)


def lyx_ert(text):
    return '\\begin_inset ERT\nstatus collapsed\n\n\\begin_layout Plain Layout\n' + text.replace('\\', '\\backslash\n') + '\n\\end_layout\n\\end_inset\n'


def lyx_content(elements, render, tex_escape, depth=0):
    output = []
    for element in elements:
        kind = element['type']
        if kind == 'subquestions':
            output.append('\\begin_deeper\n')
            for item in element['items']:
                output.append(lyx_question(item['content'], render, tex_escape))
            output.append('\\end_deeper\n')
            continue
        output.append('\\begin_layout Standard\n')
        if kind == 'body':
            output.append(render(element['segments']))
        elif kind == 'answer_lines':
            output.append(lyx_ert(''.join('\\par\\noindent\\rule{\\linewidth}{0.3pt}\\par\\vspace{0.55em}\n' for _ in range(element['count']))))
        elif kind == 'image':
            output.append('\\align center\n\\begin_inset Graphics\n\tfilename media/' + element['filename'] + '\n\twidth ' + str(round(element['scale'] * 100)) + 'text%\n\\end_inset\n')
        elif kind == 'table':
            rows = element['rows']
            widths = element.get('widths', [1 / len(rows[0])] * len(rows[0]))
            output.append('\\begin_inset Tabular\n<lyxtabular version="3" rows="' + str(len(rows)) + '" columns="' + str(len(rows[0])) + '">\n<features tabularvalignment="middle">\n')
            for width in widths:
                output.append('<column alignment="left" valignment="top" width="' + str(round(width * (100 - 4 * len(widths)), 2)) + 'line%">\n')
            for row_number, row in enumerate(rows):
                output.append('<row>\n')
                for column_number, cell in enumerate(row):
                    merged = ''
                    if row_number == 0 and element.get('merged_header'):
                        merged = ' multicolumn="' + ('1' if column_number == 0 else '2') + '"'
                    output.append('<cell' + merged + ' alignment="left" valignment="top" topline="true" bottomline="true" leftline="true" rightline="true" usebox="none">\n\\begin_inset Text\n\\begin_layout Plain Layout\n' + render([(cell, False)]) + '\n\\end_layout\n\\end_inset\n</cell>\n')
                output.append('</row>\n')
            output.append('</lyxtabular>\n\\end_inset\n')
        elif kind == 'options':
            output.append(lyx_ert(tex_content([element], None, tex_escape)))
        else:
            raise ValueError('Unsupported question content: ' + kind)
        output.append('\n\\end_layout\n')
    return ''.join(output)


def lyx_question(content, render, tex_escape):
    first = content[0]
    if first['type'] != 'body':
        raise ValueError('Question must start with supplied text')
    first_text = render(first['segments'])
    if first.get('answer_blank'):
        first_text = (lyx_ert(r'\parbox[t]{\dimexpr\linewidth-8em\relax}{')
                      + first_text + '\n'
                      + lyx_ert(r'}\hfill\mbox{\_\_\_\_\_\_\_\_}'))
    alignment = '\\align left\n' if first.get('ragged_right') else ''
    output = '\\begin_layout Enumerate\n' + alignment + first_text + '\n\\end_layout\n'
    if len(content) > 1:
        for element in content[1:]:
            if element['type'] == 'subquestions':
                output += lyx_content([element], render, tex_escape)
            else:
                output += '\\begin_deeper\n' + lyx_content([element], render, tex_escape) + '\\end_deeper\n'
    return output
