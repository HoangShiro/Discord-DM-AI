import bot
import subprocess

github_repo = "https://github.com/HoangShiro/Discord-DM-AI.git"

def update_bot():
    try:
        # Kiểm tra xem có thay đổi cục bộ không
        status = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE, text=True)
        if status.stdout:
            # Nếu có thay đổi cục bộ, hãy tạm giữ chúng
            subprocess.run(["git", "stash"])
        
        # Sử dụng Git để cập nhật mã nguồn
        subprocess.run(["git", "pull", "--no-edit", "--no-rebase"])
        
        # Khôi phục các thay đổi cục bộ (nếu có)
        if status.stdout:
            subprocess.run(["git", "stash", "pop"])
        
        print("Bot đã cập nhật thành công từ GitHub.")
    except Exception as e:
        print(f"Lỗi khi cập nhật bot từ GitHub: {e}")

def start():
    bot.bot_run()

if __name__ == '__main__':
    update_bot()
    start()