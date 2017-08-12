import os
import ft_utils
import maya.cmds as cmds


def set_project():

    work_area = get_work_project()

    print('PROJECT TO BE SET: ' + work_area)

    import pymel.core as pm
    pm.mel.setProject(work_area)


def get_work_project():

    entity = ft_utils.get_entity()

    root = entity.getProject().getRoot()
    print root

    if 'ASSET_BUILD' in os.environ.keys():
        templates = [
            'asset.task.work'
        ]
    else:
        templates = [
            'shot.task.work'
        ]

    work_area = ft_utils.getPathsYaml(entity,
                                          templateList=templates,
                                          root=root)[0]

    return work_area.replace('\\', '/')


def get_output_project():

    entity = ft_utils.get_entity()

    root = os.getenv('PROJECT_ROOT')
    print root

    if 'ASSET_BUILD' in os.environ.keys():
        templates = [
            'asset.task.output'
        ]
    else:
        templates = [
            'shot.task.output'
        ]

    output_area = ft_utils.getPathsYaml(entity,
                                            templateList=templates,
                                            root=root)[0]

    return output_area.replace('\\', '/')


def framerate_init():
    '''Set the initial framerate with the values set on the shot'''
    import ftrack
    shotId = os.getenv('FTRACK_SHOTID')

    shot = ftrack.Shot(id=shotId)
    try:
        fps = str(int(shot.get('fps')))
    except:
        show = shot.getProject()
        fps = str(int(show.get('fps')))

    mapping = {
        '15': 'game',
        '24': 'film',
        '25': 'pal',
        '30': 'ntsc',
        '48': 'show',
        '50': 'palf',
        '60': 'ntscf',
    }

    fpsType = mapping.get(fps, 'pal')
    cmds.warning('Setting current unit to {0}'.format(fps))
    cmds.currentUnit(time=fpsType)


def framerange_init():
    import ftrack
    shotId = os.getenv('FTRACK_SHOTID')

    shot = ftrack.Shot(id=shotId)
    try:
        sf = int(shot.getFrameStart())
        ef = int(shot.getFrameEnd())
        cmds.playbackOptions(ast=sf, aet=ef, min=sf, max=ef)
    except:
        print 'only supported on shots'
