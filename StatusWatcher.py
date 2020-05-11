import sys
from pathlib import Path
from typing import Iterable

from UM.Application import Application
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry
from UM.Extension import Extension
from UM.Qt.Duration import Duration

from cura.CuraApplication import CuraApplication
from cura.UI.PrintInformation import PrintInformation
from PyQt5.QtCore import QTimer


def duration_text(duration: Duration) -> str:
    if duration.valid:
        days, hours, minutes, seconds = (
            duration.days,
            duration.hours,
            duration.minutes,
            duration.seconds,
        )

        if days <= 0 and hours <= 0 and minutes <= 0 and seconds <= 0:
            return ""

        if days > 0:
            tpl = "{days}:{hours:02}:{minutes:02}:{seconds:02}"
        else:
            tpl = "{hours}:{minutes:02}:{seconds:02}"

        return tpl.format(days=days, hours=hours, minutes=minutes, seconds=seconds,)

    return ""


def print_text(lines: Iterable[str], path: Path):
    content = "\n".join(lines) + "\n"
    path.write_text(content)


class StatusWatcher(Extension):
    def __init__(self, application: CuraApplication):
        super().__init__()

        self._app = application
        self._short = Path(
            "~/cura-print-short.txt"
        ).expanduser()  # should be configurable 🤷‍♀️
        self._long = Path(
            "~/cura-print-long.txt"
        ).expanduser()  # should be configurable 🤷‍♀️

        self._timer = QTimer()
        self._timer.timeout.connect(self.dump_status)
        self._timer.start(1000)

    def dump_status(self):
        try:
            short = []
            long = []

            info = self._app.getPrintInformation()
            if info is not None:
                short.append("Job Name: {}".format(info.jobName))

                duration = duration_text(info.currentPrintTime)
                short.append("Print Time: {}".format(duration))

            print_text(short, self._short)

            if info is not None:
                for key, value in sorted(info.getFeaturePrintTimes().items()):
                    if value.valid:
                        duration = duration_text(value)
                        long.append("  {}: {}".format(key, duration))

            print_text(short + long, self._long)

        except Exception as e:
            Logger.log("w", "failed to write status file: {}".format(e))
