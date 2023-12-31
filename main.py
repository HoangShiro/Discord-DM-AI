import subprocess
import asyncio
from utils.private_files import *

github_repo = "https://github.com/HoangShiro/Discord-DM-AI.git"

def update_bot():
    try:
        # Đảm bảo bạn đang ở trạng thái sạch, không có sự thay đổi cục bộ
        subprocess.run(["git", "reset", "--hard", "HEAD"], check=True)

        # Lấy phiên bản mới nhất từ kho GitHub
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        
    except Exception as e:
        print(f"Lỗi khi cập nhật bot từ GitHub: {e}")

def start():
    import utils.bot as bot
    loop = asyncio.get_event_loop()
    loop.create_task(bot.bot_run())
    loop.run_forever()

if __name__ == '__main__':
    update_bot()

    update_cfg("user_files/openai_key.py", key_list)
    update_cfg("user_files/config.py", vals_list)
    update_cfg("user_files/moods.py", mood_names)
    json_update('user_files/vals.json', default_values)
    update_prompt("user_files/prompt/", prompts)

    #try:
    start()
    #except Exception as e:
    #    print("Start bot error: {0}".format(e))