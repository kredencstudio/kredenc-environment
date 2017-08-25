import os
import json
import re
import pprint


def _appendPath(path, key):
    '''Append *path* to *variable* in environment.'''

    if (key in os.environ.keys()):
        if path not in os.environ[key]:
            os.environ[key] += os.pathsep + path
    else:
        os.environ.setdefault(key, path)


def _get_config_files(names):

    if not isinstance(names, list):
        names = [names]

    env_path = os.environ.get('FTRACK_APP_ENVIRONMENTS')
    if not env_path:
        env_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'environment', 'env'))
    env_files = []

    for f in names:
        # determine config file for version independent environment
        env_file_name = '{}.json'.format(f)
        env_files.append(os.path.join(env_path, env_file_name))

    return env_files


def load_env(names):

    env_files = _get_config_files(names)

    env_add = []

    # loop through config files
    for env_file in env_files:
        try:
            with open(env_file, "r") as f:
                env_add = json.load(f)
        except:
            env_add = None

        # Add each path in config file to the environment
        if env_add:
            for variable in env_add:
                for path in env_add[variable]:
                    keys = re.findall(r'{.*?}', path)
                    for key in keys:
                        found_key = os.path.abspath(os.environ.get(key[1:-1]))
                        path = path.replace(key, found_key)

                    _appendPath(str(path), str(variable))

        print ''
        print(env_file.upper())
        pprint.pprint(env_add)


def pass_env(names):

    env_files = _get_config_files(names)

    environment = {}
    env_add = []

    # loop through config files
    for env_file in env_files:
        try:
            with open(env_file, "r") as f:
                env_add = json.load(f)
        except:
            env_add = None

        # Add each path in config file to the environment
        if env_add:
            for variable in env_add:
                paths = []
                for path in env_add[variable]:
                    keys = re.findall(r'{.*?}', path)
                    for key in keys:
                        found_key = os.path.abspath(os.environ.get(key[1:-1]))
                        path = path.replace(key, found_key)

                    paths.append(path)
                    # _appendPath(str(path), str(variable))

                env_add[variable] = paths

        print('Adding {} to environment.'.format(env_file.upper()))

        for key in env_add:
            if key in environment.keys():
                environment[key] = list(set(environment[key] + env_add[key]))
            else:
                environment[key] = env_add[key]

    print ''
    print 'ENVIRONMENT'
    pprint.pprint(environment)
    print ''

    return environment
