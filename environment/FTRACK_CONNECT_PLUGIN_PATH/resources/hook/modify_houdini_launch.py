import logging
import json
import os
import ftrack
import ft_utils

logging.basicConfig()
logger = logging.getLogger()


def load_env(path):
    """Load options json from path"""

    with open(path, "r") as f:
        return json.load(f)


def appendPath(path, key, environment):
    '''Append *path* to *key* in *environment*.'''
    try:
        environment[key] = (
            os.pathsep.join([
                environment[key], str(path)
            ])
        )
    except KeyError:
        environment[key] = str(path)

    return environment


def modify_houdini_launch(event):
    '''Modify the application environment.'''
    data = event['data']
    app = data['application']
    app_name = app['identifier'].split('_')[0]

    if 'houdini' not in app_name:
        return

    env_add = {}

    # Try getting taskid from event selection
    try:
        taskid = data['context']['selection'][0]['entityId']
    except:
        logger.info('Unable to determine task')

    task = ftrack.Task(taskid)

    task_env = ft_utils.get_task_enviro(task)

    for key in task_env:
        logger.info(key + ': ' + task_env[key])

    if 'ASSET_BUILD' in task_env.keys():
        templates = [
            'asset.task.work',
        ]
    else:
        templates = [
            'shot.task.work'
        ]

    root = task.getProject().getRoot()
    # Get paths for all the chosen templates
    paths = ft_utils.getPathsYaml(task,
                                      templateList=templates,
                                      root=root
                                      )

    workpath = ''
    for path in paths:
        workpath = path
        logger.info('workpath: {}'.format(workpath))

    # SET ENVIRONMENTS

    try:
        env_add['FS'] = [str(int(task.getParent().getFrameStart()))]
    except Exception:
        env_add['FS'] = ['1']

    try:
        env_add['FE'] = [str(int(task.getParent().getFrameEnd()))]
    except Exception:
        env_add['FE'] = ['1']

    #
    JOB = root
    HOUDINI_SPLASH_FILE = 'K:/core/dev/studio/launchers/hou_splash_kredenc.jpg'

    project_otls = None

    env_add['HOUDINI_PATH'] = [workpath, '&']

    if project_otls:
        env_add['HOUDINI_OTLSCAN_PATH'] = [os.pathsep.join([project_otls, '&']), '&']

    env_add['JOB'] = [JOB]
    env_add['HOUDINI_SPLASH_FILE'] = [HOUDINI_SPLASH_FILE]

    try:
        f = open(workpath + '/jump.pref', 'w+')
        f.write('\n')
        logger.info('JOB: {}'.format(JOB))
        path_to_add = (workpath.replace(JOB, '$JOB')).replace('\\', '/')
        logger.info('path to add: {}'.format(path_to_add))
        f.write(path_to_add + "\n")
        f.close()
    except:
        logger.debug('Task Location not found:\n{0}'.format(JOB + workpath))

    # Add each path in config file to the environment
    if env_add:
        for variable in env_add:
            for path in env_add[variable]:
                appendPath(path, str(variable), data['options']['env'])


def register(registry, **kw):
    '''Register location plugin.'''

    # Validate that registry is the correct ftrack.Registry. If not,
    # assume that register is being called with another purpose or from a
    # new or incompatible API and return without doing anything.
    if registry is not ftrack.EVENT_HANDLERS:
        # Exit to avoid registering this plugin again.
        return

    ftrack.EVENT_HUB.subscribe(
        'topic=ftrack.connect.application.launch',
        modify_houdini_launch
    )

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    ftrack.setup()

    ftrack.EVENT_HUB.subscribe(
        'topic=ftrack.connect.application.launch',
        modify_houdini_launch)
    ftrack.EVENT_HUB.wait()
