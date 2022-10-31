import tomllib
from html import escape
from dataclasses import dataclass
from typing import Optional, Self, Union

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


@dataclass(frozen=True, kw_only=True)
class OperatorInstance:
    name: str
    url: Optional[str]

    @staticmethod
    def from_toml(toml: Union[dict, str], library_name: str) -> Self:
        if isinstance(toml, str):
            return OperatorInstance(name=toml, url=_default_url(library_name, toml))

        name = toml['name']
        url = toml.get('url') or _default_url(library_name, name)
        return OperatorInstance(name=name, url=url)


@dataclass(frozen=True, kw_only=True)
class Operator:
    instances: dict[str, OperatorInstance]

    @staticmethod
    def from_toml(toml: dict):
        instances = { library:OperatorInstance.from_toml(instance, library) for library, instance in toml.items() }
        return Operator(instances=instances)


def _operator_cell(operator: OperatorInstance) -> str:
    if operator is None:
        return _ABSENT_OPERATOR

    label = f'<code>{escape(operator.name)}</code>'
    label = f'<a href="{escape(operator.url)}">{label}</a>' if operator.url is not None else label
    return f'<td>{label}</td>'


def _default_url(library_name: str, operator_name: str) -> str:
    match library_name:
        case 'fsharp':
            return _default_fsharp_url(operator_name)


def _default_fsharp_url(operator_name: str) -> str:
    return f'https://fsharp.github.io/fsharp-core-docs/reference/fsharp-collections-seqmodule.html#{operator_name}'


def _operator_row(operator: Operator):
    cells = [_operator_cell(operator.instances.get(library)) for library in _LIBRARIES]
    return f'<tr>{_NEWLINE.join(cells)}</tr>'


with open("operators.toml", "rb") as f:
    operators = [Operator.from_toml(o) for o in tomllib.load(f)['operators']]

with open("template.html", "r") as f:
    template = f.read()

rows = _NEWLINE.join((_operator_row(operator) for operator in operators))

with open("generated.html", "w") as f:
    f.write(template.replace('<!-- OPERATORS -->', rows))