from __future__ import annotations

from colorama import Style

from .formatter import Formatter


class Score(Formatter):

    def __init__(
        self,
        name: str,
        weight: int | float,
        score_range: tuple[int | float, int | float],
        value: int | float = 0,
        inverse: bool = False
    ) -> None:
        """Initialize a Score instance.

        Args:
            name (str): score name.
            weight (int | float): score weight.
            score_range (tuple[int  |  float, int  |  float]): score range from
                minimum to maximum.
            value (int | float, optional): current value. Defaults to 0.
            inverse (bool, optional): whether to invert the score calculation
                process. Defaults to False.
        """
        self.name = name
        self.weight = weight
        self.score_range = score_range
        self.value = value
        self.inverse = inverse

        self._compute_score()

    @property
    def name(self) -> str:
        """Get score name.

        Returns:
            str: score name.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set score name.

        Args:
            value (str): score name.
        """
        if not isinstance(value, str):
            raise TypeError(
                "expected type str for"
                + f" {self.__class__.__name__}.name but got"
                + f" {type(value).__name__} instead"
            )

        self._name = value

    @property
    def weight(self) -> int | float:
        """Get score weight.

        Returns:
            int | float: score weight.
        """
        return self._weight

    @weight.setter
    def weight(self, value: int | float) -> None:
        """Set score weight.

        Args:
            value (int | float): score weight.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type int | float for"
                + f" {self.__class__.__name__}.weight but got"
                + f" {type(value).__name__} instead"
            )

        self._weight = value

    @property
    def score_range(self) -> tuple[int | float, int | float]:
        """Get score range.

        Returns:
            tuple[int | float, int | float]: score range.
        """
        return self._score_range

    @score_range.setter
    def score_range(self, value: tuple[int | float, int | float]) -> None:
        """Set score range.

        Args:
            value (tuple[int | float, int | float]): score range.
        """
        if not isinstance(value, tuple):
            raise TypeError(
                "expected type tuple[int | float, int | float] for"
                + f" {self.__class__.__name__}.score_range but got"
                + f" {type(value).__name__} instead"
            )

        if not all(isinstance(item, (int, float)) for item in value):
            raise TypeError(
                "expected type int | float for"
                + f" {self.__class__.__name__}.score_range elements but got"
                + f" {type(value).__name__} instead"
            )

        self._score_range = value

    @property
    def value(self) -> int | float:
        """Get current value.

        Returns:
            int | float: current value.
        """
        return self._value

    @value.setter
    def value(self, value: int | float) -> None:
        """Set current value.

        Args:
            value (int | float): current value.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type int | float for"
                + f" {self.__class__.__name__}.value but got"
                + f" {type(value).__name__} instead"
            )

        self._value = value

    @property
    def inverse(self) -> bool:
        """Get inverse operation flag.

        Returns:
            bool: inverse operation flag.
        """
        return self._inverse

    @inverse.setter
    def inverse(self, value: bool) -> None:
        """Set inverse operation flag.

        Args:
            value (bool): inverse operation flag.
        """
        if not isinstance(value, bool):
            raise TypeError(
                "expected type bool for"
                + f" {self.__class__.__name__}.inverse but got"
                + f" {type(value).__name__} instead"
            )

        self._inverse = value

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
