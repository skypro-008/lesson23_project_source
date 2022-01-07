import itertools
import re
from functools import reduce
from typing import Dict, Callable, Iterable, Generator


def get_response(params: Dict[str, str]) -> Iterable[str]:
    logs = read_file(params['file_name'])
    return compose_closures(
        get_closure(params['cmd1'], params['value1']),
        get_closure(params['cmd2'], params['value2'])
    )(logs)


def read_file(file_name: str) -> Generator[str, None, None]:
    for row in open(f'data/{file_name}', 'r'):
        yield row


def make_filter(filter_phrase: str) -> Callable[[Iterable[str]], Iterable[str]]:
    def filterer(logs: Iterable[str]) -> Iterable[str]:
        return filter(lambda logs_line: filter_phrase in logs_line, logs)

    return filterer


def make_map(idx: int) -> Callable[[Iterable[str]], Iterable[str]]:
    def mapper(logs: Iterable[str]) -> Iterable[str]:
        return map(lambda logs_line: logs_line.split(' ')[idx], logs)

    return mapper


def make_unique() -> Callable[[Iterable[str]], Iterable[str]]:
    def unique(logs: Iterable[str]) -> Iterable[str]:
        return set(logs)

    return unique


def make_sort(is_asc: bool = True) -> Callable[[Iterable[str]], Iterable[str]]:
    def sort(logs: Iterable[str]) -> Iterable[str]:
        return sorted(logs, reverse=not is_asc)

    return sort


def make_limit(count: int) -> Callable[[Iterable[str]], Iterable[str]]:
    def limit(logs: Iterable[str]) -> Iterable[str]:
        return itertools.islice(logs, 0, count)

    return limit


def make_regex(r_str: str) -> Callable[[Iterable[str]], Iterable[str]]:
    pattern = re.compile(r_str)

    def regex(logs: Iterable[str]) -> Iterable[str]:
        return filter(
            lambda logs_line: bool(re.search(pattern, logs_line)),
            logs
        )

    return regex


def get_closure(type: str, param: str) -> Callable[[Iterable[str]], Iterable[str]]:
    if type == 'filter':
        return make_filter(param)
    if type == 'map':
        return make_map(int(param))
    if type == 'unique':
        return make_unique()
    if type == 'sort':
        return make_sort(param == 'asc')
    if type == 'limit':
        return make_limit(int(param))
    if type == 'regex':
        return make_regex(param)
    return lambda x: x


def compose_closures(*closures: Callable) -> Callable:
    def inner(f: Callable, g: Callable) -> Callable:
        return lambda *args, **kwargs: f(g(*args, **kwargs))

    return reduce(inner, reversed(closures), lambda x: x)
