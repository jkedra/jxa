import time
import math


def time_sec():
    return int(time.time())


class Progress:
    """
    Progress reporting.

    Usage:
    from jxa.Progress import Progress
    from time import sleep
    p = Progress(frequency=4)
    max = 9000_000
    for i in range(0,max,1000):
        sleep(1/300)
        p.print(i,max)
    p.print_final()

    """
    def __init__(self, frequency) -> None:
        """

        :param frequency: display frequency in seconds
        """
        self.last_progress = time_sec()
        self.frequency = frequency

    @staticmethod
    def human_readable_byte_count(bytes, si: bool = False):
        unit = 1000 if si else 1024
        if bytes < unit:
            return f"{bytes} B"

        exp = int(math.log(bytes) // math.log(unit))
        pre = ("kMGTPE" if si else "KMGTPE")[exp - 1]
        pre += ("" if si else "i")
        return "{:.1f} {}B".format(bytes / math.pow(unit, exp), pre)

    def print(self, sofar: int, total: int,
              line_prefix: str = "Downloaded",
              final: bool = False):
        """
        Call it each time the progress feedback is required.

        The feedback is printed only each self.frequency seconds.

        :param sofar: bytes so far processed
        :param total: sum of all bytes
        :param line_prefix: eg. downloaded, uploaded, processed
        :param final:
        :return: Nothing
        """
        if self.frequency != 0 and not final:
            next_progress_time = self.last_progress + self.frequency
            if time_sec() < next_progress_time:
                return
            else:
                self.last_progress = time_sec()

        print("{} {} ({:.0f}%)".format(
            line_prefix,
            Progress.human_readable_byte_count(sofar),
            sofar / total * 100))

    def print_final(self, *args, **kwargs):
        """
        Prints feedback unconditionally.

        To be called after the main loop exists.
        """
        kwargs['final'] = True
        self.print(*args, **kwargs)
