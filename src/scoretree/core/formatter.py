from colorama import Fore, init

init()


class Formatter:
    """Formatting class.

    This class contains several methods used for string manipulation and
    formatting operations, such as indentation or colorization.

    Attributes:
        START_CHAR (str): character used to indicate start of a new line.
        MIDDLE_CHAR (str): character used to indicate continuation of a line.
    """

    START_CHAR = "└"
    MIDDLE_CHAR = "─"

    @classmethod
    def indent(cls, count: int = 1) -> str:
        """Generate an indentation string.

        Args:
            count (int, optional): number of indents. Defaults to 1.

        Returns:
            str: indented string.
        """
        count = max(0, count)  # Normalize value.

        if count == 1:
            return (
                f"{cls.START_CHAR}{cls.MIDDLE_CHAR * 2} "
            )

        return (
            " " * 4 * (count - 1)
            + f"{cls.START_CHAR}{cls.MIDDLE_CHAR * 2} "
        )

    @classmethod
    def colorize(cls, string: str, value: int) -> str:
        """Colorize a string based on a value.

        Args:
            string (str): string to colorize.
            value (int): value to base colorization on.

        Returns:
            str: colorized string.
        """
        return {
            value < .5: Fore.RED,
            .5 <= value <= .75: Fore.YELLOW,
            .75 < value: Fore.GREEN
        }[True] + string
