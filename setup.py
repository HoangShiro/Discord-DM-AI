import tkinter as tk
from tkinter import filedialog
import re

# Định nghĩa danh sách các biến và giá trị cần cập nhật
config_updates = {
    "openai_key_1": "",
    "openai_key_2": "",
    "discord_bot_key": "",
    "vv_key": "",
    "user_id": [],
    "bot_id": [],
    "server_id": [],
    "ai_name": "",
    "ai_first_name": "",
    "speaker": ""
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

def save_config_info():
    # Lấy giá trị từ các trường nhập liệu
    openai_key1 = openai_key1_entry.get()
    openai_key2 = openai_key2_entry.get()
    discord_bot_key = discord_bot_key_entry.get()
    vv_key = vv_key_entry.get()
    user_id = user_id_entry.get()
    ai_name = ai_name_entry.get()
    ai_first_name = ai_first_name_entry.get()
    speaker = speaker_entry.get()

    # Cập nhật giá trị trong danh sách config_updates
    config_updates["openai_key_1"] = openai_key1
    config_updates["openai_key_2"] = openai_key2
    config_updates["discord_bot_key"] = discord_bot_key
    config_updates["vv_key"] = vv_key
    # Kiểm tra kiểu dữ liệu và cập nhật user_id dưới dạng danh sách hoặc danh sách trống
    if user_id:
        config_updates["user_id"] = f"[{user_id}]"
    else:
        config_updates["user_id"] = []

    config_updates["ai_name"] = ai_name
    config_updates["ai_first_name"] = ai_first_name

    if not speaker:
        speaker = 46
    config_updates["speaker"] = int(speaker)  # Chuyển giá trị về kiểu int

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
    user_id_entry.insert(0, ", ".join(config_values.get("user_id", [])))

    ai_name_entry.delete(0, "end")
    ai_name_entry.insert(0, config_values.get("ai_name", ""))

    ai_first_name_entry.delete(0, "end")
    ai_first_name_entry.insert(0, config_values.get("ai_first_name", ""))

    speaker_entry.delete(0, "end")
    speaker_entry.insert(0, config_values.get("speaker", ""))

app = tk.Tk()
app.title("Thiết lập cho bot")

# Character Info
character_label = tk.Label(app, text="Bot Info:")
character_label.pack()
character_text = tk.Text(app, height=5, width=40)
character_text.pack()

# User Info
user_label = tk.Label(app, text="User Info:")
user_label.pack()
user_text = tk.Text(app, height=5, width=40)
user_text.pack()

# Entry fields for specific configuration values
openai_key1_label = tk.Label(app, text="Openai key 1:")
openai_key1_label.pack()
openai_key1_entry = tk.Entry(app)
openai_key1_entry.pack()

openai_key2_label = tk.Label(app, text="Openai key 2:")
openai_key2_label.pack()
openai_key2_entry = tk.Entry(app)
openai_key2_entry.pack()

discord_bot_key_label = tk.Label(app, text="Discord bot token:")
discord_bot_key_label.pack()
discord_bot_key_entry = tk.Entry(app)
discord_bot_key_entry.pack()

vv_key_label = tk.Label(app, text="VoiceVox API key:")
vv_key_label.pack()
vv_key_entry = tk.Entry(app)
vv_key_entry.pack()

user_id_label = tk.Label(app, text="User id:")
user_id_label.pack()
user_id_entry = tk.Entry(app)
user_id_entry.pack()

ai_name_label = tk.Label(app, text="Bot Name")
ai_name_label.pack()
ai_name_entry = tk.Entry(app)
ai_name_entry.pack()

ai_first_name_label = tk.Label(app, text="Bot first name:")
ai_first_name_label.pack()
ai_first_name_entry = tk.Entry(app)
ai_first_name_entry.pack()

speaker_label = tk.Label(app, text="Bot VoiceVox voice id")
speaker_label.pack()
speaker_entry = tk.Entry(app)
speaker_entry.pack()

load_config_values()  # Tải giá trị từ tệp khi khởi động chương trình

save_and_close_button = tk.Button(app, text="Save and Close", command=lambda: [save_character_info(), save_user_info(), save_config_info(), app.quit()])
save_and_close_button.pack()

app.mainloop()