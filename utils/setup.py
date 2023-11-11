import tkinter as tk
import re
import customtkinter as des
import json
from customtkinter import CTk, CTkFrame, CTkEntry, CTkLabel, CTkButton, CTkImage
from tkinter import ttk, PhotoImage, filedialog, messagebox
from tkinter import *


# Định nghĩa danh sách các biến và giá trị cần cập nhật
config_updates = {
    "openai_key_1": "",
    "openai_key_2": "",
    "discord_bot_key": "",
    "vv_key": "",
    "user_id": "",
    "server_id": "",
    "speaker": "",
    "pitch": "",
    "intonation_scale": "",
    "speed": ""
}

def save_character_info():
    character_info = character_text.get(1.0, "end-1c")
    if character_info.strip():
        with open(".\\user_files\\prompt\\character.txt", "w", encoding="utf-8") as character_file:
            character_file.write(character_info)

def save_user_info():
    user_info = user_text.get(1.0, "end-1c")
    if user_info.strip():
        with open(".\\user_files\\prompt\\user.txt", "w", encoding="utf-8") as user_file:
            user_file.write(user_info)

def save_character_behavior():
    char_bv = charbv_text.get(1.0, "end-1c")
    if char_bv.strip():
        with open(".\\user_files\\prompt\\behavior.txt", "w", encoding="utf-8") as user_file:
            user_file.write(char_bv)

def save_config_info():
    # Lấy giá trị từ các trường nhập liệu
    openai_key1 = openai_key1_entry.get()
    openai_key2 = openai_key2_entry.get()
    discord_bot_key = discord_bot_key_entry.get()
    vv_key = vv_key_entry.get()
    user_id = user_id_entry.get()
    server_id = server_id_entry.get()
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

    if not speaker:
        speaker = 46
    if not pitch:
        pitch = 0
    if not intonation_scale:
        intonation_scale = 1
    if not speed:
        speed = 1
    config_updates["speaker"] = int(speaker)
    config_updates["pitch"] = float(pitch)
    config_updates["intonation_scale"] = float(intonation_scale)
    config_updates["speed"] = float(speed)

    # Đọc nội dung của tệp cấu hình
    with open(".\\user_files\\config.py", "r", encoding="utf-8") as config_file:
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
    with open(".\\user_files\\config.py", "w", encoding="utf-8") as config_file:
        config_file.writelines(updated_config_contents)



def load_config_values():
    try:
        # Đọc giá trị từ tệp character.txt và điền vào trường nhập liệu
        with open(".\\user_files\\prompt\\character.txt", "r", encoding="utf-8") as character_file:
            character_info = character_file.read()
            character_text.delete(1.0, "end")
            character_text.insert("insert", character_info)

        # Đọc giá trị từ tệp user.txt và điền vào trường nhập liệu
        with open(".\\user_files\\prompt\\user.txt", "r", encoding="utf-8") as user_file:
            user_info = user_file.read()
            user_text.delete(1.0, "end")
            user_text.insert("insert", user_info)
        
        # Đọc giá trị từ tệp behavior.txt và điền vào trường nhập liệu
        with open(".\\user_files\\prompt\\behavior.txt", "r", encoding="utf-8") as charbv_file:
            char_bv = charbv_file.read()
            charbv_text.delete(1.0, "end")
            charbv_text.insert("insert", char_bv)
    except FileNotFoundError:
        pass

    # Đọc giá trị từ tệp cấu hình và điền vào các trường nhập liệu
    config_values = {}
    with open(".\\user_files\\config.py", "r", encoding="utf-8") as config_file:
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

    speaker_entry.delete(0, "end")
    speaker_entry.insert(0, config_values.get("speaker", ""))

    pitch_entry.delete(0, "end")
    pitch_entry.insert(0, config_values.get("pitch", ""))

    intonation_scale_entry.delete(0, "end")
    intonation_scale_entry.insert(0, config_values.get("intonation_scale", ""))

    speed_entry.delete(0, "end")
    speed_entry.insert(0, config_values.get("speed", ""))

    try:
        with open('user_files/vals.json', 'r') as json_file:
            data = json.load(json_file)
            nsfw = data.get('nsfw', False)  # Lấy giá trị của nsfw từ tệp JSON, mặc định là False nếu không tìm thấy
            if nsfw:
                btn_nsfw.select()  # Chọn checkbox nếu nsfw là True
            else:
                btn_nsfw.deselect()  # Bỏ chọn checkbox nếu nsfw là False
    except FileNotFoundError:
        # Xử lý tệp không tồn tại
        pass

def checkbox_changed():
    if btn_nsfw.get() == 1:
        nsfw = True
    else:
        nsfw = False
    vals_save('user_files/vals.json', 'nsfw', nsfw)

# Save json
def vals_save(file_name, variable_name, variable_value):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            data = json.load(file)
        data[variable_name] = variable_value
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(data, file)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


app = des.CTk()
app.title("Character setting")
des.set_appearance_mode("System") 
bg_color_night = "#2c2c2c"
bg_color_day = "#fff"

wrap_color_night = "#2c2c2c"
wrap_color_day = "#fff"

text_color_night = "#2c2c2c"
text_color_day = "#fff"

input_text_day ="#fff"
input_color_day = "#e16d9e"
input_color_night = "#4f4d4e"
app.config(bg=bg_color_night)


# button status
is_on = True





# Center Popup Screen 
width = 878
height = 660
# app.maxsize(width,height)

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

app.geometry('%dx%d+%d+%d' % (width, height, x, y))

app.attributes('-alpha', 0.98)



# Main Frame
main_frame = CTkFrame(app, bg_color=bg_color_night)
main_frame.pack(fill=BOTH, expand=1)
main_frame.pack(padx=40, pady=20)

main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

#Create Canvas
my_canvas = Canvas(main_frame, borderwidth=0, highlightthickness=0, bg=bg_color_night, relief='ridge')
my_canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)


#Add scrollbar to the Canvas
my_scroll = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scroll.pack(side=RIGHT, fill=Y)


# Create another Frame
second_frame = tk.Frame(my_canvas)
# second_frame.columnconfigure([0,1], weight=1)
# second_frame.rowconfigure([0,1,2,3,4], weight=1)
# Add that New frame to a window in the canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")
# apply the grid layout

#Configure the Canvas
my_canvas.configure(yscrollcommand=my_scroll.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
def on_canvas_scroll(event):
    if event.delta > 0:
        my_canvas.yview_scroll(-1, "units")
    else:
        my_canvas.yview_scroll(1, "units")


second_frame.bind("<MouseWheel>", on_canvas_scroll)
my_canvas.bind("<MouseWheel>", on_canvas_scroll)
app.bind("<MouseWheel>", on_canvas_scroll)
my_scroll.pack_forget()

my_canvas.configure(background=bg_color_night)
second_frame.configure(background=bg_color_night)


logo = PhotoImage(file = './images/discord.png')
des.CTkLabel(second_frame, image = logo, text='').grid(columnspan= 2, row=1, padx=0, pady=20)
# Define Our Images
on = PhotoImage(file ="./images/on.png")
off = PhotoImage(file ="./images/off.png")

label = des.CTkLabel(second_frame, text = "Night Mode is On")
label.grid(columnspan= 1, row=0, padx =20, pady = 10)

def button_mode():
   global is_on
   #Determine it is on or off
   if is_on:
      on_button.config(image=off)

      label.configure(text ="Day Mode is On", text_color= text_color_day)
      app.config(bg=bg_color_day)
      my_canvas.configure(background= bg_color_day)
      second_frame.configure(background=bg_color_day)
      on_button.config(activebackground=bg_color_day, bg=bg_color_day)
      prompt_info.configure(bg=wrap_color_day,fg=text_color_night)
      character_voice.configure(bg=wrap_color_day, fg=text_color_night)
      required_info.configure(bg=wrap_color_day, fg=text_color_night)

      #Character Info
      character_label.configure(text_color=text_color_night)
      character_text.configure(fg_color= input_color_day, text_color= input_text_day)
      

      #User Info
      user_label.configure(text_color=text_color_night)
      user_text.configure(fg_color= input_color_day, text_color= input_text_day)

      # Character behavior
      charbv_label.configure(text_color=text_color_night)
      charbv_text.configure(fg_color= input_color_day, text_color= input_text_day)

      #NSFW
      btn_nsfw.configure(fg_color= input_color_day, text_color= text_color_night)

      #Discord bot token
      discord_bot_key_label.configure(text_color=text_color_night)
      discord_bot_key_entry.configure(fg_color= input_color_day, text_color= input_text_day)

      #OPENAI Key 1
      openai_key1_label.configure(text_color=text_color_night)
      openai_key1_entry.configure(fg_color= input_color_day, text_color= input_text_day)

      #OPENAI Key 2
      openai_key2_label.configure(text_color=text_color_night)
      openai_key2_entry.configure(fg_color= input_color_day, text_color= input_text_day)

      #User ID
      user_id_label.configure(text_color=text_color_night)
      user_id_entry.configure(fg_color= input_color_day, text_color= input_text_day)

      #Server ID
      server_id_label.configure(text_color=text_color_night)
      server_id_entry.configure(fg_color= input_color_day, text_color= input_text_day)

      #VoiceVox API Key
      vv_key_label.configure(text_color=text_color_night)
      vv_key_entry.configure(fg_color= input_color_day, text_color= input_text_day)

      #Speaker ID
      speaker_label.configure(text_color=text_color_night)
      speaker_entry.configure(fg_color= input_color_day, text_color= input_text_day)

      #Voice picth
      pitch_label.configure(text_color=text_color_night)
      pitch_entry.configure(fg_color= input_color_day, text_color= input_text_day)

     #Voice intonation
      intonation_scale_label.configure(text_color=text_color_night)
      intonation_scale_entry.configure(fg_color= input_color_day, text_color= input_text_day)

     #Voice speed
      speed_label.configure(text_color=text_color_night)
      speed_entry.configure(fg_color= input_color_day, text_color= input_text_day)

      is_on = False
   else:
      on_button.config(image=on)

      label.configure(text ="Night Mode is On", text_color=text_color_night)
      app.config(bg= bg_color_night)
      my_canvas.configure(background=bg_color_night)
      second_frame.configure(background=bg_color_night)
      on_button.config(activebackground=bg_color_night, bg=bg_color_night)
      prompt_info.configure(bg=wrap_color_night,fg=text_color_day)
      character_voice.configure(bg=wrap_color_night, fg=text_color_day)
      required_info.configure(bg=wrap_color_night, fg=text_color_day)

      #Character Info
      character_label.configure(text_color=text_color_day)
      character_text.configure(fg_color= input_color_night, text_color= text_color_day)

      #User Info
      user_label.configure(text_color=text_color_day)
      user_text.configure(fg_color= input_color_night, text_color= text_color_day)

      # Character behavior
      charbv_label.configure(text_color=text_color_day)
      charbv_text.configure(fg_color= input_color_night, text_color= text_color_day)

      #NSFW
      btn_nsfw.configure(fg_color=input_color_day, text_color=text_color_day)

      #Discord bot token
      discord_bot_key_label.configure(text_color=text_color_day)
      discord_bot_key_entry.configure(fg_color= input_color_night, text_color= text_color_day)

      #OPENAI Key 1
      openai_key1_label.configure(text_color=text_color_day)
      openai_key1_entry.configure(fg_color= input_color_night, text_color= text_color_day)

      #OPENAI Key 2
      openai_key2_label.configure(text_color=text_color_day)
      openai_key2_entry.configure(fg_color= input_color_night, text_color= text_color_day)

      #User ID
      user_id_label.configure(text_color=text_color_day)
      user_id_entry.configure(fg_color= input_color_night, text_color= text_color_day)

      #Server ID
      server_id_label.configure(text_color=text_color_day)
      server_id_entry.configure(fg_color= input_color_night, text_color= text_color_day)

      #VoiceVox API Key
      vv_key_label.configure(text_color=text_color_day)
      vv_key_entry.configure(fg_color= input_color_night, text_color= text_color_day)

      #Speaker ID
      speaker_label.configure(text_color=text_color_day)
      speaker_entry.configure(fg_color= input_color_night, text_color= text_color_day)

      #Voice picth
      pitch_label.configure(text_color=text_color_day)
      pitch_entry.configure(fg_color= input_color_night, text_color= text_color_day)

     #Voice intonation
      intonation_scale_label.configure(text_color=text_color_day)
      intonation_scale_entry.configure(fg_color= input_color_night, text_color= text_color_day)

     #Voice speed
      speed_label.configure(text_color=text_color_day)
      speed_entry.configure(fg_color= input_color_night, text_color= text_color_day)

      is_on = True

      

# Create A Button



# on_.pack(pady = 50)

prompt_info = tk.LabelFrame(second_frame, text="Your character information")
prompt_info.configure(bg=wrap_color_night, fg=text_color_day)
prompt_info.grid(row=2, column=0, padx=20, pady=20)




on_button = Button(second_frame,image = on,bd=0, bg=bg_color_night, activebackground=bg_color_night , text='',command = button_mode)
on_button.grid(columnspan=3, row=0, padx=4, pady=10)
# Character Info

character_label = des.CTkLabel(prompt_info, text="Character Info:\nDescribe your character's personality, appearance, and other information.", text_color=text_color_day)
character_label.grid(row=1, column=0, padx=0, pady=10, sticky="n",columnspan=5)
character_text = des.CTkTextbox(prompt_info, height=100, width= 710, fg_color= input_color_night, border_width=0)
character_text.grid(row=2, column=0, columnspan=4,
                             padx=20, pady=20, sticky="nsew")

# User Info
user_label = des.CTkLabel(prompt_info, text="\nUser info:\nDescribe your name and any other information you want your character to know.", text_color=text_color_day)  
user_label.grid(row=3, column=0, padx=20, pady= 20, columnspan=5, sticky="n")
user_text = des.CTkTextbox(prompt_info, height=100, width=710,border_width=0)
user_text.grid(row=4, column=0, padx=20, pady= 20, columnspan=5, sticky="nsew")

# Character behavior
charbv_label = des.CTkLabel(prompt_info, text="\nCharacter behavior:\nThe way/context in which your character will chat.",text_color=text_color_day)
charbv_label.grid(row=5, column=0, padx=20, pady= 20, columnspan=5, sticky="n")
charbv_text = des.CTkTextbox(prompt_info, height=100, width=710,border_width=0)
charbv_text.grid(row=6, column=0, padx=20, pady= 20, columnspan=5, sticky="nsew")


btn_nsfw = des.CTkCheckBox(prompt_info, text="NSFW", onvalue=1, offvalue=0, fg_color=input_color_day, text_color=text_color_day, command=checkbox_changed)
btn_nsfw.grid(row=5, column=3 ,padx= 0, pady=20)

# User Info
required_info = tk.LabelFrame(second_frame, text="Settings for your character on Discord")
required_info.configure(bg=wrap_color_night, fg=text_color_day)
required_info.grid(row=8, column=0, padx=20, pady=20)




discord_bot_key_label = des.CTkLabel(required_info, text="Discord Bot token:")
discord_bot_key_label.grid(row=9, column=0, 
                              padx=20, pady=20,
                              sticky="ew")
discord_bot_key_entry = des.CTkEntry(required_info, placeholder_text="Enter your Bot token",border_width=0)
discord_bot_key_entry.grid(row=9, column=1,
                            columnspan=4, padx=20,
                            pady=20 ,sticky="nsew")


# Entry fields for specific configuration values
openai_key1_label = des.CTkLabel(required_info, text="Openai key 1:")
openai_key1_label.grid(row=10, column=0,
                            padx=20, pady=20
                            )
openai_key1_entry = des.CTkEntry(required_info, placeholder_text="Enter your Key Open AI 1", width= 200,border_width=0)
openai_key1_entry.grid(row=10, column=1,
                            columnspan=1, padx=20,
                            pady=20)

openai_key2_label = des.CTkLabel(required_info, text="Openai key 2:")
openai_key2_label.grid(row=10, column=2,
                           padx=0, pady=20)

openai_key2_entry = des.CTkEntry(required_info, placeholder_text="Enter your Key Open AI 2", width=200, border_width=0)
openai_key2_entry.grid(row=10, column=3,
                        columnspan=2, padx=20,
                        pady=20)

user_id_label = des.CTkLabel(required_info, text="Discord user ID:")
user_id_label.grid(row=11, column=0, 
                              padx=20, pady=10,
                              sticky="ew")
user_id_entry = des.CTkEntry(required_info, placeholder_text="Enter your User ID", border_width=0)
user_id_entry.grid(row=11, column=1, 
                              padx=20, pady=10,
                              sticky="ew")

server_id_label = des.CTkLabel(required_info, text="Discord server ID:")
server_id_label.grid(row=11, column=2,
                              padx=20, pady=10,
                              sticky="ew")
server_id_entry = des.CTkEntry(required_info, border_width=0, placeholder_text="Server that the bot & you join")
server_id_entry.grid(row=11, column=3, columnspan=4,
                              padx=20, pady=10,
                              sticky="ew")


character_voice = tk.LabelFrame(second_frame, text="Character's voice setting (optional)")
character_voice.configure(bg=wrap_color_night, fg=text_color_day)
character_voice.grid(row=13, column=0, padx=20, pady=20)

vv_key_label = des.CTkLabel(character_voice, text="VoiceVox API key:")
vv_key_label.grid(row=13, column=0, columnspan=1,
                              padx=20, pady=20,
                              sticky="ew")
vv_key_entry = des.CTkEntry(character_voice, placeholder_text="Enter your key Voicevox", border_width=0)
vv_key_entry.grid(row=13, column=1,
                              padx=20, pady=20,
                              sticky="ew")

speaker_label = des.CTkLabel(character_voice, text="\nCharacter speaker ID:")
speaker_label.grid(row=14, column=0)
speaker_entry = des.CTkEntry(character_voice, width=332, border_width=0)
speaker_entry.grid(row=15, column=0, padx=20, pady=20)
                              
pitch_label = des.CTkLabel(character_voice, text="\nVoice pitch:")
pitch_label.grid(row=16, column=0)
pitch_entry = des.CTkEntry(character_voice, width=332, border_width=0)
pitch_entry.grid(row=17, column=0, padx=20, pady=10)

intonation_scale_label = des.CTkLabel(character_voice, text="\nVoice intonation:")
intonation_scale_label.grid(row=14, column=1)
intonation_scale_entry = des.CTkEntry(character_voice, width=332, border_width=0)
intonation_scale_entry.grid(row=15, column=1, padx=20, pady=10)

speed_label = des.CTkLabel(character_voice, text="\nVoice speed:")
speed_label.grid(row=16, column=1)
speed_entry = des.CTkEntry(character_voice, width=332, border_width=0)
speed_entry.grid(row=17, column=1, padx=20, pady=10)

save_and_close_button = des.CTkButton(second_frame, width=300, height=60, text="Save and Close",hover_color="#ff8888",corner_radius=12, command=lambda: [save_character_info(), save_user_info(), save_config_info(), second_frame.quit(),save_character_behavior()])
save_and_close_button.grid(row=20, column=0, padx=20, pady=10)


load_config_values()  # Tải giá trị từ tệp khi khởi động chương trình

app.mainloop()