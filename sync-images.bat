@echo off
cd /d "%~dp0"
echo Syncing roleplay images...
git add img/roleplay/
git status --short img/roleplay/
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
