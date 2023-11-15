from colorama import Style

from .formatter import Formatter
from .scores import Score, ScoreArea


class ScoreTree(Formatter):

    def __init__(self, levels: list[ScoreArea]):
        self.levels = levels

    @property
    def levels(self):
        return self._levels

    @levels.setter
    def levels(self, value):
        for area in value:
            self.check_weights(area)

        self._levels = value

    @classmethod
    def check_weights(cls, area):
        total = 0
        for item in area.scores:
            total += item.weight

            if isinstance(item, ScoreArea):
                cls.check_weights(item)

        if total != 1:
            raise ValueError(
                f"\"{area.name}\" score weights do not add up to 1 ({total})"
            )

    def __repr__(self):
        return f"<ScoreTree with {len(self.levels)} levels>"

    def __str__(self):
        return "\n".join(
            self.colorize(
                Style.BRIGHT
                + f"{level.name.title()} ({level.weight * 100:.2f}%): {level._computed * 100:.2f}%\n"
                + f"\n".join(
                    item._render()
                    for item in level.scores
                )
                + Style.RESET_ALL,
                level._computed
            )
            for level in self.levels
        )
