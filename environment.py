import os
import getpass
import launch_tools
from conda_git_deployment import utils

root_dir = os.path.dirname(__file__)

environments = [
    'ftrack_connect',
    'pyblish'
    ]

environment = launch_tools.pass_env(environments)
utils.write_environment(environment)


os.environ.setdefault('systemuser', getpass.getuser())
