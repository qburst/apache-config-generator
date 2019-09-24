
import sys


class ColouredSysOut(object):
    """
    Class for make the sys out colorful
    """
    ANSI_COLOR_START = {
        'blue': '\033[34m', # Blue Ansi
        'yellow': '\033[33m', #Yellow
        'red': '\033[1;31m', #Bold red
        'default': '\u001b[37m' #White
    }

    ANSI_COLOR_END = '\033[0m'

    @classmethod
    def log_message(cls, message, color):
        """
        Method to change the color of the log based on the input
        @params cls: Class
        @params message: Message to show
        @params color: Color of the message
        @return None
        @prints Sys out message in specified color
        """
        color_start = cls.ANSI_COLOR_START.get(color, cls.ANSI_COLOR_START.get("default"))
        colored_message = f"\n{color_start}{message}{cls.ANSI_COLOR_END}\n"
        sys.stdout.write(colored_message)
