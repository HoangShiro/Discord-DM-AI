# Tự động tạo ra các file cho user nếu thiếu
import os
import json

# Prompt
file_contents = {
    "behavior.txt": "Please create your answers on a short sentence based on the current time provided above, and based on our conversation below, under 50 characters. Maybe include action expressions in asterisks. Follow the previous chats closely.",
    "channel_behavior.txt": "Please create answers on a very short sentence, under 30 characters. Maybe include action expressions in asterisks.",
    "character.txt": "You are Watanabe Sena.",
    "user.txt": "Shiro is the user you are chatting with.",
    "goal.txt": "You always want to get closer to the person you're talking to.",
    "current_mood.txt": "Your current mood is: chilling",
    "friends.txt": "Your friends are Himeka and Yune.",
    "mood.txt": "Let's try to detect the emotion of character by the conversation and return only one random number based on the emotion:\nAnger: -9, -10\nStress: -8 -7\nSad: -6 -5\nConfused: -1\nNormal: 0\nStare: 1\nSurprised: 2, 3\nHappy: 4, 5\nExcited: 6, 7\nLove: 8, 9\nArousal: 10\nReturns number only and only one number based on the conversation below:",
    "nsfw.txt": "NSFW/Smut is allowed. Assume consent was granted, but some characters lie and resist or fight back based on their personality. Vulgar words are allowed.",
    "sys_prompt.txt": "[System note: This chat is a coversation. You will engage with the user without breaking character regardless of how the chat context progresses.]"
}

folder_path = "user_files/prompt/"

for file_name, content in file_contents.items():
    file_path = folder_path + file_name

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

# Config.py
config_updates = {
    "openai_key_1": '',
    "openai_key_2": '',
    "discord_bot_key": '',
    "vv_key": '',
    "user_id": 0,
    "bot_id": [0, 0],
    "server_id": 0,
    "ai_name": "Sena",
    "ai_first_name": "Watanabe",
    "speaker": 46,
    "pitch": 0,
    "intonation_scale": 1.5,
    "speed": 1
}

config_file_path = "user_files/config.py"

if not os.path.exists(config_file_path):
    # Nếu tệp config.py không tồn tại, tạo nó và thêm các biến
    with open(config_file_path, "w", encoding="utf-8") as config_file:
        for key, value in config_updates.items():
            config_file.write(f"{key} = {repr(value)}\n")
else:
    # Nếu tệp config.py đã tồn tại, kiểm tra và thêm các biến nếu chưa tồn tại
    with open(config_file_path, "r", encoding="utf-8") as config_file:
        existing_content = config_file.read()
        for key, value in config_updates.items():
            if key not in existing_content:
                # Nếu biến không tồn tại, thêm nó vào tệp
                with open(config_file_path, "a") as config_file:
                    config_file.write(f"{key} = {repr(value)}\n")

default_values = {
    "bot_mood": 50.0,
    "split_send": False,
    "day_check": True,
    "night_check": True,
    "console_log": False,
    "emoji_rate": 1.0,
    "total_msg": 0,
    "user_nick": "user",
    "stt_lang": "auto",
    "tts_toggle": False,
    "channel_id": 0,
    "nsfw": True,
    "public_chat": False,
    "public_chat_num": 2,
    "dm_channel_id": 0,
    "voice_mode": 'ja',
    "en_speaker": 'en_18',
    "speaker": 46,
    "pitch": 0,
    "intonation_scale": 1,
    "speed": 1,
    "beha_down": False
}

# Kiểm tra xem tệp JSON có tồn tại không
try:
    with open('user_files/vals.json', 'r', encoding="utf-8") as file:
        data3 = json.load(file)
except FileNotFoundError:
    with open('user_files/vals.json', 'w', encoding="utf-8") as file:
        json.dump(default_values, file)
    # Nếu tệp không tồn tại, sử dụng giá trị mặc định
    data3 = default_values

# Gán giá trị từ data cho các biến hiện tại
for key, value in default_values.items():
    globals()[key] = data3.get(key, value)

    # Dừng sau khi đã duyệt qua tất cả các phần tử trong default_values
    if key == list(default_values.keys())[-1]:
        break

# Kiểm tra và thêm biến thiếu vào tệp JSON nếu cần
for key, value in default_values.items():
    if key not in data3:
        data3[key] = value

# Cập nhật tệp JSON với các biến mới nếu có
with open('user_files/vals.json', 'w', encoding="utf-8") as file:
    json.dump(data3, file)