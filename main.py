import subprocess
import os

github_repo = "https://github.com/HoangShiro/Discord-DM-AI.git"

def update_bot():
    if not os.path.exists(".git"):
        # Thư mục Git chưa tồn tại, nên ta sẽ clone dự án từ GitHub
        subprocess.run(["git", "clone", github_repo], check=True)
    else:
        try:
            # Đảm bảo bạn đang ở trạng thái sạch, không có sự thay đổi cục bộ
            subprocess.run(["git", "reset", "--hard", "HEAD"], check=True)

            # Lấy phiên bản mới nhất từ kho GitHub
            subprocess.run(["git", "pull", "origin", "main"], check=True)
        except Exception as e:
            print(f"Lỗi khi cập nhật bot từ GitHub: {e}")

def start():
    import utils.bot as bot
    bot.bot_run()

if __name__ == '__main__':
    update_bot()
    try:
        start()
    except Exception as e:
        print("Start bot error: {0}".format(e))