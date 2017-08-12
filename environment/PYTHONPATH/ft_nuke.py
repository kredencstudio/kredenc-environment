import nuke
import os
import ft_utils


def projectFavorites():

    entity = ft_utils.get_entity()

    root = entity.getProject().getRoot()

    try:
        paths = ft_utils.getAllPathsYaml(entity)
    except:
        print 'this project is not yet supported'
        return

    if 'ASSET_BUILD' in os.environ.keys():
        pathNameMapping = {
            'asset.task.work': 'Task work',
            'asset.render': 'Task output',
        }
    else:
        pathNameMapping = {
            'shot.task.work': 'Task work',
            'shot.render': 'Task output',
        }

    dir = os.path.dirname(os.path.dirname(__file__))
    icon_path = os.path.join(dir, 'resource', 'images', 'ft_logo.png')

    for path in paths:
        if path[1].name in pathNameMapping.keys():
            niceName = pathNameMapping.get(path[1].name, None)
            nuke.removeFavoriteDir(niceName)
            path_to_add = os.path.join(root, path[0])
            os.environ[niceName] = path_to_add
            nuke.addFavoriteDir(
                niceName,
                path_to_add,
                nuke.IMAGE | nuke.SCRIPT | nuke.GEO,
                icon=icon_path)


# CUSTOM WRITE NODE WITH AUTOFILL

class Write:

    def __init__(self, name="Write"):
        self.name = name

    def create(self):
        w = nuke.createNode('Write', inpanel=True)

        count = 1
        while nuke.exists(self.name + str(count)):
            count += 1
        w.knob('name').setValue(self.name + str(count))

        w.knob('name').setValue(self.name + str(count))

        self.add_auto_path(w=w)

    def add_auto_path(self, w=None):
        if not w:
            w = nuke.thisNode()

        t = nuke.Tab_Knob("paths")
        w.addKnob(t)

        w.addKnob(nuke.EvalString_Knob(
        'task_output', 'Task Output', '[python os.getenv("task output")]'))
        w.addKnob(nuke.EvalString_Knob(
            'script', 'Script Name', '[file rootname [file tail [value root.name] ] ]'))

        w.addKnob(nuke.EvalString_Knob('output_exp', 'Output expression',
                                       "[value task_output]/[value version]/[value script].####.exr"))

        w.addKnob(nuke.EvalString_Knob('version_string', 'version', r'[python \"\".join(nukescripts.version_get(nuke.root().knob(\"name\").value(), \"v\"))]'))

        w.addKnob(nuke.Text_Knob(' '))

        updateKnob = nuke.PyScript_Knob('bake_path', 'Bake Path')
        w.addKnob(updateKnob)
        updateKnob.setValue('reload(ft_nuke); ft_nuke.Write().bake_path()')

        updateKnob = nuke.PyScript_Knob('live_path', 'Live Path')
        w.addKnob(updateKnob)
        updateKnob.setValue('reload(ft_nuke); ft_nuke.Write().live_path()')

        self.bake_path(w)

        w.knob('file_type').setValue('exr')
        w.knob('datatype').setValue('16')
        w.knob('compression').setValue('Zips')


    def bake_path(self, w=None):
        w = w or nuke.thisNode()
        task_output = w['task_output'].evaluate()
        script = w['script'].evaluate()
        version = w['version_string'].evaluate()
        script = w['script'].evaluate()
        path = os.path.join(task_output, 'render', version, (script +'.####.exr'))
        path = path.replace('\\', '/')
        w.knob('file').fromScript(path)
        print(path)

    def live_path(self, w=None):
        w = w or nuke.thisNode()
        path = w['output_exp'].getText()
        w.knob('file').fromScript(path)
        print path
