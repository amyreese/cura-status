import sys
import textwrap
import unittest
from pathlib import Path
from typing import Iterable, Union

from UM.Logger import Logger
from UM.Extension import Extension
from UM.Qt.Duration import Duration

from cura.CuraApplication import CuraApplication
from PyQt5.QtCore import QTimer


def duration_text(duration: Union[Duration, int]) -> str:
    if isinstance(duration, int):
        days, hours, minutes, = 0, 0, 0
        seconds = duration

        while seconds > 86400:
            days += 1
            seconds -= 86400

        while seconds > 3600:
            hours += 1
            seconds -= 3600

        while seconds > 60:
            minutes += 1
            seconds -= 60

    elif isinstance(duration, Duration) and duration.valid:
        days, hours, minutes, seconds = (
            duration.days,
            duration.hours,
            duration.minutes,
            duration.seconds,
        )

    else:
        return ""

    if days <= 0 and hours <= 0 and minutes <= 0 and seconds <= 0:
        return ""

    if days > 0:
        tpl = "{days}:{hours:02}:{minutes:02}:{seconds:02}"
    else:
        tpl = "{hours}:{minutes:02}:{seconds:02}"

    return tpl.format(days=days, hours=hours, minutes=minutes, seconds=seconds,)

    return ""


class StatusWatcher(Extension):
    def __init__(self, application: CuraApplication):
        super().__init__()

        self._app = application
        self._path = Path(
            "~/cura-print-status.txt"
        ).expanduser()  # should be configurable 🤷‍♀️
        self._path.write_text("\n")

        self._timer = QTimer()
        self._timer.timeout.connect(self.dump_status)
        self._timer.start(15000)

    def dump_status(self):
        try:
            job_name = ""
            total_time = ""
            elapsed_time = ""
            remaining_time = ""

            info = self._app.getPrintInformation()
            if info is not None:
                job_name = info.jobName
                total_time = duration_text(info.currentPrintTime)

            devices = self._app.getMachineManager().printerOutputDevices
            if devices:
                printer = devices[0].activePrinter
                if printer is not None:
                    job = printer.activePrintJob
                    if job is not None:
                        total_time = duration_text(job.timeTotal)
                        elapsed_time = duration_text(job.timeElapsed)
                        remaining_time = duration_text(job.timeTotal - job.timeElapsed)

            content = """
                Job Name: {job_name}
                Total Time: {total_time}
                Elapsed: {elapsed_time}
                Remaining: {remaining_time}
            """.format(
                job_name=job_name,
                total_time=total_time,
                elapsed_time=elapsed_time,
                remaining_time=remaining_time,
            )
            self._path.write_text(textwrap.dedent(content))

            if self._timer.interval() > 1000:
                self._timer.setInterval(1000)

        except Exception as e:
            Logger.log("w", "failed to write status file: {}".format(e))


class StatusTest(unittest.TestCase):
    def test_duration_text(self):
        pairs = [
            (45, "0:00:45"),
            (145, "0:02:25"),
            (3145, "0:52:25"),
            (3845, "1:04:05"),
            (7845, "2:10:45"),
        ]

        for value, expected in pairs:
            with self.subTest((value, expected)):
                self.assertEqual(duration_text(value), expected)


if __name__ == "__main__":
    unittest.main()
