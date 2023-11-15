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

        Raises:
            TypeError: if count is not an integer.

        Returns:
            str: indented string.
        """
        if not isinstance(count, int):
            raise TypeError("count must be an integer.")

        count = max(0, count)  # Value normalization.

        if count == 1:
            return (
                f"{cls.START_CHAR}{cls.MIDDLE_CHAR * 2} "
            )

        return (
            " " * 4 * (count - 1)
            + f"{cls.START_CHAR}{cls.MIDDLE_CHAR * 2} "
        )

    @classmethod
    def colorize(cls, text: str, value: int | float) -> str:
        """Colorize text based on a value.

        Args:
            text (str): text to colorize.
            value (int | float): value to base colorization from 0 to 1 (both
                included).

        Raises:
            TypeError: if text is not a string.
            TypeError: if value is not an integer or float.
            ValueError: if value is not between 0 and 1.

        Returns:
            str: colorized text.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string.")

        if not isinstance(value, (int, float)):
            raise TypeError("value must be an integer or float.")

        if not 0 <= value <= 1:
            raise ValueError("value must be between 0 and 1.")

        return {
            value < .5: Fore.RED,
            .5 <= value <= .75: Fore.YELLOW,
            .75 < value: Fore.GREEN
        }[True] + text
