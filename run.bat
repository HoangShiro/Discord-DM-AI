@echo off

:seterrorcount
set /a errorcount=0

pip install -r requirements.txt

:start_ai
cls
python main.py

echo ----------------------
echo.
echo Bot is Restarting!
echo.
echo ----------------------

REM Kiểm tra trạng thái trả về của lệnh py main.py
if %errorlevel% neq 0 (
  set /a errorcount+=1
  echo Error %errorcount% times.
  if %errorcount% geq 2 (
    goto exit
  )
) else (
  REM Nếu không có lỗi, đặt lại số lần lỗi về 0
  set /a errorcount=0
)

GOTO start_ai
:exit
echo Bot run error above.
PAUSE
