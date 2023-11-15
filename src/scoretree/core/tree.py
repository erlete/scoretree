from colorama import Style

from .formatter import Formatter
from .scores import Score, ScoreArea


class ScoreTree(Formatter):
    """Score tree generation class.

    This class serves as interface for score tree generation. By providing the
    levels attribute with a list of Score and/or ScoreArea instances (last ones
    being nestable), all dependent scores will be computed and displayed with
    ease.

    Attributes:
        levels (list[Score | ScoreArea]): list of Score or ScoreArea items.
    """

    def __init__(self, levels: list[Score | ScoreArea]) -> None:
        """Initialize a ScoreTree instance.

        Args:
            levels (list[Score | ScoreArea]): list of Score or ScoreArea items.
        """
        self.levels = levels

    @property
    def levels(self) -> list[Score | ScoreArea]:
        """Get score levels.

        Returns:
            list[Score | ScoreArea]: score levels.
        """
        return self._levels

    @levels.setter
    def levels(self, value: list[Score | ScoreArea]) -> None:
        """Set score levels.

        Raises:
            TypeError: if value is not a list.
            TypeError: if value contains elements that are not Score or
                ScoreArea instances.

        Args:
            value (list[Score | ScoreArea]): score levels.
        """
        if not isinstance(value, list):
            raise TypeError(
                "expected type list[Score | ScoreArea] for"
                + f" {self.__class__.__name__}.levels but got"
                + f" {type(value).__name__} instead"
            )

        if not all(isinstance(item, (Score, ScoreArea)) for item in value):
            raise TypeError(
                "expected type list[Score | ScoreArea] for"
                + f" {self.__class__.__name__}.levels elements but got"
                + f" {type(value).__name__} instead"
            )

        # Weight completeness checking:
        for area in value:
            self.check_weights(area)

        self._levels = value

    @classmethod
    def check_weights(cls, area: ScoreArea) -> None:
        """Check if weights of a ScoreArea add up to 1.

        Args:
            area (ScoreArea): ScoreArea to check.

        Raises:
            ValueError: if weights do not add up to 1.
        """
        # Accumulation:
        total = 0
        for item in area.items:
            total += item.weight

            # Recursive checking:
            if isinstance(item, ScoreArea):
                cls.check_weights(item)

        if total != 1:
            raise ValueError(
                f"\"{area.name}\" score weights do not add up to 1 ({total})"
            )

    def __repr__(self) -> str:
        """Get short string representation of the score tree.

        Returns:
            str: short string representation of the score tree.
        """
        return f"<ScoreTree with {len(self.levels)} levels>"

    def __str__(self) -> str:
        """Get long representation of the score tree.

        Returns:
            str: long representation of the score tree.
        """
        return "\n".join(
            self.colorize(
                f"{Style.BRIGHT}{level.name.title()}"
                + f" ({level.weight * 100:.2f}%):"
                + f"{level._computed * 100:.2f}%\n"
                + f"\n".join(
                    item._render()
                    for item in level.items
                ) + Style.RESET_ALL,
                level._computed
            )
            for level in self.levels
        )
