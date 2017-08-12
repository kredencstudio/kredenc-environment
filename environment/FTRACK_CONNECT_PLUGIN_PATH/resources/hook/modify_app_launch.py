import logging
import ftrack
import ft_utils


logging.basicConfig()
logger = logging.getLogger()


def modify_application_launch(event):
    '''Modify the application environment.'''
    data = event['data']

    taskid = data['context']['selection'][0].get('entityId')

    # Append task specific variables

    task = ftrack.Task(taskid)
    task_env = ft_utils.get_task_enviro(task)

    for variable in task_env:
            data['options']['env'][variable] = task_env[variable]

    logger.info('TASK ENV:{}'.format(task_env))


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
        modify_application_launch
    )


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    ftrack.setup()

    ftrack.EVENT_HUB.subscribe(
        'topic=ftrack.connect.application.launch',
        modify_application_launch)
    ftrack.EVENT_HUB.wait()
