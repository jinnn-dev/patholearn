class BgColors:
    """
    Definition of console colors
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ColoredPrinter:
    """
    Functions for printing highlighted text on the console.
    """

    @staticmethod
    def print_info(message: str):
        """
        Prints info text on warning level on the console.

        :param message: Message to be printed on the console
        """
        print(f"{BgColors.WARNING}{message}{BgColors.ENDC}")

    @staticmethod
    def print_lined_info(message: str):
        """
        Prints text on the console with entwined with lines.

        :param message: Message to be printed on the console
        """
        ColoredPrinter.print_info(f"----- {message} -----")
