import os
import getpass
import launch_tools
from conda_git_deployment import utils

root_dir = os.path.dirname(__file__)

environments = [
    'global',
    'ftrack_connect',
    'pyblish'
    ]


environment_start = {}
environment_start["STUDIO_REPOS"] = [os.path.join(r'\\kre-c01', 'share', 'core', 'repos')]
environment_start["STUDIO_SOFT"] = [os.path.join(r'\\kre-c01', 'share', 'core', 'software')]
utils.write_environment(environment_start)


environment = launch_tools.pass_env(environments)
utils.write_environment(environment)


os.environ.setdefault('systemuser', getpass.getuser())
