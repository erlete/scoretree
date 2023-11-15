"""Score classes module.

This module contains the Score and ScoreArea classes, which are used to
represent a score and a score area, respectively. The Score class is the
smallest score unit, containing a name, a weight for ponderation, a score range
that defines the evaluation range and a value. The ScoreArea class is a score
area, which contains a name, a weight for ponderation and a list of scores or
score areas.

Author:
    Paulo Sanchez (@erlete)
"""


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
        score (float): score.
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

        Raises:
            TypeError: if value is not a string.
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

        Args:
            value (int | float): score weight.

        Raises:
            TypeError: if value is not an int or float.
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

        Args:
            value (tuple[int | float, int | float]): score range.

        Raises:
            TypeError: if value is not a tuple.
            TypeError: if value elements are not int or float.
            ValueError: if value length is not 2.
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

        Args:
            value (int | float): current value.

        Raises:
            TypeError: if value is not an int or float.
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

        Args:
            value (bool): inverse operation flag.

        Raises:
            TypeError: if value is not a bool.
        """
        if not isinstance(value, bool):
            raise TypeError(
                "expected type bool for"
                + f" {self.__class__.__name__}.inverse but got"
                + f" {type(value).__name__} instead"
            )

        self._inverse = value

    @property
    def score(self) -> float:
        """Get score.

        Returns:
            float: score.
        """
        # Compute score, invert it (if specified) and normalize it:
        return min(1, max(abs(
            self._inverse - (min(
                self._value - self._score_range[0],
                self._score_range[1] - self._score_range[0]
            ) / (self._score_range[1] - self._score_range[0]))
        ), 0))

    def _render(self, indent: int = 1) -> str:
        """Render formatted score.

        Args:
            indent (int, optional): indentation level. Defaults to 1.

        Returns:
            str: formatted score.

        Raises:
            TypeError: if indent is not an integer.
        """
        if not isinstance(indent, int):
            raise TypeError("indent must be an integer")

        indent = max(0, indent)  # Value normalization.

        return self.colorize(
            f"{Style.DIM}{self.indent(indent)}{self!s}"
            if Formatter.COLOR_ENABLED else f"{self.indent(indent)}{self!s}",
            self.score
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
            + f" {self.score * 100:.2f}%"
        )


class ScoreArea(Formatter):
    """Score area representation unit.

    The score area represents a set of scores or child score areas that can be
    used to group scores by level or category. It contains a name, a weight for
    ponderation and a list of scores or score areas.

    Attributes:
        name (str): score area name.
        weight (float): score area weight.
        items (list[Score | ScoreArea]): score area items (can either be
            Score or ScoreArea instances).
        score (float): weighted score.
    """

    def __init__(
        self,
        name: str,
        weight: int | float,
        items: list[Score | ScoreArea]
    ) -> None:
        """Initialize a ScoreArea instance.

        Args:
            name (str): score area name.
            weight (int | float): score area weight.
            items (list[Score | ScoreArea]): score area items (can either be
                Score or ScoreArea instances).
        """
        self.name = name
        self.weight = weight
        self.items = items

    @property
    def name(self) -> str:
        """Get score area name.

        Returns:
            str: score area name.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set score area name.

        Args:
            value (str): score area name.

        Raises:
            TypeError: if value is not a string.
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
        """Get score area weight.

        Returns:
            float: score area weight.
        """
        return self._weight

    @weight.setter
    def weight(self, value: int | float) -> None:
        """Set score area weight.

        Args:
            value (int | float): score area weight.

        Raises:
            TypeError: if value is not an int or float.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type int | float for"
                + f" {self.__class__.__name__}.weight but got"
                + f" {type(value).__name__} instead"
            )

        self._weight = float(value)

    @property
    def items(self) -> list[Score | ScoreArea]:
        """Get score area items.

        Returns:
            list[Score | ScoreArea]: score area items.
        """
        return self._items

    @items.setter
    def items(self, value: list[Score | ScoreArea]) -> None:
        """Set score area items.

        Args:
            value (list[Score | ScoreArea]): score area items.

        Raises:
            TypeError: if value is not a list.
            TypeError: if value elements are not Score or ScoreArea instances.
        """
        if not isinstance(value, list):
            raise TypeError(
                "expected type list[Score | ScoreArea] for"
                + f" {self.__class__.__name__}.items but got"
                + f" {type(value).__name__} instead"
            )

        if not all(isinstance(item, (Score, ScoreArea)) for item in value):
            raise TypeError(
                "expected type Score | ScoreArea for"
                + f" {self.__class__.__name__}.items elements but got"
                + f" {type(value).__name__} instead"
            )

        self._items = value

    @property
    def score(self) -> float:
        """Get weighted score.

        Returns:
            float: weighted score.
        """
        return sum(item.score * item._weight for item in self.items)

    def _render(self, indent: int = 1) -> str:
        """Render formatted score area.

        Args:
            indent (int, optional): indentation level. Defaults to 1.

        Returns:
            str: formatted score area.

        Raises:
            TypeError: if indent is not an integer.
        """
        if not isinstance(indent, int):
            raise TypeError("indent must be an integer")

        indent = max(0, indent)  # Value normalization.

        return self.colorize(
            (
                Style.NORMAL
                + f"{self.indent(indent)}{self.name.title()}"
                + f" ({self.weight * 100:.2f}%): {self.score * 100:.2f}%\n"
                + f"\n".join(
                    item._render(indent + 1)
                    for item in self.items
                )
            ) if Formatter.COLOR_ENABLED else (
                f"{self.indent(indent)}{self.name.title()}"
                + f" ({self.weight * 100:.2f}%): {self.score * 100:.2f}%\n"
                + f"\n".join(
                    item._render(indent + 1)
                    for item in self.items
                )
            ), self.score
        )

    def __repr__(self) -> str:
        """Get short representation of the score area.

        Returns:
            str: short representation of the score area.
        """
        return f"ScoreArea({self.name})"

    def __str__(self) -> str:
        """Get long representation of the score area.

        Returns:
            str: long representation of the score area.
        """
        return (
            f"{self.name.title()} ({self.weight * 100:.2f}%):"
            + f" {self.score * 100:.2f}%\n"
            + "\n".join(f"{' ' * 4}{item!s}" for item in self.items)
        )
