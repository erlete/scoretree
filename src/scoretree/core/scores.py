from __future__ import annotations

from colorama import Style

from .formatter import Formatter


class Score(Formatter):
    """Minimal score representation unit.

    This class represents the smallest score unit, which contains a name, a
    weight for ponderation, a score range that defines the evaluation range and
    a value. Furthermore, the computation can be inverted, for example, if the
    score range is from 0 to 10, a value of 10 will be 0 and a value of 0 will
    be 1. This is useful for scores that are better when lower, like distance
    to end.

    Attributes:
        name (str): score name.
        weight (float): score weight.
        score_range (tuple[float, float]): score range from
            minimum to maximum.
        value (float, optional): current value. Defaults to 0.
        inverse (bool, optional): whether to invert the score calculation
            process. Defaults to False.
    """

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
            score_range (tuple[int | float, int | float]): score range from
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

        Raises:
            TypeError: if value is not a string.

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
    def weight(self) -> float:
        """Get score weight.

        Returns:
            float: score weight.
        """
        return self._weight

    @weight.setter
    def weight(self, value: int | float) -> None:
        """Set score weight.

        Raises:
            TypeError: if value is not an int or float.

        Args:
            value (int | float): score weight.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type int | float for"
                + f" {self.__class__.__name__}.weight but got"
                + f" {type(value).__name__} instead"
            )

        self._weight = float(value)

    @property
    def score_range(self) -> tuple[float, float]:
        """Get score range.

        Returns:
            tuple[float, float]: score range.
        """
        return self._score_range

    @score_range.setter
    def score_range(self, value: tuple[int | float, int | float]) -> None:
        """Set score range.

        Raises:
            TypeError: if value is not a tuple.
            TypeError: if value elements are not int or float.
            ValueError: if value length is not 2.

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

        if not len(value) == 2:
            raise ValueError(
                "expected length 2 for"
                + f" {self.__class__.__name__}.score_range but got"
                + f" {len(value)} instead"
            )

        self._score_range = (float(value[0]), float(value[1]))

    @property
    def value(self) -> float:
        """Get current value.

        Returns:
            float: current value.
        """
        return self._value

    @value.setter
    def value(self, value: int | float) -> None:
        """Set current value.

        Raises:
            TypeError: if value is not an int or float.

        Args:
            value (int | float): current value.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type int | float for"
                + f" {self.__class__.__name__}.value but got"
                + f" {type(value).__name__} instead"
            )

        self._value = float(value)

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

        Raises:
            TypeError: if value is not a bool.

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

    def _compute_score(self) -> None:
        """Compute score value from current value, weight and score range."""
        # Compute score and invert it, if specified:
        self._computed = abs(self._inverse - (
            min(
                self._value - self._score_range[0],
                self._score_range[1] - self._score_range[0]
            ) / (self._score_range[1] - self._score_range[0])
        ))

        # Normalize score:
        self._computed = min(1, max(self._computed, 0))

    def _render(self, indent: int = 1) -> str:
        """Render formatted score.

        Args:
            indent (int, optional): indentation level. Defaults to 1.

        Returns:
            str: formatted score.
        """
        return self.colorize(
            f"{Style.DIM}{self.indent(indent)}{self!s}",
            self._computed
        )

    def __repr__(self) -> str:
        """Get short representation of the score.

        Returns:
            str: short representation of the score.
        """
        return f"Score({self.name})"

    def __str__(self) -> str:
        """Get long representation of the score.

        Returns:
            str: long representation of the score.
        """
        return (
            f"{self.name.title()} ({self.weight * 100:.2f}%):"
            + f" {self._computed * 100:.2f}%"
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

    def _render(self, indent=1):
        return self.colorize(
            Style.NORMAL
            + f"{self.indent(indent)}{self.name.title()} ({self.weight * 100:.2f}%): {self._computed * 100:.2f}%\n"
            + f"\n".join(
                item._render(indent + 1)
                for item in self.scores
            ),
            self._computed
        )
