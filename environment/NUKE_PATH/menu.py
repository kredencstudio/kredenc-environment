import nuke
import traceback

print 'executing NUKE_PATH menu.py'

# fill favorites
nuke.menu('Nuke').addCommand('Kredenc/Fill favorites', 'import ft_nuke;ft_nuke.projectFavorites()')
print 'fill favorite'
try:
# prepare ftrack favorites
    import ft_nuke
    print 'imported ft_nuke'
    ft_nuke.projectFavorites()
    # add custom fields do write node
    nuke.menu('Nodes' ).addCommand('Image/Write', lambda: ft_nuke.Write().create(), 'w')
except:
   print '-'*60
   traceback.print_exc(file=sys.stdout)
   print '-'*60
   print 'could not set project folders. Ftrack might not be set up correctly'


# SETUP PYBLISH

import pyblish.api

nuke_menu = nuke.menu('Nuke')
file_menu = nuke_menu.findItem('File')
file_menu.addCommand("pyblish", 'pyblish_nuke.show()', "`")


pyblish.api.register_gui('pyblish_lite')
pyblish.api.register_gui('pyblish_qml')

print 'finished with NUKE_PATH menu.py'
