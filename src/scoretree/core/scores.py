from __future__ import annotations

from colorama import Style

from .formatter import Formatter


class Score(Formatter):

    def __init__(self, name, weight, score_range, value=0, inverse=False):
        self._name = name
        self._weight = weight
        self._score_range = score_range
        self._value = value
        self._inverse = inverse

        self._compute_score()
        # self._computed = randrange(0, 100) / 100

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    def _compute_score(self):
        self._computed = abs(self._inverse - (
            min(
                self._value - self._score_range[0],
                self._score_range[1] - self._score_range[0]
            ) / (self._score_range[1] - self._score_range[0])
        ))

        self._computed = min(
            self._score_range[1],
            max(self._computed, self._score_range[0])
        )

    def __repr__(self):
        return f"Score({self.name}, {self.weight})"

    def render(self, indent=1):
        return self.colorize(
            Style.DIM
            + self.indent(indent)
            + f"{self.name.title()} ({self.weight * 100:.2f}%): {self._computed * 100:.2f}%",
            self._computed
        )


class Area(Formatter):

    def __init__(self, name: str, weight: float, scores: list[Score | Area]):
        self.name = name
        self.weight = weight
        self.scores = scores

        self._compute_score()
        # self._computed = randrange(0, 100) / 100

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def scores(self):
        return self._scores

    @scores.setter
    def scores(self, value):
        self._scores = value

    def _compute_score(self):
        self._computed = sum(
            item._computed * item._weight
            for item in self.scores
        )

    def __repr__(self):
        return f"Area({self.name}, {self.weight})"

    def render(self, indent=1):
        return self.colorize(
            Style.NORMAL
            + f"{self.indent(indent)}{self.name.title()} ({self.weight * 100:.2f}%): {self._computed * 100:.2f}%\n"
            + f"\n".join(
                item.render(indent + 1)
                for item in self.scores
            ),
            self._computed
        )
