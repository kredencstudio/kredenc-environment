set FTRACK_SERVER=https://%1.ftrackapp.com
set FTRACK_APIKEY=%2
set PYTHONDONTWRITEBYTECODE=1
set FTRACK_APP_ENVIRONMENTS=%~dp0\environment\env

%~dp0..\..\..\startup --environment environment.yml --attached

pause
