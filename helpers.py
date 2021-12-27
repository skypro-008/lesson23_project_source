import itertools
from functools import reduce


def make_filter(filter_phrase):
    def filterer(logs):
        return filter(lambda logs_line: filter_phrase in logs_line, logs)

    return filterer


def make_map(idx):
    def mapper(logs):
        return map(lambda logs_line: logs_line.split(' ')[idx], logs)

    return mapper


def make_unique():
    def unique(logs):
        return logs

    return unique


def make_sort(is_asc=True):
    def sort(logs):
        return sorted(logs, reverse=not is_asc)

    return sort


def make_limit(count):
    def limit(logs):
        return itertools.islice(logs, 0, count)

    return limit


def get_closure(type: str, param):
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


def compose_closures(*closures):
    def inner(f, g):
        return lambda *args, **kwargs: f(g(*args, **kwargs))

    return reduce(inner, reversed(closures), lambda x: x)
