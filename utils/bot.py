#♥️♥️

import discord
import threading
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import View, button

import re
import logging
import asyncio
import random
import json
import datetime
import pytz
import math
import time

import utils.status as status
from utils.private_files import *
from user_files.config import *
from utils.openai_call import *
from utils.tts import *
from utils.translate import *
from utils.voice_message import *
from utils.noperm import noperm

logging.getLogger('discord.gateway').setLevel(logging.ERROR)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)
ai_full_name = f"{ai_name} {ai_first_name}"
channel_id = 0
dm_channel_id = 0

rmv_bt = discord.ui.Button(label="⚜️", custom_id="remove", style=discord.ButtonStyle.grey)
irmv_bt = discord.ui.Button(label="⚜️", custom_id="remove", style=discord.ButtonStyle.grey)
rc_bt = discord.ui.Button(label="💫 re chat", custom_id="rc", style=discord.ButtonStyle.grey)
continue_bt = discord.ui.Button(label="✨ continue", custom_id="continue", style=discord.ButtonStyle.grey)
nt_bt = discord.ui.Button(label="🔆 next", custom_id="next", style=discord.ButtonStyle.green)
bk_bt = discord.ui.Button(label="🔅 back", custom_id="back", style=discord.ButtonStyle.green)

user_name = "Master"
user_nick = "user"
member = ""
guild = ""
emojis = []

emoji_random = []
emoji_angry = []
emoji_stress = []
emoji_sad = []
emoji_think = []
emoji_stare = []
emoji_sup = []
emoji_happy = []
emoji_hype = []
emoji_love = []
emoji_kiss = []


alarms = []
alarm_check = True
user_stt = "offline"
online = "online"
idle = "idle"
dnd = "dnd"
msg_busy = False
task_busy_with_user = False
task_busy_with_another = False
stt_lang = "auto"
chat_wait = False
call_limit = False
img_prompt = "sky"
img_id = 0
message_states = {}
img_block = "futanari furry bestiality yaoi hairy"

bot_mood = 50.0
split_send = False
day_check = True
night_check = True
console_log = False
emoji_rate = 0.5
total_msg = 0
tts_toggle = False
nsfw = True
public_chat = False
public_chat_num = 2
voice_mode = 'ja'
en_speaker = 'en_18'
beha_down = False

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
    "beha_down": False,
    "img_block": ""
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

emoji_rate_percent = emoji_rate * 100

print(f"{ai_full_name} đang thức dậy!")
print()

# Bot Greeting
@bot.event
async def on_ready():
    print(f"{bot.user.name} đã kết nối tới Discord!")
    # Đồng bộ hoá commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    # Chạy status
    asyncio.create_task(bot_idle())
    bot_idle.start()
    
    asyncio.create_task(time_check())
    time_check.start()

    global alarms
    await member_info()
    alarms = load_alarms_from_json()

    user = await bot.fetch_user(user_id)
    if user.dm_channel is None:
        await user.create_dm()
    dm_channel_id = user.dm_channel.id
    channel = bot.get_channel(dm_channel_id)

    view = View(timeout=None)
    view.add_item(rmv_bt)
    view.add_item(rc_bt)
    view.add_item(continue_bt)
    rc_bt.callback = rc_bt_atv
    rmv_bt.callback = rmv_bt_atv
    irmv_bt.callback = irmv_bt_atv
    continue_bt.callback = ctn_bt_atv
    async for message in channel.history(limit=3):
        if message.author == bot.user:
            if message.content:
                await message.edit(view=view)
                break
    print()

# Check typing

@client.event
async def on_typing(channel, user, when):
    global chat_wait
    if user.id in bot_id:
        chat_wait = True

# AI Chat
@bot.event
async def on_message(message):
    global channel_id, task_busy_with_user, task_busy_with_another, public_chat_num, chat_wait, dm_channel_id
    # Bỏ qua nếu tin nhắn là bot hoặc không phải user được chỉ định
    #if message.author == bot.user:
    #    return
    """if not message.author.bot and message.author.id != user_id:
        user_name = message.author.name
        result = "{}: {}".format(user_name, message.content)
        user_answer_channel(result)
    # Phản hồi lại chat trong channel chung
    if not message.content.startswith('.') and (message.author.id in bot_id or message.author.id == user_id) and public_chat_num != 0:
        if not isinstance(message.channel, discord.DMChannel):
            user_name = message.author.name
            if message.content:
                result = "{}: {}".format(user_name, message.content)
                user_answer_channel(result)
            if not public_chat or task_busy_with_another or task_busy_with_user:
                return
            random_time = random.uniform(1, 3)
            time.sleep(random_time)
            if chat_wait:
                chat_wait = False
                return
            task_busy_with_another = True
            channel_id = message.channel.id
            vals_save('user_files/vals.json', 'channel_id', channel_id)
            if message.content:
                async with message.channel.typing():
                    asyncio.create_task(bot_answer_channel(message))
                #await answer_send_channel(message, result)
            elif message.attachments:
                file_names = []
                file_lists = []
                for attachment in message.attachments:
                    file_names.append(attachment.filename)
                    file_lists.append(message.attachments)
                files = message.attachments[0]
                if console_log:
                    print(file_names)
                    print(file_lists)
                # Nếu là file âm thanh
                if files.content_type.startswith('audio/'):
                    asyncio.create_task(bot_reaction_with_voice_channel(files, message))
            public_chat_num -= 1
            task_busy_with_another = False"""
        
    # Phản hồi lại user sau khi nhận được chat
    if not message.content.startswith('!') and message.author.id == user_id:
        # Chỉ phản hồi khi là DM channel
        if isinstance(message.channel, discord.DMChannel):
            # Nếu đang reply thì bỏ qua
            if task_busy_with_user:
                return
            elif task_busy_with_another:
                return
            dm_channel_id = message.channel.id
            vals_save('user_files/vals.json', 'dm_channel_id', dm_channel_id)
            channel_id = dm_channel_id
            vals_save('user_files/vals.json', 'channel_id', channel_id)

            # Xoá button cũ
            now_msg = message
            async for message in message.channel.history(limit=3):
                if message.author == bot.user:
                    if message.content and not message.content.startswith("🏷️"):
                        await message.edit(view=None)
                        break
            message = now_msg
            # Trường hợp là văn bản:
            if message.content:
                result = message.content
                asyncio.create_task(answer_send(message, result))
            # Trường hợp là tệp đính kèm:
            elif message.attachments:
                file_names = []
                file_lists = []
                for attachment in message.attachments:
                    file_names.append(attachment.filename)
                    file_lists.append(message.attachments)
                files = message.attachments[0]
                if console_log:
                    print(file_names)
                    print(file_lists)
                # Nếu là file âm thanh
                if files.content_type.startswith('audio/'):
                    asyncio.create_task(bot_reaction_with_voice(files, message))
                # Nếu là file khác
                else:
                    lang = lang_detect(get_bot_answer())
                    result = f"*{file_names} has just been sent to you*"
                    if lang == "vi":
                        result = f"*{user_nick} vừa gửi {file_names} cho {ai_name}*"
                    elif lang == "ja":
                        result = f"*{user_nick}から{file_names}が送られてきました*"
                    asyncio.create_task(answer_send(message, result))
            #asyncio.create_task(bot_tasks(message))
    # Tiếp tục thực thi các command
    #await bot.process_commands(message)

# Bot restart
@bot.tree.command(name="renew", description=f"Khởi động lại {ai_name}.")
async def renew(interaction: discord.Interaction):
    if interaction.user.id == user_id:
        if bot_mood < 250:
            await interaction.response.send_message(f"`{ai_name} sẽ quay lại ngay sau 3s...`", ephemeral=True)
            await bot.close()
        else:
            await interaction.response.send_message(f"❤️❔🔪", ephemeral=True)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Cuộc trò chuyện mới
@bot.tree.command(name="newchat", description="Cuộc trò chuyện mới.")
async def newchat(interaction: discord.Interaction):
    global bot_mood
    if interaction.user.id == user_id:
        if bot_mood < 250:
            clear_conversation_history()
            bot_mood = 50
            vals_save('user_files/vals.json', 'bot_mood', bot_mood)

            await interaction.response.send_message(f"`{ai_name} đã làm mới cuộc trò chuyện.`", ephemeral=True)
        else:
            await interaction.response.send_message(f"❤️❤️❤️❔🔪", ephemeral=True)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Cuộc trò chuyện mới trong server
@bot.tree.command(name="clearchat", description="Cuộc trò chuyện public mới.")
async def new_pchat(interaction: discord.Interaction):
    if interaction.user.id == user_id:
        clear_conversation_history_public()
        await interaction.response.send_message(f"`{ai_name} đã làm mới cuộc trò chuyện public.`", ephemeral=True)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Tạo lại câu trả lời
@bot.tree.command(name="delchat", description=f"Xoá chat của {ai_name}.")
async def answer_regen(interaction: discord.Interaction):
    if interaction.user.id == user_id:
        if bot_mood < 250:
            await interaction.response.send_message(f"_{ai_name} đang xoá chat..._", delete_after = 1)
            if console_log:
                print(f"Đang xoá các tin nhắn của {ai_name}...")
            # Xác định số lượng tin nhắn của bot cần xoá
            limit = 0
            async for message in interaction.channel.history():
                if message.author == bot.user:
                    limit += 1
                elif message.author == interaction.user:
                    break
            if limit != 0:
                await delete_messages(interaction, limit)
                # Xoá câu trả lời trước đó
            remove_bot_answer()
            user = await bot.fetch_user(user_id)
            if user.dm_channel is None:
                await user.create_dm()
            dm_channel_id = user.dm_channel.id
            channel = bot.get_channel(dm_channel_id)

            view = View(timeout=None)
            view.add_item(rmv_bt)
            view.add_item(rc_bt)
            view.add_item(continue_bt)
            rc_bt.callback = rc_bt_atv
            rmv_bt.callback = rmv_bt_atv
            continue_bt.callback = ctn_bt_atv
            async for message in channel.history(limit=3):
                if message.author == bot.user:
                    if message.content:
                        await message.edit(view=view)
                        break
        else:
            await interaction.response.send_message(f"✖️🔪", ephemeral=True)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Check user status
@bot.tree.command(name="status", description=f"Trạng thái hoạt động của {user_nick}.")
async def us_status(interaction: discord.Interaction):
    if interaction.user.id == user_id:
        user_stt = "offline"
        # Check user_stt status
        user_stt = user_stt_check()
        await interaction.response.send_message(f"`trạng thái hoạt động của {user_nick} là {user_stt}`", ephemeral=True)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Chat log
@bot.tree.command(name="chatlog", description=f"Hiển thị log chat ra console. Total chat: {total_msg}")
async def chatlog(interaction: discord.Interaction):
    global console_log
    if interaction.user.id == user_id:
        if console_log:
            case = "tắt"
            console_log = False
        else:
            case = "bật"
            console_log = True
        await interaction.response.send_message(f"`Log chat ra console đã được {case}`", ephemeral=True)
        vals_save('user_files/vals.json', 'console_log', console_log)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Behavior prompt mode up/down
@bot.tree.command(name="bemode", description=f"Đổi mode behavior. Reverse: {beha_down}")
async def bemode(interaction: discord.Interaction):
    global beha_down
    if interaction.user.id == user_id:
        if beha_down:
            case = "tắt"
            beha_down = False
        else:
            case = "bật"
            beha_down = True
        await interaction.response.send_message(f"`Chế độ đảo behavior đã {case}`", ephemeral=True)
        vals_save('user_files/vals.json', 'beha_down', beha_down)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Thay đổi tỷ lệ tương tác emoji
@bot.tree.command(name="erate", description=f"Tỷ lệ tương tác emoji của {ai_name}: {emoji_rate_percent}%")
async def emo_rate(interaction: discord.Interaction, rate: int):
    global emoji_rate
    if interaction.user.id == user_id:
        if rate == 0:
            case = "sẽ không tương tác emoji nữa."
        elif rate < 40:
            case = "sẽ hạn chế tương tác emoji."
        elif rate < 70:
            case = "sẽ hay tương tác emoji."
        elif rate <= 100:
            case = "sẽ thường xuyên tương tác emoji."
        else:
            pass
        if 0 <= rate <= 100:
            emoji_rate = rate / 100.0  # Chuyển đổi giá trị từ 0-100 thành 0-0.9
            await interaction.response.send_message(f"`{ai_name} {case}`", ephemeral=True)
            vals_save('user_files/vals.json', 'emoji_rate', emoji_rate)
        else:
            await interaction.response.send_message("`Hãy nhập giá trị từ 0 đến 100.`")
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Lưu lời nhắc
@bot.tree.command(name="remind", description=f"Nhắc {user_nick} khi tới giờ.")
async def reminder(interaction: discord.Interaction, note: str, time: str, date: str = None):
    if interaction.user.id == user_id:
        try:
            current_date = datetime.datetime.now()
            if date is not None:
                date_str = f"{date} {time}"
                alarm_time = datetime.datetime.strptime(date_str, "%d/%m %H:%M")
                alarm_time = alarm_time.replace(year=current_date.year)  # Thêm năm hiện tại
            else:
                date_str = current_date.strftime(f"%d-%m-{current_date.year}")  # Sử dụng ngày hiện tại nếu không có date
                alarm_time = datetime.datetime.strptime(f"{date_str} {time}", "%d-%m-%Y %H:%M")
            
            alarms.append((alarm_time, note))
            if date == None:
                date = ""
            save_alarms_to_json(alarms)
            await interaction.response.send_message(f"`{ai_name} sẽ nhắc {user_nick} {note} vào {time} {date}.`", ephemeral=True)
        except ValueError:
            await interaction.response.send_message('`Định dạng ngày hoặc thời gian không hợp lệ. Hãy sử dụng định dạng "DD/MM" cho ngày và "H:M" cho thời gian`')
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Danh sách lời nhắc
@bot.tree.command(name="remindlist", description=f"Danh sách lời nhắc.")
async def reminder_list(interaction: discord.Interaction):
    if interaction.user.id == user_id:
        if not alarms:
            await interaction.response.send_message('`Hiện không có lời nhắc nào.`', ephemeral=True)
        else:
            alarm_list = '\n'.join([f'{index}: {alarm[0]} - {alarm[1]}' for index, alarm in enumerate(alarms)])
            await interaction.response.send_message(f'```Danh sách lời nhắc:\n{alarm_list}```', ephemeral=True)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Xoá lời nhắc
@bot.tree.command(name="remindremove", description=f"Xóa lời nhắc cho {user_nick}.")
async def reminder_remover(interaction: discord.Interaction, index: int):
    if interaction.user.id == user_id:
        if index < 0 or index >= len(alarms):
            await interaction.response.send_message('`Lời nhắc không tồn tại.`', ephemeral=True)
            return
        
        removed_alarm = alarms.pop(index)
        
        save_alarms_to_json(alarms)
        
        await interaction.response.send_message(f"`{ai_name} đã xóa lời nhắc cho {user_nick}: {removed_alarm[1]} vào {removed_alarm[0]}.`", ephemeral=True)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Đổi mode voice chat
@bot.tree.command(name="vchat", description=f"Ngôn ngữ voice chat của {ai_name}: [{voice_mode}].")
async def voice_chat(interaction: discord.Interaction, language: str = None):
    global tts_toggle, voice_mode, en_speaker
    if interaction.user.id == user_id:
        text = f"{ai_name} sẽ không gửi voice chat nữa."
        if language is None:
            tts_toggle = False
        elif re.search('ja', language.lower()):
            if len(vv_key) == 15:
                tts_toggle = True
                text = f"{ai_name} sẽ gửi voice chat bằng Japanese"
                voice_mode = "ja"
                en_speaker = speaker
            else:
                await interaction.response.send_message(f"`Hãy nhập VoiceVox api-key trước khi bật nó.`", ephemeral=True)
        else:
            tts_toggle = True
            text = f"{ai_name} sẽ gửi voice chat bằng English"
            voice_mode = "en"
        await interaction.response.send_message(f"`{text}`", ephemeral=True)
        vals_save('user_files/vals.json', 'tts_toggle', tts_toggle)
        vals_save('user_files/vals.json', 'voice_mode', voice_mode)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Thiết lập voice chat
@bot.tree.command(name="vconfig", description=f"Voice chat config: Spr:{en_speaker}, P:{pitch}, I:{intonation_scale}, Spd{speed}.")
async def voice_config(interaction: discord.Interaction, vspeaker: int, vpitch: float = None, vintonation: float = None, vspeed: float = None):
    global en_speaker, speaker, pitch, intonation_scale, speed
    if interaction.user.id == user_id:
        if voice_mode == "en":
            if 1 > speaker > 117:
                await interaction.response.send_message("`Voice English không tồn tại, chọn voice từ 1 -> 117.`", ephemeral=True)
                return
            name = "en_"
            en_speaker = name + str(vspeaker)
            vals_save('user_files/vals.json', 'en_speaker', en_speaker)

        if voice_mode == "ja":
            if vspeaker > 75:
                await interaction.response.send_message("`Voice Japanese không tồn tại, chọn voice từ 0 -> 75.`", ephemeral=True)
                return
            
            speaker = vspeaker
            vals_save('user_files/vals.json', 'speaker', speaker)
            if vpitch is not None:
                if -0.15 > vpitch > 0.15:
                    await interaction.response.send_message("`Pitch(cao độ) không hợp lệ, chọn pitch từ -0.15 -> 0.15.`", ephemeral=True)
                    return
                pitch = vpitch
                vals_save('user_files/vals.json', 'pitch', pitch)
            if vintonation is not None:
                if 0 > vintonation > 2:
                    await interaction.response.send_message("`Intonation(diễn cảm) không hợp lệ, chọn intonation từ 0 -> 2.`", ephemeral=True)
                    return
                intonation_scale = vintonation
                vals_save('user_files/vals.json', 'intonation_scale', intonation_scale)
            if vspeed is not None:
                if 0.5 > vspeed > 2:
                    await interaction.response.send_message("`Speed(tốc độ) không hợp lệ, chọn speed từ 0.5 -> 2.`", ephemeral=True)
                    return
                speed = vspeed
                vals_save('user_files/vals.json', 'speed', speed)

        await interaction.response.send_message(f"`Đã lưu thiết lập voice. Speaker:{vspeaker}, pitch:{pitch}, intonation:{intonation_scale}, speed:{speed}.`", ephemeral=True)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# NSFW toggle
@bot.tree.command(name="nsfw", description=f"{ai_name} nsfw mode.")
async def nsfw_chat(interaction: discord.Interaction):
    global nsfw
    if interaction.user.id == user_id:
        text = f"tắt"
        if nsfw:
            nsfw = False
        else:
            nsfw = True
            text = f"bật"
        await interaction.response.send_message(f"`NSFW mode đã {text}.`", ephemeral=True)
        vals_save('user_files/vals.json', 'nsfw', nsfw)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Public chat toggle
@bot.tree.command(name="pchat", description=f"Cho phép {ai_name} chat public. limit: {public_chat_num}")
async def public_bot_chat(interaction: discord.Interaction, limit: int = None):
    global nsfw, public_chat_num, public_chat
    if interaction.user.id == user_id:
        text = f"tắt"
        if limit == None or limit == 0:
            public_chat = False
        elif 4 > limit > 0:
            public_chat = True
            text = f"bật"
        else:
            await interaction.response.send_message(f"`{ai_name} chỉ có thể chat tối đa 3 tin nhắn public trong 3 phút.`", ephemeral=True)
        public_chat_num = limit
        await interaction.response.send_message(f"`Public chat đã {text}.`", ephemeral=True)
        vals_save('user_files/vals.json', 'public_chat_num', public_chat_num)
        vals_save('user_files/vals.json', 'public_chat', public_chat)
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Image Gen
@bot.tree.command(name="igen", description=f"Tạo art")
async def image_gen(interaction: discord.Interaction, prompt: str):
    if interaction.user.id == user_id:
        global img_prompt, img_id, bot_mood
        img_prompt = prompt
        guild = bot.get_guild(server_id)
        emojis = guild.emojis
        emoji = random.choice(emojis)
        embed = discord.Embed(title=f"Image đang được tạo... {emoji}", color=discord.Color.blue())
        view = View(timeout=None)
        view.add_item(irmv_bt)
        await interaction.response.send_message(embed=embed, view=view)
        mess = f"*Sent {user_nick} an image: {prompt}*"
        his = get_bot_answer()
        if his:
            lang = lang_detect(his)
            if "vi" in lang:
                mess = f"*Gửi cho {user_nick} hình ảnh: {prompt}"
        bot_answer_save(mess)
        image_url = await openai_images(prompt)
        # Tạo một Embed để gửi hình ảnh
        embed = discord.Embed(description=f"{prompt}", color=discord.Color.blue())
        embed.set_image(url=image_url)
        # Gửi embed lên kênh
        async for message in interaction.channel.history(limit=1):
            img_id = message.id
            await message.edit(embed=embed)
        bot_mood +=1
        if isinstance(interaction.channel, discord.DMChannel):
            rate = (0.2/(bot_mood*2))*100
            if random.random() < rate:
                case = f"Please say something about the beautiful illustation that {user_nick} just requested."
                asyncio.create_task(bot_imgreact_answer(interaction, case))
    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)

# Image Search
@bot.tree.command(name="isrc", description=f"Tìm art")
async def image_search(interaction: discord.Interaction, keywords: str, limit: int=1, page: int=1, block: str=None):
    if interaction.user.id == user_id:
        import booru
        global img_block, message_states, bot_mood
        if block is not None:
            vals_save('user_files/vals.json', 'img_block', block)
        if limit > 100:
            limit = 100
        temp_limit = 1
        index = 0
        img_urls = ""
        link = ""
        imgs = []
        fix_kws = keywords
        if nsfw and isinstance(interaction.channel, discord.DMChannel):
            if block is None:
                block = img_block
            try:
                se = booru.Gelbooru()
                fix_kws = await fix_src(se, keywords)
                img_urls = await se.search(query=fix_kws, block=block, limit=temp_limit, page=page)
                img = booru.resolve(img_urls)
                for image in img:
                    img_info = {
                        'file_url': image['file_url'],
                        'post_url': image['post_url'],
                        'rating': image['rating']
                    }
                    imgs.append(img_info)
            except Exception as e:
                await interaction.response.send_message(f"Không có art nào có tag '{keywords}' cả.", ephemeral=True)
                print("Image search:", str(e))
                return
        
        else:
            if block is None:
                block = img_block
            try:
                se = booru.Safebooru()
                fix_kws = await fix_src(se, keywords)
                img_urls = await se.search(query=fix_kws, block=block, limit=temp_limit, page=page)
                img = booru.resolve(img_urls)
                for image in img:
                    img_info = {
                        'file_url': image['file_url'],
                        'post_url': image['post_url'],
                        'rating': image['rating']
                    }
                    imgs.append(img_info)
            except Exception as e:
                await interaction.response.send_message(f"Không có art nào có tag '{keywords}' cả.", ephemeral=True)
                print("Image search:", str(e))
                return
            
        if not img_urls:
            await interaction.response.send_message(f"Không có art nào với '{keywords}'", ephemeral=True)
            return
        num_l = "❔"
        if not limit:
            num_l = 1
        link = imgs[0]['post_url']
        embed = discord.Embed(title="", url=imgs[0]['file_url'], description=f"🏷️ [{fix_kws}]({imgs[0]['post_url']})", color=discord.Color.blue())
        embed.add_field(name=f"{int_emoji(index+1)}🔹{num_l}        💟 {imgs[0]['rating']}", value="", inline=False)
        embed.set_image(url=imgs[0]['file_url'])

        async def update_embed(interaction, index, img_url, num, tags):
        # Tạo một Embed mới với URL hình ảnh mới từ img_urls
            emoji = "💟"
            if img_url['rating'] == "general":
                emoji = random.choice(emoji_happy)
            elif img_url['rating'] == "questionable":
                emoji = random.choice(emoji_hype)
            elif img_url['rating'] == "sensitive":
                emoji = random.choice(emoji_love)
            elif img_url['rating'] == "explicit":
                emoji = random.choice(emoji_kiss)
            else:
                emoji = random.choice(emoji_stare)
            link_bt.url = img_url['post_url']
            view.remove_item(link_bt)
            view.add_item(link_bt)
            new_embed = discord.Embed(title="", url=img_url['file_url'], description=f"🏷️ [{tags}]({img_url['post_url']})", color=discord.Color.blue())
            new_embed.add_field(name=f"{int_emoji(index+1)}🔹{int_emoji(num)}       {emoji} {img_url['rating']}", value="", inline=False)
            new_embed.set_image(url=img_url['file_url'])
            url = img_url['file_url']
            if url.endswith((".mp4", ".webp")):
                await interaction.response.edit_message(content=f"🏷️ [{tags}]({img_url['file_url']})\n\n{int_emoji(index+1)}🔹{int_emoji(num)}      {emoji} {img_url['rating']}", embed=None, view=view)
            else:
                await interaction.response.edit_message(content=None, embed=new_embed, view=view)

        async def nt_bt_atv(interaction):
            nonlocal index
            global bot_mood
            msg_id = interaction.message.id
            imgs_2 = message_states.get(msg_id, {"index": 0, "tags": "", "imgs": []})
            num = len(imgs_2["imgs"]) - 1
            index = imgs_2["index"]
            tags = imgs_2["tags"]
            if index < (num-1):
                index += 1
            else:
                index = 0  # Trở về link đầu nếu chạm giới hạn
            img_url = imgs_2["imgs"][index]
            await update_embed(interaction, index, img_url, num, tags)
            message_states[msg_id] = {"index": index, "tags": tags, "imgs": imgs_2["imgs"]}
            bot_mood += 0.1

        async def bk_bt_atv(interaction):
            nonlocal index
            global bot_mood
            msg_id = interaction.message.id
            imgs_2 = message_states.get(msg_id, {"index": 0, "tags": "", "imgs": []})
            num = len(imgs_2["imgs"]) - 1
            index = imgs_2["index"]
            tags = imgs_2["tags"]
            if index > 0:
                index -= 1
            else:
                index = (num-1)  # Trở về link cuối nếu chạm giới hạn
            img_url = imgs_2["imgs"][index]
            await update_embed(interaction, index, img_url, num, tags)
            message_states[msg_id] = {"index": index, "tags": tags, "imgs": imgs_2["imgs"]}
            bot_mood += 0.1

        link_bt = discord.ui.Button(label="〽️", url=link, style=discord.ButtonStyle.grey)
        view = View(timeout=None)
        view.add_item(irmv_bt)
        view.add_item(bk_bt)
        view.add_item(nt_bt)
        view.add_item(link_bt)
        bk_bt.callback = bk_bt_atv
        nt_bt.callback = nt_bt_atv
        await interaction.response.send_message(embed=embed, view=view)
        bot_mood += 1
        if nsfw and isinstance(interaction.channel, discord.DMChannel):
            if block is None:
                block = img_block
            try:
                se = booru.Gelbooru()
                img_urls = await se.search(query=fix_kws, block=block, limit=limit, page=page)
                img = booru.resolve(img_urls)
                for image in img:
                    img_info = {
                        'file_url': image['file_url'],
                        'post_url': image['post_url'],
                        'rating': image['rating']
                    }
                    imgs.append(img_info)
            except Exception as e:
                print("Error img search:", str(e))

        else:
            if block is None:
                block = img_block
            try:
                se = booru.Safebooru()
                img_urls = await se.search(query=fix_kws, block=block, limit=limit, page=page)
                img = booru.resolve(img_urls)
                for image in img:
                    img_info = {
                        'file_url': image['file_url'],
                        'post_url': image['post_url'],
                        'rating': image['rating']
                    }
                    imgs.append(img_info)
            except Exception as e:
                print("Error img search:", str(e))
        async for message in interaction.channel.history(limit=1):
            msg_id = message.id
            message_states[msg_id] = {"index": index, "tags": fix_kws, "imgs": imgs}
        
        skip_first_bot_message = False
        async for message in interaction.channel.history(limit=3):
            if message.author == bot.user:
                if skip_first_bot_message:
                    if message.content and not message.content.endswith((".mp4", ".webp")):
                        await message.edit(view=None)
                    break
                else:
                    skip_first_bot_message = True

        if isinstance(interaction.channel, discord.DMChannel):
            mess = f"*Sent illustartions of {fix_kws}'s content when {user_nick} asked.*"
            his = get_bot_answer()
            if his:
                lang = lang_detect(his)
                if "vi" in lang:
                    mess = f"*Đã gửi cho {user_nick} illustartions: {fix_kws}.*"
            bot_answer_save(mess)
            rate = (0.2/((bot_mood+1)*2))*100
            if random.random() < rate:
                if nsfw:
                    case = f"Please say something about the illustation that {user_nick} just requested, don't forget to tease them!"
                else:
                    case = f"Please say something about the illustation that {user_nick} just requested."
                asyncio.create_task(bot_imgreact_answer(interaction, case))
        
        guild = bot.get_guild(server_id)
        emojis = guild.emojis
        emoji_split(emojis)

    else:
        randaw = noperm_answ()
        await interaction.response.send_message(f"`{randaw}`", ephemeral=True)


# Button call
async def irmv_bt_atv(interaction):
    try:
        await interaction.response.send_message(f" ", delete_after = 0)
    except:
        pass
    await interaction.message.delete()

async def rmv_bt_atv(interaction):
    try:
        await interaction.response.send_message(f" ", delete_after = 0)
    except:
        pass
    if not interaction.message.content.startswith('`Error'):
        remove_near_answer()
        remove_nearest_user_answer()
    await interaction.message.delete()

    user = await bot.fetch_user(user_id)
    if user.dm_channel is None:
        await user.create_dm()
    channel_id = user.dm_channel.id
    channel = bot.get_channel(channel_id)
    del_view = View(timeout=None)
    del_view.add_item(irmv_bt)
    irmv_bt.callback = irmv_bt_atv
    view = View(timeout=None)
    view.add_item(rmv_bt)
    view.add_item(rc_bt)
    view.add_item(continue_bt)
    rc_bt.callback = rc_bt_atv
    rmv_bt.callback = rmv_bt_atv
    continue_bt.callback = ctn_bt_atv
    async for message in channel.history(limit=3):
        if message.author == bot.user:
            if not message.content and not message.content.endswith("🏷️") and message.attachments:
                await message.delete()
            elif message.content:
                await message.edit(view=view)
                break

async def rc_bt_atv(interaction):
    try:
        await interaction.response.send_message(f" ", delete_after = 0)
    except:
        pass
    asyncio.create_task(bot_regen_answer(interaction))

async def ctn_bt_atv(interaction):
    try:
        await interaction.response.send_message(f" ", delete_after = 0)
    except:
        pass
    asyncio.create_task(bot_continue_answer(interaction))

def int_emoji(num):
    emoji_digits = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣'
    }

    if num == 0:
        return emoji_digits['0']

    emoji_str = ""
    is_negative = False

    if num < 0:
        is_negative = True
        num = abs(num)

    if num < 10:
        emoji_str = emoji_digits['0'] + emoji_digits[str(num)]
    else:
        while num > 0:
            digit = num % 10
            emoji_str = emoji_digits[str(digit)] + emoji_str
            num //= 10

    if is_negative:
        emoji_str = '➖' + emoji_str

    return emoji_str


# Correct search
async def fix_src(engine, keywords):
    import booru
    tags = keywords.split(",") if "," in keywords else keywords.split()
    tasks = []
    for tag in tags:
        task = asyncio.create_task(engine.find_tags(query=tag))
        tasks.append(task)
    found_tags = []
    results = await asyncio.gather(*tasks)
    for tag_result in results:
        tag_result = booru.resolve(tag_result)
        if tag_result:
            found_tags.append(tag_result[0])
    if found_tags:
        tags_str = " ".join(found_tags)
    else:
        tags_str = ""
    
    return tags_str

# Save json
def vals_save(file_name, variable_name, variable_value):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            data = json.load(file)
        data[variable_name] = variable_value
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(data, file)
    except FileNotFoundError:
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(data, file)
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Load json
def vals_load(file_name, variable_name):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            data = json.load(file)
        variable_value = data[variable_name]
        return variable_value
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

# Random noperm
def noperm_answ():
    random_response = random.choice(noperm)
    random_response = random_response.format(user_nick=user_nick, ai_name=ai_name)
    return random_response

# Xoá câu trả lời
async def delete_messages(interaction, limit):
    messages = []
    async for message in interaction.channel.history(limit=limit):
        if message.author == bot.user:
            messages.append(message)
    
    for message in messages:
        time.sleep(1)
        await message.delete()

# Gửi câu trả lời của bot vào channel
async def answer_send(message, result):
    asyncio.create_task(count_msg())
    user_answer(result)
    if console_log:
        print()
        print(result)
    async with message.channel.typing():
        ai_text = await bot_answer()
        await msg_send(message, ai_text)
    asyncio.create_task(bot_tasks(message))

# Gửi câu trả lời của bot vào channel chung
async def answer_send_channel(message, result):
    asyncio.create_task(count_msg())
    user_answer_channel(result)
    if console_log:
        print()
        print(result)
    async with message.channel.typing():
        ai_text = bot_answer_channel(message)
        await msg_send(message, ai_text)

# Bot rep limit
async def rep_limit():
    global call_limit
    call_limit = True
    await asyncio.sleep(21)  # Đợi trong 21 giây
    call_limit = False

# Tạo câu trả lời cho bot
async def bot_answer():
    # Gọi Openai
    answer = "`Error error`"
    if not call_limit:
        try:
            await openai_answer()
            answer = get_bot_answer()
        except Exception as e:
            error_message = str(e)
            if "Rate limit reached" in error_message:
                answer = "`Error: Please wait for me in 20s`"
                await rep_limit()
            elif "The server is overloaded or not ready yet" in error_message:
                await openai_answer()
            else:
                answer = "`Error error`"
            print("Error OPEN-AI:", error_message)
    else:
        answer = "`Error: Please wait for me in 20s`"
    # Lấy câu trả lời sau khi hoàn thành phản hồi từ openai
    if console_log:
        print(f"[{ai_name}]:", answer)
    return answer

async def bot_answer_2(case):
    # Gọi Openai
    answer = "`Error error`"
    if not call_limit:
        try:
            answer = await openai_task(case)
        except Exception as e:
            error_message = str(e)
            if "Rate limit reached" in error_message:
                answer = "`Error: Please wait for me in 20s`"
                await rep_limit()
            elif "The server is overloaded or not ready yet" in error_message:
                answer = await openai_task(case)
            else:
                answer = "`Error error`"
            print("Error OPEN-AI:", error_message)
        asyncio.create_task(count_msg())
    else:
        answer = "`Error: Please wait for me in 20s`"
    # Lấy câu trả lời sau khi hoàn thành phản hồi từ openai
    if console_log:
        print(f"[{ai_name}]:", answer)
    return answer

# Tạo câu trả lời cho bot với trường hợp trong channel
async def bot_answer_channel(message):
    # Gọi Openai
    try:
        openai_answer_channel()
    except Exception as e:
        print("Error OPEN-AI: {0}".format(e))
        await bot_error_notice(e)
    # Lấy câu trả lời sau khi hoàn thành phản hồi từ openai
    answer = get_bot_answer_channel()
    if console_log:
        print(f"[{ai_name}]:", answer)
    
    await msg_send_channel(message, answer)
    return answer

# Tạo câu trả lời với lời nhắc
async def bot_remind_answer(user, channel_id, case):
    channel = bot.get_channel(channel_id)
    async with channel.typing():
        ai_text = await bot_answer_2(case)
        await ai_voice_create(ai_text)
        await voice_message(channel_id, console_log)
        await user.send(ai_text)
    skip_first_bot_message = False
    async for message in channel.history(limit=5):
        time.sleep(0.5)
        if message.author == bot.user:
            if skip_first_bot_message:
                if message.content and not message.content.startswith("🏷️"):
                    await message.edit(view=None)
                break
            else:
                # Bỏ qua tin nhắn đầu tiên của bot.user
                skip_first_bot_message = True

# Tạo lại câu trả lời cho bot
async def bot_regen_answer(interaction):
    view = View(timeout=None)
    view.add_item(rmv_bt)
    view.add_item(rc_bt)
    view.add_item(continue_bt)
    remove_near_answer()
    async with interaction.channel.typing():
        ai_text = await bot_answer()
        sentences = await split_text(ai_text)
        paragraph = "\n".join(sentence.strip() for sentence in sentences)
        await interaction.message.edit(content=paragraph, view=view)

# Tạo câu trả lời tiếp tục cho bot
async def bot_continue_answer(interaction):
    clear_view = View()
    view = View(timeout=None)
    view.add_item(rmv_bt)
    view.add_item(rc_bt)
    view.add_item(continue_bt)
    case = "Please continue your actions/words creatively."
    async with interaction.channel.typing():
        ai_text = await bot_answer_2(case)
        if tts_toggle:
            await ai_voice_create(ai_text)
            await voice_message(channel_id, console_log)
        sentences = await split_text(ai_text)
        paragraph = "\n".join(sentence.strip() for sentence in sentences)
        await interaction.message.edit(view=clear_view)
        if "`Error error`" in paragraph:
            pass
        else:
            await interaction.channel.send(paragraph, view=view)
        # Khởi tạo biến đếm để kiểm tra tin nhắn đầu tiên của bot.user
        skip_first_bot_message = False
        async for message in interaction.channel.history(limit=6):
            time.sleep(0.5)
            if message.author == bot.user:
                if skip_first_bot_message:
                    if message.content and not message.content.startswith("🏷️"):
                        await message.edit(view=None)
                    break
                else:
                    # Bỏ qua tin nhắn đầu tiên của bot.user
                    skip_first_bot_message = True

# Báo cho user biết khi lỗi
async def bot_error_notice(error):
    user = await bot.fetch_user(user_id)
    if user.dm_channel is None:
        await user.create_dm()
    await user.send(f"`Error {error}`")

# Nhận dạng gen ảnh
async def bot_imgreact_answer(interaction, case):
    view = View(timeout=None)
    view.add_item(rmv_bt)
    view.add_item(rc_bt)
    view.add_item(continue_bt)
    async with interaction.channel.typing():
        ai_text = await bot_answer_2(case)
        if tts_toggle:
            await ai_voice_create(ai_text)
            await voice_message(channel_id, console_log)
        sentences = await split_text(ai_text)
        paragraph = "\n".join(sentence.strip() for sentence in sentences)
        if "`Error error`" in paragraph:
            pass
        else:
            await interaction.channel.send(paragraph, view=view)

# Nhận dạng voice và trả lời lại
async def bot_reaction_with_voice(files, message):
    result = await openai_audio(files)
    await answer_send(message, result)
    asyncio.create_task(bot_tasks(message))

# Nhận dạng voice và trả lời lại trong channel
async def bot_reaction_with_voice_channel(files, message):
    user_name = message.author.name
    result = await openai_audio(files)
    result = "{}: {}".format(user_name, result)
    await answer_send_channel(message, result)

# Hàm tách dòng:
async def split_text(text):
    sentences = re.split(r'(\*.*?\*|".*?"|\(.*?\))', text)
    # Loại bỏ các chuỗi trống và None trong danh sách
    sentences = [s for s in sentences if s]
    return sentences

# Hàm gửi nhiều tin nhắn theo từng câu:
async def splits_send(message, text):
    if text:
        if tts_toggle:
            await ai_voice_create(text)
            await voice_message(channel_id, console_log)

        sentences = await split_text(text)
        for sentence in sentences:
            if sentence.strip():
                await message.channel.send(sentence)
                asyncio.create_task(count_msg())

# Hàm gửi tin nhắn theo một lần
async def msg_send(message, text):
    global bot_mood
    if text:
        if tts_toggle:
            await ai_voice_create(text)
            await voice_message(channel_id, console_log)

        sentences = await split_text(text)
        # Gộp các câu thành một đoạn văn bản
        paragraph = "\n".join(sentence.strip() for sentence in sentences)
        if bot_mood > 250:
            if "sorry" in paragraph:
                bot_mood -= 80
            if "hurt" in paragraph:
                bot_mood -= 250
            if bot_mood < 0:
                bot_mood = 1
        view = View(timeout=None)
        view.add_item(rmv_bt)
        view.add_item(rc_bt)
        view.add_item(continue_bt)
        
        rc_bt.callback = rc_bt_atv
        rmv_bt.callback = rmv_bt_atv
        continue_bt.callback = ctn_bt_atv
        if "`Error error`" in paragraph:
            pass
        else:
            rate = (0.2/(bot_mood*2))*100
            if random.random() < rate:
                await message.channel.send(paragraph)
                case = "Continue your answer above proactively and creatively by yourself, follow the line closely, maybe with actions. If the above is a question, don't ask it again."
                asyncio.create_task(bot_imgreact_answer(message, case))
            else:
                await message.channel.send(paragraph, view=view)
        skip_first_bot_message = False
        async for message in message.channel.history(limit=6):
            time.sleep(0.5)
            if message.author == bot.user:
                if skip_first_bot_message:
                    if message.content and not message.content.startswith("🏷️"):
                        await message.edit(view=None)
                else:
                    # Bỏ qua tin nhắn đầu tiên của bot.user
                    skip_first_bot_message = True
        asyncio.create_task(count_msg())

async def msg_send_channel(message, text):
    if text:
        if tts_toggle:
            await ai_voice_create(text)
            await voice_message(channel_id, console_log)

        sentences = await split_text(text)
        # Gộp các câu thành một đoạn văn bản
        paragraph = "\n".join(sentence.strip() for sentence in sentences)
        await message.channel.send(paragraph)
        asyncio.create_task(count_msg())

# Tạo voice cho bot
async def ai_voice_create(ai_text):
    if voice_mode == "ja":
        lang = "ja"
        translated = text_translate(ai_text, lang)
        tts_get(translated, speaker, pitch, intonation_scale, speed, console_log)
    else:
        lang = "en"
        translated = text_translate(ai_text, lang)
        try:
            tts_get_en(ai_text, en_speaker)
        except Exception as e:
            print("Voice En error: {0}".format(e))
            await bot_error_notice('Voice En gen error')

# Phân loại emoji
def emoji_split(emojis):
    global emoji_happy, emoji_sad, emoji_think, emoji_love
    for emoji in emojis:
        emoji_name = emoji.name.lower()
        if re.search(r'angry|bonk', emoji_name):
            emoji_angry.append(emoji)
        elif re.search(r'ded|dead|sleep|yan|suicide', emoji_name):
            emoji_stress.append(emoji)
        elif re.search(r'sad|sock', emoji_name):
            emoji_sad.append(emoji)
        elif re.search(r'huh|think|wink|smug|confused', emoji_name):
            emoji_think.append(emoji)
        elif re.search(r'stare|peak', emoji_name):
            emoji_stare.append(emoji)
        elif re.search(r'surprised|pog|wow|bruh|eh', emoji_name):
            emoji_sup.append(emoji)
        elif re.search(r'happy|joy', emoji_name):
            emoji_happy.append(emoji)
        elif re.search(r'hype|dance', emoji_name):
            emoji_hype.append(emoji)
        elif re.search(r'love|heart|shy|blush', emoji_name):
            emoji_love.append(emoji)
        elif re.search(r'kiss|lewd', emoji_name):
            emoji_kiss.append(emoji)
        else:
            emoji_random.append(emoji)

# Hiểu và thực thi các task theo câu trả lời
async def bot_tasks(message):
    if emoji_rate != 0:
        # Mood check
        mood = 0
        emoji = "\U0001F496"
        case = 1
        answ = "mood: 0"
        check_msg = get_bot_answer()
        try:
            answ = await openai_task(case)
        except Exception as e:
            print("Error OPEN-AI while detect mood: {0}".format(e))
        pattern = r'-?\d+'
        matches = re.findall(pattern, answ)
        if matches:
            mood = int(matches[0])
        else:
            mood = 0
        if check_msg:
            keyword = "love"
            keywordvi = "yêu"
            count = check_msg.count(keyword)
            countvi = check_msg.count(keywordvi)
            if count > 4:
                mood += 310
            if countvi > 4:
                mood += 310
        await mood_change(mood)
        # Schedule
        case = 2

        # Emoji reaction
        mood = int(mood)
        if mood < -8:
            if emoji_angry:
                emoji = random.choice(emoji_angry)
        if -9 < mood < -6:
            if emoji_stress:
                emoji = random.choice(emoji_stress)
        if -7 < mood < -4:
            if emoji_sad:
                emoji = random.choice(emoji_sad)
        if mood == -1:
            if emoji_think:
                emoji = random.choice(emoji_think)
        if mood == 1:
            if emoji_stare:
                emoji = random.choice(emoji_stare)
        if 1 < mood < 4:
            if emoji_sup:
                emoji = random.choice(emoji_sup)
        if 3 < mood < 6:
            if emoji_happy:
                emoji = random.choice(emoji_happy)
        if 5 < mood < 8:
            if emoji_hype:
                emoji = random.choice(emoji_hype)
        if 7 < mood < 10:
            if emoji_love:
                emoji = random.choice(emoji_love)
        if mood == 10:
            if emoji_kiss:
                emoji = random.choice(emoji_kiss)
        if mood == 0:
            if emoji_random:
                emoji = random.choice(emoji_random)

        # Reaction emoji vào chat của user, tỷ lệ dựa theo mood
        probability = sigmoid(mood)
        threshold = 0.1 + (emoji_rate * probability)
        if random.uniform(0, 1) < threshold:
            async for prev_message in message.channel.history(limit=10):
                if prev_message.author.id == user_id:
                    await prev_message.add_reaction(emoji)
                    if console_log:
                        print("Emoji reaction:", emoji)
                    break

# Maybe for gacha?
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# Hàm thay đổi mood
async def mood_change(mood):
    global bot_mood
    new_mood = bot_mood + int(mood)

    # Đảm bảo rằng new_mood không nhỏ hơn 0 và không lớn hơn 310
    if new_mood < 0:
        new_mood = 0
    elif new_mood > 500:
        new_mood = 500

    bot_mood = new_mood

    if console_log:
        print(f"{ai_name} mood:", bot_mood)
    mood_name = mood_name_change(bot_mood)
    asyncio.create_task(bot_status(mood_name))
    vals_save('user_files/vals.json', 'bot_mood', bot_mood)
    return bot_mood

# Cập nhật mood
def mood_name_change(bot_mood):
    mood_name = "normal"
    if bot_mood == 0:
        mood_name = f"sulking with {user_nick}"
    elif bot_mood < 10:
        mood_name = f"sad because of {user_nick}"
    elif bot_mood < 30:
        mood_name = f"a bit lonely"
    elif bot_mood < 60:
        mood_name = "chilling"
    elif bot_mood < 70:
        mood_name = "happily"
    elif bot_mood < 80:
        mood_name = "so happy"
    elif bot_mood < 99:
        mood_name = "feeling loved"
    elif bot_mood < 150:
        mood_name = f"love {user_nick} so much! ♥️"
    elif bot_mood < 250:
        mood_name = f"Obsessive love with {user_nick} ♥️"
    else:
        mood_name = f"Yandere mode on ♥️♥️♥️"

    # Lưu lại mood vào prompt
    with open("user_files/prompt/current_mood.txt", "w", encoding="utf-8") as f:
        mood = f"Your current mood is: {mood_name}"
        f.write(mood)
        f.close()

    return mood_name

# Cập nhật bot mood
async def bot_status(mood_name):
    await status.bot_activ(bot, mood_name)

# Mood tự tụt khi không chat
async def mood_drop():
    global bot_mood, intonation_scale, speed, pitch
    if bot_mood > 250:
        bot_mood -= 25
        old_pitch = pitch
        pitch = -0.05
        old_is = intonation_scale
        intonation_scale = 2
        old_speed = speed
        speed = 0.7
        user = await bot.fetch_user(user_id)
        if user.dm_channel is None:
            await user.create_dm()
        channel_id = user.dm_channel.id
        case = f"You are so obsessed and madly in love with {user_nick}, continue your above chat proactively and creatively by question, or by action if the above is already a question with yandere mode using incorrect words or lengthening the last letter of the last word."
        await bot_remind_answer(user, channel_id, case)
        pitch = old_pitch
        intonation_scale = old_is
        speed = old_speed
    if bot_mood > 200:
        bot_mood -= 10
    if bot_mood > 100:
        bot_mood -= 0.5
    if bot_mood > 90:
        bot_mood -= 2
    if bot_mood > 80:
        bot_mood -= 1
    if bot_mood > 70:
        bot_mood -= 0.4
    if bot_mood > 30:
        bot_mood -= 0.3
    if bot_mood > 10:
        bot_mood -= 0.1
    if bot_mood > 0:
        bot_mood -= 0.05
    if bot_mood < 0:
        bot_mood = 0
    vals_save('user_files/vals.json', 'bot_mood', bot_mood)
    mood_name = mood_name_change(bot_mood)
    await status.bot_activ_non_chat(bot, mood_name)

# Lấy thông tin user
async def member_info():
    global user_name, user_nick, member, guild
    # Lấy thông tin user
    try:
        guild = bot.get_guild(server_id)
        emojis = guild.emojis
        emoji_split(emojis)
        member = guild.get_member(user_id)
        user_name = member.name
        user_nick = member.nick
        if user_nick == None:
            user_nick = user_name
    except Exception as e:
            print("Không thể lấy thông tin user: {0}".format(e))
    
    vals_save('user_files/vals.json', 'user_nick', user_nick)
        
# Check status
def user_stt_check():
    guild = bot.get_guild(server_id)  # Lấy đối tượng máy chủ
    if guild is not None:
        member = guild.get_member(user_id)  # Lấy thông tin member từ ID
        if member is not None:
            user_stt = member.status  # Lấy trạng thái hiện tại của member
            user_stt = str(user_stt)
            if console_log:
                print(f"{member.name} đang {user_stt}.")
        else:
            print("Không tìm thấy user trong server.")
    else:
        print("Không tìm thấy server.")
    return user_stt

# Lưu hoặc load lời nhắc
def save_alarms_to_json(alarms):
    with open('user_files/alarms.json', 'w', encoding="utf-8") as file:
        json.dump(alarms, file, default=str)

def load_alarms_from_json():
    try:
        with open('user_files/alarms.json', 'r', encoding="utf-8") as file:
            alarms = json.load(file)
    except FileNotFoundError:
        alarms = []
        with open('user_files/alarms.json', 'w', encoding="utf-8") as file:
            json.dump(alarms, file, default=str)
    return alarms

# Count chat
async def count_msg():
    global total_msg
    total_msg = total_msg + 1
    vals_save('user_files/vals.json', 'total_msg', total_msg)

# Bot idle or dnd
@tasks.loop(seconds=random.randint(180, 300))
async def bot_idle():
    global public_chat_num
    if bot_mood >= 30:
        await status.bot_status_change(bot)
    elif bot_mood < 30:
        await status.bot_status_change_sad(bot)

    await mood_drop()
    public_chat_num = vals_load('user_files/vals.json', 'public_chat_num')

# Time check
@tasks.loop(seconds=60)
async def time_check():
    global day_check, night_check, alarm_check
    my_timezone = pytz.timezone('Asia/Bangkok')
    vn_time = datetime.datetime.now(my_timezone)

    user = await bot.fetch_user(user_id)
    if user.dm_channel is None:
        await user.create_dm()
    channel_id = user.dm_channel.id
    channel = bot.get_channel(channel_id)
    
    view = View(timeout=None)
    if bot_mood > 250:
        rmv_bt.label="❤️"
        rc_bt.label="❤️"
        continue_bt.label="❤️"
    else:
        rmv_bt.label="⚜️"
        rc_bt.label="💫 re chat"
        continue_bt.label="✨ continue"
    view.add_item(rmv_bt)
    view.add_item(rc_bt)
    view.add_item(continue_bt)
    rc_bt.callback = rc_bt_atv
    rmv_bt.callback = rmv_bt_atv
    continue_bt.callback = ctn_bt_atv
    async for message in channel.history(limit=1):
        if message.author == bot.user:
            if message.content and not message.content.startswith("🏷️"):
                await message.edit(view=view)
                break

    # Wake up check
    if day_check:
        if 6 <= vn_time.hour <= 10:
            user_stt = user_stt_check()
            # Nếu thấy user hoạt động thì chào
            if (user_stt == online) or (user_stt == idle):
                day_check = False
                note = f"Looks like {user_nick} just woke up."
                async with user.typing():
                    asyncio.create_task(bot_remind_answer(user, channel_id, note))
                vals_save('user_files/vals.json', 'day_check', day_check)

    # Sleep check
    if night_check:
        if vn_time.hour >= 22:
            user_stt = user_stt_check()
            # Nếu thấy user onl thì chào
            if (user_stt == online) or (user_stt == idle) or (user_stt == dnd):
                night_check = False
                note = f"it's late now, reminded {user_nick} to go to sleep."
                if user_stt == dnd:
                    note = f"It's time for bed but {user_nick} still working. let wish {user_nick} good night."
                async with user.typing():
                    asyncio.create_task(bot_remind_answer(user, channel_id, note))
                vals_save('user_files/vals.json', 'night_check', night_check)

    # Restart sche
    if 11 <= vn_time.hour <= 12:
        day_check = True
        night_check = True
        vals_save('user_files/vals.json', 'day_check', day_check)
        vals_save('user_files/vals.json', 'night_check', night_check)

    # Alarm
    if alarm_check:
        current_time = vn_time.strftime('%Y-%m-%d %H:%M')
        for alarm in alarms:
            alarm_time, note = alarm
            alarm_time = str(alarm_time)
            alarm_time = alarm_time[:-3]
            if current_time == alarm_time:
                alarm_check = False
                case = "Remind"
                text = f"{case} {user_nick}: {note}"
                asyncio.create_task(bot_remind_answer(user, channel_id, text))
                alarms.remove(alarm)
                save_alarms_to_json(alarms)
    alarm_check = True

def bot_run():
    bot.run(discord_bot_key)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(bot_run())
    loop.run_forever()