"""Score tree module.

This module contains the ScoreTree class, which is used to generate a score
tree from a list of Score and/or ScoreArea instances.

Author:
    Paulo Sanchez (@erlete)
"""


from __future__ import annotations

from colorama import Style

from .formatter import Formatter
from .scores import Score, ScoreArea


class ScoreTree(Formatter):
    """Score tree generation class.

    This class serves as interface for score tree generation. By providing the
    items attribute with a list of Score and/or ScoreArea instances (last ones
    being nestable), all dependent scores will be computed and displayed with
    ease.

    Attributes:
        items (list[Score | ScoreArea]): list of Score or ScoreArea items.
        score (float): weighted score.
    """

    def __init__(self, items: list[Score | ScoreArea]) -> None:
        """Initialize a ScoreTree instance.

        Args:
            items (list[Score | ScoreArea]): list of Score or ScoreArea items.
        """
        self.items = items

    @property
    def items(self) -> list[Score | ScoreArea]:
        """Get score items.

        Returns:
            list[Score | ScoreArea]: score items.
        """
        return self._items

    @items.setter
    def items(self, value: list[Score | ScoreArea]) -> None:
        """Set score items.

        Args:
            value (list[Score | ScoreArea]): score items.

        Raises:
            TypeError: if value is not a list.
            TypeError: if value contains elements that are not Score or
                ScoreArea instances.
        """
        if not isinstance(value, list):
            raise TypeError(
                "expected type list[Score | ScoreArea] for"
                + f" {self.__class__.__name__}.items but got"
                + f" {type(value).__name__} instead"
            )

        if not all(isinstance(item, (Score, ScoreArea)) for item in value):
            raise TypeError(
                "expected type list[Score | ScoreArea] for"
                + f" {self.__class__.__name__}.items elements but got"
                + f" {type(value).__name__} instead"
            )

        self._items = value

        # Weight completeness self-checking:
        self.check_weights(self)

    @property
    def score(self) -> float:
        """Get weighted score.

        Returns:
            float: weighted score.
        """
        return sum(level.score * level.weight for level in self.items)

    @classmethod
    def check_weights(cls, score_collection: ScoreArea | ScoreTree) -> None:
        """Check if weights of a ScoreArea or ScoreTree add up to 1.

        Args:
            score_collection (ScoreArea | ScoreTree): score area or score tree
                to check.

        Raises:
            ValueError: if weights do not add up to 1.
        """
        # Accumulation:
        total = 0
        for item in score_collection.items:
            total += item.weight

            # Recursive checking:
            if isinstance(item, ScoreArea):
                cls.check_weights(item)

        # Score area checking:
        if total != 1 and isinstance(score_collection, ScoreArea):
            raise ValueError(
                f"\"{score_collection.name}\""
                + f" score weights do not add up to 1 ({total})"
            )

        # Score tree checking:
        elif total != 1 and isinstance(score_collection, ScoreTree):
            raise ValueError(
                f"score tree weights do not add up to 1 ({total})"
            )

    def __repr__(self) -> str:
        """Get short string representation of the score tree.

        Returns:
            str: short string representation of the score tree.
        """
        return f"<ScoreTree with {len(self.items)} items>"

    def __str__(self) -> str:
        """Get long representation of the score tree.

        Returns:
            str: long representation of the score tree.
        """
        return "\n".join(
            self.colorize(
                f"{Style.BRIGHT}{level.name.title()}"
                + f" ({level.weight * 100:.2f}%):"
                + f" {level.score * 100:.2f}%\n"
                + f"\n".join(
                    item._render()
                    for item in level.items
                ) + Style.RESET_ALL,
                level.score
            )
            for level in self.items
        )
