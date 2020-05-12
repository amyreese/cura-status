import sys
import textwrap
from pathlib import Path
from typing import Iterable, Union

from UM.Application import Application
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry
from UM.Extension import Extension
from UM.Qt.Duration import Duration

from cura.CuraApplication import CuraApplication
from cura.UI.PrintInformation import PrintInformation
from cura.Settings.MachineManager import MachineManager
from PyQt5.QtCore import QTimer


def duration_text(duration: Union[Duration, int]) -> str:
    if isinstance(duration, int):
        days, hours, minutes, = 0, 0, 0
        seconds = duration

        while seconds > 86400:
            days += 1
            seconds -= 86400

        while hours > 3600:
            hours += 1
            seconds -= 3600

        while minutes > 60:
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


def write_lines(lines: Iterable[str], path: Path):
    content = "\n".join(lines) + "\n"
    path.write_text(content)


class StatusWatcher(Extension):
    def __init__(self, application: CuraApplication):
        super().__init__()

        self._app = application
        self._path = Path(
            "~/cura-print-status.txt"
        ).expanduser()  # should be configurable 🤷‍♀️

        self._timer = QTimer()
        self._timer.timeout.connect(self.dump_status)
        self._timer.start(1000)

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
                printer = printers[0].activePrinter
                if printer is not None:
                    job = printer.activePrintJob
                    if job is not None:
                        elapsed_time = duration_text(job.timeElapsed)
                        remaining_time = duration_text(job.timeRemaining)

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

        except Exception as e:
            Logger.log("w", "failed to write status file: {}".format(e))
