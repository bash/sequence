import tomllib
from html import escape

_LIBRARIES = [
    'dotnet',
    'funcky',
    'fsharp',
    'rust',
    'rust_itertools',
    'python',
    'more_itertools',
    'javascript',
    'npm_itertools',
    'java',
]

_ABSENT_OPERATOR = '<td>&mdash;</td>'

_NEWLINE = '\n'

def _operator_cell(operator) -> str:
    if operator is None:
        return _ABSENT_OPERATOR
    else:
        url = operator.get('url')
        label = f'<code>{operator["name"]}</code>'
        label = f'<a href="{url}">{label}</a>' if url is not None else label
        return f'<td>{label}</td>'

def _operator_row(operator):
    cells = [_operator_cell(operator.get(library)) for library in _LIBRARIES]
    return f'<tr>{_NEWLINE.join(cells)}</tr>'

with open("operators.toml", "rb") as f:
    operators = tomllib.load(f)['operators']

with open("template.html", "r") as f:
    template = f.read()

rows = _NEWLINE.join((_operator_row(operator) for operator in operators))

with open("generated.html", "w") as f:
    f.write(template.replace('<!-- OPERATORS -->', rows))