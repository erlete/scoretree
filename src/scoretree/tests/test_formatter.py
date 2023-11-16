import pytest
from colorama import Fore

from ..core.formatter import Formatter


class TestFormatter:

    def test_indent(self):
        assert 1 == 2
        with pytest.raises(TypeError):
            Formatter.indent(1.1)
            Formatter.indent("1")
            Formatter.indent(True)

        assert Formatter.indent(-1) == ""
        assert Formatter.indent(0) == ""
        assert Formatter.indent(1) == (
            f"{Formatter.START_CHAR}{Formatter.MIDDLE_CHAR * 2} "
        )
        assert Formatter.indent(2) == (
            f"{' ' * 4}{Formatter.START_CHAR}{Formatter.MIDDLE_CHAR * 2} "
        )

    def test_colorize(self):
        with pytest.raises(TypeError):
            Formatter.colorize(1, 0)
            Formatter.colorize(1.1, 0)
            Formatter.colorize([1, 2, 3], 0)

        with pytest.raises(TypeError):
            Formatter.colorize("", "1")
            Formatter.colorize("", [1, 2, 3])

        assert Formatter.colorize("red", 0) == f"{Fore.RED}red"
        assert Formatter.colorize("red", 0.49) == f"{Fore.RED}red"
        assert Formatter.colorize("yellow", 0.5) == f"{Fore.YELLOW}yellow"
        assert Formatter.colorize("yellow", 0.75) == f"{Fore.YELLOW}yellow"
        assert Formatter.colorize("green", 0.76) == f"{Fore.GREEN}green"
        assert Formatter.colorize("green", 1) == f"{Fore.GREEN}green"
