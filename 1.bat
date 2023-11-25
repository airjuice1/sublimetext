xcopy .\*.* "%APPDATA%\Sublime Text\Packages\User" /R /I /S /Y /EXCLUDE:excludedfileslist.txt
mkdir "%HOMEPATH%\\Documents\\webapps"
mkdir "%HOMEPATH%\\Documents\\webapps\\.sublime"
PAUSE