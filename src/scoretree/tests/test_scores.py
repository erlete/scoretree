import pytest
from colorama import Fore, Style

from ..core.scores import Score, ScoreArea


class TestScore:

    def test_init(self):
        Score("", 0, (0, 0))
        Score("", 0, (0, 0), 0)
        Score("", 0, (0, 0), 0)
        Score("", 0, (0, 0), 0, False)

    def test_properties(self):
        score = Score("test", 0, (0, 1))

        assert score.name == "test"
        assert score.weight == 0
        assert score.score_range == (0, 1)
        assert score.value == 0
        assert not score.inverse

        score.name = "test2"
        with pytest.raises(TypeError):
            score.name = 0
            score.name = 0.0
            score.name = None
            score.name = []

        score.weight = 1
        score.weight = 1.0
        with pytest.raises(TypeError):
            score.weight = "0"
            score.weight = None
            score.weight = []

        score.score_range = (0, 1)
        score.score_range = (0.0, 1.0)
        with pytest.raises(TypeError):
            score.score_range = "0"
            score.score_range = None
            score.score_range = []
            score.score_range = [0, 0]

        with pytest.raises(TypeError):
            score.score_range = (0, "a")
            score.score_range = ("a", 0)
            score.score_range = ("1", "0")

        with pytest.raises(ValueError):
            score.score_range = ()
            score.score_range = (0,)
            score.score_range = (0, 0, 0)

        score.value = 1
        score.value = 1.0
        with pytest.raises(TypeError):
            score.value = "0"
            score.value = None
            score.value = []

        score.inverse = True
        score.inverse = False
        with pytest.raises(TypeError):
            score.inverse = 0
            score.inverse = 0.0
            score.inverse = "0"
            score.inverse = None
            score.inverse = []
            score.inverse = ()

        score.score_range = (0, 1)
        score.value = 0.5
        assert score.score == 0.5

    def test_representation(self):
        score = Score("test", 0, (0, 1))

        assert repr(score) == "Score(test)"
        assert str(score) == "Test (0.00%): 0.00%"

        assert score._render(0) == (
            f"{Fore.RED}{Style.DIM}Test (0.00%): 0.00%"
        )
        assert score._render(1) == score._render() == (
            f"{Fore.RED}{Style.DIM}└── Test (0.00%): 0.00%"
        )

        with pytest.raises(TypeError):
            score._render("0")
            score._render(None)
            score._render([])
            score._render(())


class TestScoreArea:

    def test_init(self):
        ScoreArea("", 0, [])
        ScoreArea("", 0, [Score("", 0, (0, 1))])

    def test_properties(self):
        score_area = ScoreArea("test", 0, [])

        assert score_area.name == "test"
        assert score_area.weight == 0
        assert score_area.items == []

        score_area.name = "test2"
        with pytest.raises(TypeError):
            score_area.name = 0
            score_area.name = 0.0
            score_area.name = None
            score_area.name = []

        score_area.weight = 1
        score_area.weight = 1.0
        with pytest.raises(TypeError):
            score_area.weight = "0"
            score_area.weight = None
            score_area.weight = []

        score_area.items = []
        score_area.items = [Score("", 0, (0, 1))]
        score_area.items = [Score("", 0, (0, 1)), Score("", 0, (0, 1))]
        score_area.items = [ScoreArea("", 0, [])]
        score_area.items = [ScoreArea("", 0, []), ScoreArea("", 0, [])]
        score_area.items = [Score("", 0, (0, 1)), ScoreArea("", 0, [])]
        with pytest.raises(TypeError):
            score_area.items = 0
            score_area.items = 0.0
            score_area.items = ""
            score_area.items = None
            score_area.items = ()

        with pytest.raises(TypeError):
            score_area.items = [0]
            score_area.items = [0.0]
            score_area.items = [""]
            score_area.items = [None]
            score_area.items = [()]

        score_area.weight = 1
        score_area.items = [Score("", 1, (0, 1), 1)]

        assert score_area.score == 1

    def test_representation(self):
        score_area = ScoreArea("test", 1, [Score("test1", 1, (0, 1), 1)])

        assert repr(score_area) == "ScoreArea(test)"
        assert str(score_area) == (
            "Test (100.00%): 100.00%\n    Test1 (100.00%): 100.00%"
        )

        assert score_area._render(0) == (
            f"{Fore.GREEN}{Style.NORMAL}Test (100.00%): 100.00%\n"
            + f"{Fore.GREEN}{Style.DIM}└── Test1 (100.00%): 100.00%"
        )
        assert score_area._render(1) == score_area._render() == (
            f"{Fore.GREEN}{Style.NORMAL}└── Test (100.00%): 100.00%\n"
            + f"{Fore.GREEN}{Style.DIM}    └── Test1 (100.00%): 100.00%"
        )

        with pytest.raises(TypeError):
            score_area._render("0")
            score_area._render(None)
            score_area._render([])
            score_area._render(())
