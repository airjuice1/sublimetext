del /S "%APPDATA%\\Sublime Text\\Packages\\User\\*.sublime-snippet"
timeout /t 1 /nobreak
xcopy .\*.* "%APPDATA%\Sublime Text\Packages\User" /R /I /S /Y /EXCLUDE:excludedfileslist.txt
mkdir "%HOMEPATH%\\Documents\\webapps"
rem mkdir "%HOMEPATH%\\Documents\\workspaces"
rem mkdir "%HOMEPATH%\\Documents\\webapps\\.sublime"
PAUSE