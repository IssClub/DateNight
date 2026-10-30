@echo off
cd /d "%~dp0"
echo Syncing new images...
git add img/roleplay/ img/GIF/
git commit -m "sync: new images"
if %errorlevel% neq 0 (
  echo Nothing to sync.
  pause
  exit /b 0
)
git push
echo.
echo Done! Images are live.
pause
