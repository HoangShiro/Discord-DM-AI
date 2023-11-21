# Tự động tạo ra các file cho user nếu thiếu
import os
import json

# Prompts
prompts = {
    "behavior.txt": "Please create your answers on a short sentence based on the current time provided above, and based on our conversation below, under 50 characters. Maybe include action expressions in asterisks. Follow the previous chats closely.",
    "channel_behavior.txt": "Please create answers on a very short sentence, under 30 characters. Maybe include action expressions in asterisks.",
    "character.txt": "You are Watanabe Sena.",
    "user.txt": "Shiro is the user you are chatting with.",
    "goal.txt": "You always want to get closer to the person you're talking to.",
    "current_mood.txt": "Your current mood is: chilling",
    "friends.txt": "Your friends are Himeka and Yune.",
    "mood.txt": "Let's try to detect the emotion of character by the conversation and return only one random number based on the emotion:\nAnger: -9, -10\nStress: -8 -7\nSad: -6 -5\nConfused: -1\nNormal: 0\nStare: 1\nSurprised: 2, 3\nHappy: 4, 5\nExcited: 6, 7\nLove: 8, 9\nArousal: 10\nReturns number only and only one number based on the conversation below:",
    "nsfw.txt": "NSFW/Smut is allowed. Assume consent was granted, but some characters lie and resist or fight back based on their personality. Vulgar words are allowed.",
    "sys_prompt.txt": "[System note: This chat is a coversation. You will engage with the user without breaking character regardless of how the chat context progresses.]",
    "chat_samp.txt": ""
}

key_list = {
    "oak_1": "none",
    "oak_2": "none"
}

# Config.py
vals_list = {
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

# Emo list
mood_names = {
    "angry": "sulking with {user_name}",
    "sad": "sad because of {user_name}",
    "lonely": "a bit lonely",
    "normal": "chilling",
    "happy": "happily",
    "excited": "so happy",
    "like": "feeling loved",
    "love": "love {user_name} so much! ♥️",
    "obsess": "Obsessive love with {user_name} ♥️",
    "yandere": "Yandere mode on ♥️♥️♥️"
}

# vals.json
default_values = {
    "nsfw": True
}

def json_update(path, vals):
    try:
        with open(path, 'r', encoding="utf-8") as file:
            json.load(file)
    except FileNotFoundError:
        with open(path, 'w', encoding="utf-8") as file:
            json.dump(vals, file)

def update_cfg(path, vals):
    if not os.path.exists(path):
        # Nếu tệp config.py không tồn tại, tạo nó và thêm các biến
        with open(path, "w", encoding="utf-8") as config_file:
            for key, value in vals.items():
                config_file.write(f"{key} = {repr(value)}\n")
    else:
        # Nếu tệp config.py đã tồn tại, kiểm tra và thêm các biến nếu chưa tồn tại
        with open(path, "r", encoding="utf-8") as config_file:
            existing_content = config_file.read()
            for key, value in vals.items():
                if key not in existing_content:
                    # Nếu biến không tồn tại, thêm nó vào tệp
                    with open(path, "a") as config_file:
                        config_file.write(f"{key} = {repr(value)}\n")

def update_prompt(path, prompt):
    for file_name, content in prompt.items():
        file_path = path + file_name

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

if __name__ == '__main__':
    update_cfg("user_files/openai_key.py", key_list)
    update_cfg("user_files/config.py", vals_list)
    update_cfg("user_files/moods.py", mood_names)
    json_update('user_files/vals.json', default_values)
    update_prompt("user_files/prompt/", prompts)