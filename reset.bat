taskkill /IM "sublime_text.exe" /F
timeout /t 5 /nobreak
RMDIR "%APPDATA%\\Sublime Text" /s /q
RMDIR "%LOCALAPPDATA%\\Sublime Text" /s /q
PAUSE
