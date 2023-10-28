@echo off
setlocal enabledelayedexpansion

:step_1
if exist %USERPROFILE%\scoop\ (
    echo Scoop installed.
) else (
    powershell -command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"
    powershell -command "irm get.scoop.sh | iex"
)

:step_2
git --version > nul 2>&1
if %errorlevel% equ 0 (
    echo Git installed.
) else (
    scoop install git
)

:step_3
python --version > nul 2>&1
if %errorlevel% equ 0 (
    echo Python installed.
) else (
    scoop bucket add versions
    scoop install python311
)

:step_4
:: Sử dụng thư mục hiện tại của file batch làm thư mục gốc
set "base_dir=%~dp0"

:: Đặt tên thư mục đích (có thể thay đổi tùy ý)
set "destination_folder=Discord-DM-AI"

mkdir "!base_dir!%destination_folder%"
cd "!base_dir!%destination_folder%"

cd "!base_dir!%destination_folder%"
:: Đặt đường dẫn của kho lưu trữ Git
set "repo_url=https://github.com/HoangShiro/Discord-DM-AI.git"

:: Kiểm tra xem thư mục đã có kho lưu trữ Git chưa
if not exist ".git" (
  :: Nếu chưa có, thực hiện git clone để tải về kho lưu trữ
  git clone "%repo_url%" .
) else (
  :: Nếu đã tồn tại, sử dụng git pull để cập nhật kho lưu trữ
  git pull
)

pip install -r requirements.txt

python setup.py

start start_bot.bat

:: Kết thúc script
exit /b
