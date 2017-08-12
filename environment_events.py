import os
from conda_git_deployment import utils

root = os.path.dirname(__file__)

env = {}

# FTRACK_CONNECT_PLUGIN_PATH
env["FTRACK_CONNECT_PLUGIN_PATH"] = [
    os.path.join(root, "environment", "FTRACK_CONNECT_EVENTS")
]

# QT_PREFERRED_BINDING
env["QT_PREFERRED_BINDING"] = ["PySide2", "PySide"]

utils.write_environment(env)
