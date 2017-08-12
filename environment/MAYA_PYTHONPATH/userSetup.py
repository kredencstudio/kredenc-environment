print 'executing ftrack_studio usersetup.py'

# prepare ftrack favorites
try:
    import ft_maya

    try:
        ft_maya.set_project()
        print 'Project Folder set'
    except:
        print 'Project Folder probably doesn\'t exist'
except:
    print 'Could not set project folders. Ftrack might not be set up correctly'
