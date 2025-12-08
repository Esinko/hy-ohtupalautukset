from typing import Self
from matchers import And, HasAtLeast, PlaysIn, Not, HasFewerThan, All, Or


class Query:
    def __init__(self, stack=None, matcher=None):
        self._stack = stack 
        self._matcher = matcher
        
        if not self._stack:
            self._stack = self._matcher
        else:
            self._stack = And(self._stack, self._matcher)

    def build(self):
        return And(self._stack or All(), self._matcher or All())

class QueryBuilder(Query):
    def plays_in(self, team: str) -> Self:
        return self.__class__(self._stack, PlaysIn(team))

    def has_at_least(self, value: int, attr: str) -> Self:
        return self.__class__(self._stack, HasAtLeast(value, attr))

    def has_fewer_than(self, value: int, attr: str) -> Self:
        return self.__class__(self._stack, HasFewerThan(value, attr))
    