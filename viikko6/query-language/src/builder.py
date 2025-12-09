from typing import Self, Tuple
from matchers import And, HasAtLeast, PlaysIn, HasFewerThan, All, Or


class Query:
    def __init__(self, stack: Tuple[Self] | None = None, matcher=All()):
        self._stack = (*(stack or tuple()), matcher)

    def build(self):
        return And(*self._stack)

class QueryBuilder(Query):
    def one_of(self, *queries: Self):
        built = map(lambda q: q.build(), queries)
        return QueryBuilder(self._stack, Or(*built))

    def plays_in(self, team: str) -> Self:
        return QueryBuilder(self._stack, PlaysIn(team))

    def has_at_least(self, value: int, attr: str) -> Self:
        return QueryBuilder(self._stack, HasAtLeast(value, attr))

    def has_fewer_than(self, value: int, attr: str) -> Self:
        return QueryBuilder(self._stack, HasFewerThan(value, attr))
    