import bot
import asyncio
import os
import subprocess

github_repo = "https://github.com/HoangShiro/Discord-DM-AI.git"

def update_bot():
    try:  
        # Sử dụng Git để cập nhật mã nguồn
        subprocess.run(["git", "pull", "--no-edit", "--no-rebase"])
        
        print("Bot đã cập nhật thành công từ GitHub.")
    except Exception as e:
        print(f"Lỗi khi cập nhật bot từ GitHub: {e}")

def start():
    bot.bot_run()

if __name__ == '__main__':
    update_bot()
    start()