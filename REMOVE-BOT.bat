@echo off
setlocal enabledelayedexpansion

echo ----------------------------------------------------------
echo WARNING: Back up if necessary before performing this action.
echo Press any key to completely delete your bot.
echo -----------------------------------------------------------
pause
cls
set "bot_py_path=%~dp0\bot.py"

if exist "!bot_py_path!" (
    set "parent_dir=%~dp0"
    cd /d "!parent_dir!"
    rmdir /s /q "!parent_dir!"
) else (
    echo Error: Can't remove bot. Are you sure your bot is here?
    PAUSE
    exit
)

endlocal
