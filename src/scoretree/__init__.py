"""ScoreTree package.

This package contains the ScoreTree class and its dependencies. It is used to
generate a score tree from a list of Score and/or ScoreArea instances,
providing with an easy to use, multi-level grade weighting system.

Author:
    Paulo Sanchez (@erlete)
"""


from .core.scores import Score, ScoreArea
from .core.tree import ScoreTree
