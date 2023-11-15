from colorama import Fore, init

init()


class Formatter:

    START_CHAR = "└"
    MIDDLE_CHAR = "─"

    @classmethod
    def indent(cls, count: int = 1):
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
    def colorize(cls, string, value):
        return {
            value < .5: Fore.RED,
            .5 <= value <= .75: Fore.YELLOW,
            .75 < value: Fore.GREEN
        }[True] + string
