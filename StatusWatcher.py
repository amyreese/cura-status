import sys

from UM.Application import Application #To register the information dialogue.
from UM.Event import Event #To understand what events to react to.
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry #To find the QML files in the plug-in folder.
from UM.Scene.Selection import Selection #To get the current selection and some information about it.
from UM.Tool import Tool #The PluginObject we're going to extend.

class StatusWatcher(Tool): #The Tool class extends from PluginObject, and we have to be a PluginObject for the plug-in to load.
    ##  Creates an instance of this tool.
    #
    #   Here you can set some additional metadata.
    def __init__(self):
        super().__init__()

        self._shortcut_key = None

        #This plug-in creates a window with information about the objects we've selected. That window is lazily-loaded.
        self.info_window = None

        Logger.log("i", "Python version %s" % (sys.version_info(), ))

    ##  Called when something happens in the scene while our tool is active.
    #
    #   For instance, we can react to mouse clicks, mouse movements, and so on.
    def event(self, event):
        super().event(event)

        Logger.log("i", "event received: %s" % (event, ))
