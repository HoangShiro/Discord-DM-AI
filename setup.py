import tkinter as tk
from tkinter import filedialog
import re

# Định nghĩa danh sách các biến và giá trị cần cập nhật
config_updates = {
    "openai_key_1": "",
    "openai_key_2": "",
    "discord_bot_key": "",
    "vv_key": "",
    "user_id": "",
    "server_id": "",
    "ai_name": "",
    "ai_first_name": "",
    "speaker": "",
    "pitch": "",
    "intonation_scale": "",
    "speed": ""
}

def save_character_info():
    character_info = character_text.get(1.0, "end-1c")
    if character_info.strip():
        with open(".\\prompt\\character.txt", "w", encoding="utf-8") as character_file:
            character_file.write(character_info)

def save_user_info():
    user_info = user_text.get(1.0, "end-1c")
    if user_info.strip():
        with open(".\\prompt\\user.txt", "w", encoding="utf-8") as user_file:
            user_file.write(user_info)

def save_character_behavior():
    char_bv = charbv_text.get(1.0, "end-1c")
    if char_bv.strip():
        with open(".\\prompt\\behavior.txt", "w", encoding="utf-8") as user_file:
            user_file.write(char_bv)

def save_config_info():
    # Lấy giá trị từ các trường nhập liệu
    openai_key1 = openai_key1_entry.get()
    openai_key2 = openai_key2_entry.get()
    discord_bot_key = discord_bot_key_entry.get()
    vv_key = vv_key_entry.get()
    user_id = user_id_entry.get()
    server_id = server_id_entry.get()
    ai_name = ai_name_entry.get()
    ai_first_name = ai_first_name_entry.get()
    speaker = speaker_entry.get()
    pitch = pitch_entry.get()
    intonation_scale = intonation_scale_entry.get()
    speed = speed_entry.get()

    # Cập nhật giá trị trong danh sách config_updates
    config_updates["openai_key_1"] = openai_key1
    config_updates["openai_key_2"] = openai_key2
    config_updates["discord_bot_key"] = discord_bot_key
    config_updates["vv_key"] = vv_key
    config_updates["user_id"] = int(user_id)
    config_updates["server_id"] = int(server_id)
    config_updates["ai_name"] = ai_name
    config_updates["ai_first_name"] = ai_first_name

    if not speaker:
        speaker = 46
    config_updates["speaker"] = int(speaker)
    config_updates["pitch"] = int(pitch)
    config_updates["intonation_scale"] = int(intonation_scale)
    config_updates["speed"] = int(speed)

    # Đọc nội dung của tệp cấu hình
    with open(".\\utils\\config.py", "r", encoding="utf-8") as config_file:
        config_contents = config_file.readlines()

    # Duyệt qua từng dòng trong tệp cấu hình và cập nhật giá trị nếu có
    updated_config_contents = []
    for line in config_contents:
        for var_name, var_value in config_updates.items():
            pattern = re.compile(rf"{var_name} = .+")
            if pattern.match(line):
                # Bao quanh giá trị với ngoặc tương ứng, trừ user_id
                if isinstance(var_value, str) and var_name not in ["user_id"]:
                    updated_line = f"{var_name} = '{var_value}'\n"
                else:
                    updated_line = f"{var_name} = {var_value}\n"
                updated_config_contents.append(updated_line)
                break
        else:
            updated_config_contents.append(line)

    # Ghi lại nội dung cập nhật vào tệp cấu hình
    with open(".\\utils\\config.py", "w", encoding="utf-8") as config_file:
        config_file.writelines(updated_config_contents)



def load_config_values():
    try:
        # Đọc giá trị từ tệp character.txt và điền vào trường nhập liệu
        with open(".\\prompt\\character.txt", "r", encoding="utf-8") as character_file:
            character_info = character_file.read()
            character_text.delete(1.0, "end")
            character_text.insert("insert", character_info)

        # Đọc giá trị từ tệp user.txt và điền vào trường nhập liệu
        with open(".\\prompt\\user.txt", "r", encoding="utf-8") as user_file:
            user_info = user_file.read()
            user_text.delete(1.0, "end")
            user_text.insert("insert", user_info)
        
        # Đọc giá trị từ tệp behavior.txt và điền vào trường nhập liệu
        with open(".\\prompt\\behavior.txt", "r", encoding="utf-8") as charbv_file:
            char_bv = charbv_file.read()
            charbv_text.delete(1.0, "end")
            charbv_text.insert("insert", char_bv)
    except FileNotFoundError:
        pass

    # Đọc giá trị từ tệp cấu hình và điền vào các trường nhập liệu
    config_values = {}
    with open(".\\utils\\config.py", "r", encoding="utf-8") as config_file:
        config_contents = config_file.readlines()

    for line in config_contents:
        for var_name, _ in config_updates.items():
            pattern = re.compile(rf"{var_name} = .+")
            match = pattern.match(line)
            if match:
                value = match.group().split(" = ")[1]

                if value.startswith("[") and value.endswith("]"):
                    # Loại bỏ dấu ngoặc vuông và khoảng trắng
                    value = value[1:-1].strip()
                    # Chuyển chuỗi giá trị thành danh sách
                    value = [v.strip() for v in value.split(",")]
                else:
                    # Bỏ dấu ngoặc từ giá trị
                    if value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                config_values[var_name] = value
                break

    openai_key1_entry.delete(0, "end")
    openai_key1_entry.insert(0, config_values.get("openai_key_1", ""))

    openai_key2_entry.delete(0, "end")
    openai_key2_entry.insert(0, config_values.get("openai_key_2", ""))

    discord_bot_key_entry.delete(0, "end")
    discord_bot_key_entry.insert(0, config_values.get("discord_bot_key", ""))

    vv_key_entry.delete(0, "end")
    vv_key_entry.insert(0, config_values.get("vv_key", ""))

    user_id_entry.delete(0, "end")
    user_id_entry.insert(0, config_values.get("user_id", ""))

    server_id_entry.delete(0, "end")
    server_id_entry.insert(0, config_values.get("server_id", ""))

    ai_name_entry.delete(0, "end")
    ai_name_entry.insert(0, config_values.get("ai_name", ""))

    ai_first_name_entry.delete(0, "end")
    ai_first_name_entry.insert(0, config_values.get("ai_first_name", ""))

    speaker_entry.delete(0, "end")
    speaker_entry.insert(0, config_values.get("speaker", ""))

    pitch_entry.delete(0, "end")
    pitch_entry.insert(0, config_values.get("pitch", ""))

    intonation_scale_entry.delete(0, "end")
    intonation_scale_entry.insert(0, config_values.get("intonation_scale", ""))

    speed_entry.delete(0, "end")
    speed_entry.insert(0, config_values.get("speed", ""))

app = tk.Tk()
app.attributes('-alpha', 0.9)
app.iconbitmap('images/Yuueh.ico')
app.title("Your character's setting")

# Character Info
character_label = tk.Label(app, text="\nCharacter info:\nDescribe your character's personality, appearance, and other information.", font=("Helvetica", 10))
character_label.grid(row=0, column=0, columnspan=2)
character_text = tk.Text(app, height=5, width=80)
character_text.grid(row=1, column=0, columnspan=2)

# User Info
user_label = tk.Label(app, text="\nUser info:\nDescribe your name and any other information you want your character to know.", font=("Helvetica", 10))
user_label.grid(row=2, column=0, columnspan=2)
user_text = tk.Text(app, height=5, width=80)
user_text.grid(row=3, column=0, columnspan=2)

# Character behavior
charbv_label = tk.Label(app, text="\nCharacter behavior:\nThe way/context in which your character will chat.", font=("Helvetica", 10))
charbv_label.grid(row=4, column=0, columnspan=2)
charbv_text = tk.Text(app, height=5, width=80)
charbv_text.grid(row=5, column=0, columnspan=2)

# key1
openai_key1_label = tk.Label(app, text="\nOpenai key 1:")
openai_key1_label.grid(row=6, column=0)
openai_key1_entry = tk.Entry(app)
openai_key1_entry.grid(row=7, column=0)

# key2
openai_key2_label = tk.Label(app, text="\nOpenai key 2:")
openai_key2_label.grid(row=6, column=1)
openai_key2_entry = tk.Entry(app)
openai_key2_entry.grid(row=7, column=1)

discord_bot_key_label = tk.Label(app, text="\nDiscord bot token:")
discord_bot_key_label.grid(row=8, column=0)
discord_bot_key_entry = tk.Entry(app)
discord_bot_key_entry.grid(row=9, column=0)

vv_key_label = tk.Label(app, text="\nVoiceVox API key:")
vv_key_label.grid(row=8, column=1)
vv_key_entry = tk.Entry(app)
vv_key_entry.grid(row=9, column=1)

ai_name_label = tk.Label(app, text="\nCharacter last name")
ai_name_label.grid(row=10, column=0)
ai_name_entry = tk.Entry(app)
ai_name_entry.grid(row=11, column=0)

ai_first_name_label = tk.Label(app, text="\nCharacter first name:")
ai_first_name_label.grid(row=10, column=1)
ai_first_name_entry = tk.Entry(app)
ai_first_name_entry.grid(row=11, column=1)

user_id_label = tk.Label(app, text="\nDiscord user id:")
user_id_label.grid(row=12, column=0)
user_id_entry = tk.Entry(app)
user_id_entry.grid(row=13, column=0)

server_id_label = tk.Label(app, text="\nDiscord server id:")
server_id_label.grid(row=12, column=1)
server_id_entry = tk.Entry(app)
server_id_entry.grid(row=13, column=1)

speaker_label = tk.Label(app, text="\nCharacter's voice setting (optional)", font=("Helvetica", 10))
speaker_label.grid(row=14, column=0, columnspan=2)

speaker_label = tk.Label(app, text="\nCharacter speaker id:")
speaker_label.grid(row=15, column=0)
speaker_entry = tk.Entry(app)
speaker_entry.grid(row=16, column=0)

pitch_label = tk.Label(app, text="\nVoice pitch:")
pitch_label.grid(row=15, column=1)
pitch_entry = tk.Entry(app)
pitch_entry.grid(row=16, column=1)

intonation_scale_label = tk.Label(app, text="\nVoice intonation:")
intonation_scale_label.grid(row=17, column=0)
intonation_scale_entry = tk.Entry(app)
intonation_scale_entry.grid(row=18, column=0)

speed_label = tk.Label(app, text="\nVoice speed:")
speed_label.grid(row=17, column=1)
speed_entry = tk.Entry(app)
speed_entry.grid(row=18, column=1)


load_config_values()  # Tải giá trị từ tệp khi khởi động chương trình

save_and_close_button = tk.Button(app, text="Save and Close", command=lambda: [save_character_info(), save_user_info(), save_config_info(), app.quit()])
save_and_close_button.grid(row=20, column=0, columnspan=2)

app.mainloop()