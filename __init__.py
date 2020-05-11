# Copyright (c) 2017 Ultimaker B.V.
# This example is released under the terms of the AGPLv3 or higher.

from . import StatusWatcher

##  Defines additional metadata for the plug-in.
#
#   Tool plug-ins can have a button in the interface. This has some metadata
#   that describes the tool and provides an image.
def getMetaData():
    return {
        "tool": {
            "name": "Status Watcher",
            "description": "Watch the status",
            "icon": "magnifying_glass.svg",
        }
    }

##  Lets Uranium know that this plug-in exists.
#
#   This is called when starting the application to find out which plug-ins
#   exist and what their types are. We need to return a dictionary mapping from
#   strings representing plug-in types (in this case "tool") to objects that
#   inherit from PluginObject.
#
#   \param app The application that the plug-in needs to register with.
def register(app):
    return {"extension": StatusWatcher.StatusWatcher(app)}