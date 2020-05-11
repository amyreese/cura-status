import sys

from UM.Application import Application
from UM.Event import Event #To understand what events to react to.
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry #To find the QML files in the plug-in folder.
from UM.Scene.Selection import Selection #To get the current selection and some information about it.
from UM.Extension import Extension

from cura.CuraApplication import CuraApplication
from cura.UI.PrintInformation import PrintInformation
from PyQt5.QtCore import QTimer

class StatusWatcher(Extension):
    def __init__(self, application: CuraApplication):
        super().__init__()

        self._app = application

        Logger.log("i", "Python version: %s" % (sys.version_info, ))
        Logger.log("i", "Cura app: %s" % (self._app, ))

        self._timer = QTimer()
        self._timer.timeout.connect(self.dump_status)
        self._timer.start(1000)

    def dump_status(self):
        pi = self._app.getPrintInformation()
        if pi is not None:
            dur = pi.currentPrintTime
            if dur.valid:
                Logger.log("i", "print time: %s" % (dur.getDisplayString(), ))
