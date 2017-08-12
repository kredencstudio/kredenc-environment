import nuke

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
    nuke.addOnUserCreate(ft_nuke.Write().add_auto_path, nodeClass='Write')
except:
   print 'could not set project folders. Ftrack might not be set up correctly'


# SETUP PYBLISH

import pyblish.api

nuke_menu = nuke.menu('Nuke')
file_menu = nuke_menu.findItem('File')
file_menu.addCommand("pyblish", 'pyblish_nuke.show()', "`")


pyblish.api.register_gui('pyblish_lite')

print 'finished with NUKE_PATH menu.py'
# pyblish.api.register_gui('pyblish_qml')
