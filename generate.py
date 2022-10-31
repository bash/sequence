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

def _operator_cell(operator, library_name: str) -> str:
    if operator is None:
        return _ABSENT_OPERATOR

    operator_name = operator['name']
    url = operator.get('url') or _default_url(library_name, operator_name)
    label = f'<code>{escape(operator_name)}</code>'
    label = f'<a href="{escape(url)}">{label}</a>' if url is not None else label
    return f'<td>{label}</td>'


def _default_url(library_name: str, operator_name: str) -> str:
    match library_name:
        case 'fsharp':
            return _default_fsharp_url(operator_name)


def _default_fsharp_url(operator_name: str) -> str:
    seq_prefix = "Seq."
    if operator_name.startswith(seq_prefix):
        return f'https://fsharp.github.io/fsharp-core-docs/reference/fsharp-collections-seqmodule.html#{operator_name[len(seq_prefix):]}'


def _operator_row(operator):
    cells = [_operator_cell(operator.get(library), library) for library in _LIBRARIES]
    return f'<tr>{_NEWLINE.join(cells)}</tr>'


with open("operators.toml", "rb") as f:
    operators = tomllib.load(f)['operators']

with open("template.html", "r") as f:
    template = f.read()

rows = _NEWLINE.join((_operator_row(operator) for operator in operators))

with open("generated.html", "w") as f:
    f.write(template.replace('<!-- OPERATORS -->', rows))