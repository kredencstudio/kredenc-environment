set FTRACK_SERVER=https://%1.ftrackapp.com
set FTRACK_APIKEY=%2
set PYTHONDONTWRITEBYTECODE=1

%~dp0..\..\..\startup --environment environment.yml --attached
