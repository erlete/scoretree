import pytest
from colorama import Fore, Style

from ..core.scores import Score, ScoreArea
from ..core.tree import ScoreTree


class TestScoreTree:

    def test_init(self):
        ScoreTree([Score("test", 1, (0, 1))])
        ScoreTree([Score("test", 1, (0, 1))], False)

    def test_properties(self):
        score = Score("test", 1, (0, 1), 1)
        score_tree = ScoreTree([score])

        assert score_tree.items == [score]
        assert score_tree.colorized == True

        score_tree.items = [Score("test", 1, (0, 1))]
        score_tree.items = [
            Score("test", 0.5, (0, 1)),
            Score("test2", 0.5, (0, 1))
        ]
        score_tree.items = [
            ScoreArea("test", 1, [
                Score("test", 0.5, (0, 1)),
                Score("test2", 0.5, (0, 1))
            ])
        ]
        score_tree.items = [
            ScoreArea("test", 0.5, [
                Score("test", 0.5, (0, 1)),
                Score("test2", 0.5, (0, 1))
            ]),
            Score("test", 0.25, (0, 1)),
            Score("test2", 0.25, (0, 1))
        ]
        with pytest.raises(TypeError):
            score_tree.items = None
            score_tree.items = 0
            score_tree.items = 0.0
            score_tree.items = ""
            score_tree.items = ()

        with pytest.raises(TypeError):
            score_tree.items = [None]
            score_tree.items = [0]
            score_tree.items = [0.0]
            score_tree.items = [""]
            score_tree.items = [()]

        score_tree.colorized = True
        score_tree.colorized = False
        with pytest.raises(TypeError):
            score_tree.colorized = None
            score_tree.colorized = 0
            score_tree.colorized = 0.0
            score_tree.colorized = ""
            score_tree.colorized = ()

        score_tree.items = [Score("test", 1, (0, 1), 0.5)]
        assert score_tree.score == 0.5

    def test_check_score(self):
        with pytest.raises(ValueError):
            ScoreTree([])
            ScoreTree([Score("test", 0, (0, 1))])
            ScoreTree([Score("test", .5, (0, 1))])
            ScoreTree([Score("test", .99, (0, 1))])
            ScoreTree([Score("test", 1.01, (0, 1))])
            ScoreTree([Score("test", -1, (0, 1))])

        with pytest.raises(ValueError):
            ScoreTree([ScoreArea("test", 0, [])])
            ScoreTree([ScoreArea("test", .5, [])])
            ScoreTree([ScoreArea("test", .99, [])])
            ScoreTree([ScoreArea("test", 1.01, [])])
            ScoreTree([ScoreArea("test", -1, [])])

    def test_representation(self):
        score_tree = ScoreTree([
            Score("test", 0.5, (0, 1)),
            Score("test2", 0.5, (0, 1), .5)
        ])

        assert repr(score_tree) == "<ScoreTree with 2 items>"
        assert str(score_tree) == (
            f"{Fore.RED}{Fore.RED}{Style.DIM}Test (50.00%): 0.00%"
            + f"{Style.RESET_ALL}\n{Fore.YELLOW}{Fore.YELLOW}{Style.DIM}"
            + f"Test2 (50.00%): 50.00%{Style.RESET_ALL}"
        )
