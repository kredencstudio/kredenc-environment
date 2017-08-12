import os
from conda_git_deployment import utils

root = os.path.dirname(__file__)

conda = os.environ['CONDA_GIT_REPOSITORY']

env = {}

# FTRACK_CONNECT_PLUGIN_PATH
env["FTRACK_CONNECT_PLUGIN_PATH"] = [
    os.path.join(conda, 'ftrack-kredenc-hooks', "server_events")
]

# QT_PREFERRED_BINDING
env["QT_PREFERRED_BINDING"] = ["PySide2", "PySide"]

utils.write_environment(env)
