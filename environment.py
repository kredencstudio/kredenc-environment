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

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

os.environ.setdefault('STUDIO_REPOS', os.path.join(r'\\kre-c01', 'share', 'core', 'repos'))
os.environ.setdefault('STUDIO_SOFT', os.path.join(r'\\kre-c01', 'share', 'core', 'software'))
os.environ.setdefault('STUDIO_USER', getpass.getuser())

environment = launch_tools.pass_env(environments)
utils.write_environment(environment)
