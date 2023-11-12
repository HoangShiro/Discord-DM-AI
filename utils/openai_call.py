import json
import re
from utils.promptMaker_self import getPrompt, getPrompt_task, getPrompt_channel
from user_files.config import openai_key_1, openai_key_2
from openai import AsyncOpenAI, OpenAI
import aiohttp
from translate import Translator
from utils.translate import lang_detect

total_characters = 0
total_characters_channel = 0
audio_filename = 'user_files/user_audio_msg.wav'

try:
    with open('user_files/conversation.json', "r", encoding="utf-8") as f:
        history = json.load(f)
        conversation = history.get("history", [])
except:
    conversation = []
    # Create a dictionary to hold the message data
    history = {"history": conversation}

try:
    with open('user_files/channel_history.json', "r", encoding="utf-8") as f2:
        history2 = json.load(f2)
        channel_history = history2.get("history", [])
except:
    channel_history = []
    # Create a dictionary to hold the message data
    history2 = {"history": channel_history}

# Ghi câu trả lời của user và bot vào lịch sử
def user_answer(mess):
    conversation.append({'role': 'user', 'content': mess})

def bot_answer_save(mess):
    conversation.append({'role': 'assistant', 'content': mess})

# Lấy câu trả lời của AI từ lịch sử
def get_bot_answer():
    try:
        mess = conversation[-1]['content']
    except Exception as e:
        print("Lỗi khi lấy chat của bot: Chưa có cuộc trò chuyện nào.")
        mess = "Wow!"
    return mess

# Ghi câu trả lời của user vào lịch sử
def user_answer_channel(mess):
    channel_history.append({'role': 'user', 'content': mess})

# Lấy câu trả lời của AI từ lịch sử
def get_bot_answer_channel():
    try:
        mess = channel_history[-1]['content']
    except Exception as e:
        print("Lỗi khi lấy chat của bot: Chưa có cuộc trò chuyện nào.")
        mess = "Xin chào!"
    return mess

# Xoá các câu trả lời gần nhất của AI trong lịch sử
def remove_bot_answer():
    remove = False  # Biến này sẽ đánh dấu khi cần dừng lại
    for i in range(len(conversation) - 1, -1, -1):
        if conversation[i]["role"] == "assistant":
            if remove:  # Kiểm tra nếu đã gặp message của user thì dừng lại
                break
            else:
                del conversation[i]
        elif conversation[i]["role"] == "user":
            remove = True  # Gặp message của user, đánh dấu để dừng lại
    with open('user_files/conversation.json', "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(conversation, f, indent=4)

def remove_near_answer():
    for i in range(len(conversation) - 1, -1, -1):
        if conversation[i]["role"] == "assistant":
            del conversation[i]
            break
    with open('user_files/conversation.json', "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

def remove_near_user_answer():
    for i in range(len(conversation) - 1, -1, -1):
        if conversation[i]["role"] == "user":
            del conversation[i]
            break
    with open('user_files/conversation.json', "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

def remove_nearest_user_answer():
    for i in range(len(conversation) - 1, -1, -1):
        if conversation[i]["role"] == "assistant":
            break
        if conversation[i]["role"] == "user":
            del conversation[i]
            break
    with open('user_files/conversation.json', "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

# Lấy câu trả lời từ OpenAI dành cho chat
async def openai_answer():
    global total_characters, conversation
    client = AsyncOpenAI(api_key=openai_key_1, timeout=60)
    total_characters = sum(len(d['content']) for d in conversation)

    while total_characters > 4000:
        try:
            conversation.pop(2)
            total_characters = sum(len(d['content']) for d in conversation)
        except Exception as e:
            print("Error removing old messages: {0}".format(e))

    with open('user_files/conversation.json', "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

    prompt = getPrompt()

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=1024,
        temperature=1,
        top_p=0.9
    )
    message = response.choices[0].message.content

    conversation.append({'role': 'assistant', 'content': message})

    with open('user_files/conversation.json', "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

# Lấy câu trả lời từ OpenAI dành cho chat trong channel
def openai_answer_channel():
    global total_characters_channel, channel_history
    client = OpenAI(api_key=openai_key_1, timeout=60)
    total_characters_channel = sum(len(d['content']) for d in channel_history)

    while total_characters_channel > 4000:
        try:
            # print(total_characters)
            # print(len(conversation))
            channel_history.pop(2)
            total_characters_channel = sum(len(d['content']) for d in channel_history)
        except Exception as e:
            print("Error removing old messages: {0}".format(e))

    with open('user_files/channel_history.json', "w", encoding="utf-8") as f2:
        # Write the message data to the file in JSON format
        json.dump(history2, f2, indent=4)

    prompt = getPrompt_channel()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=128,
        temperature=1,
        top_p=0.9
    )
    message = response.choices[0].message.content

    channel_history.append({'role': 'assistant', 'content': message})

    with open('user_files/channel_history.json', "w", encoding="utf-8") as f2:
        # Write the message data to the file in JSON format
        json.dump(history2, f2, indent=4)

# Lấy câu trả lời từ OpenAI dành cho tasks
async def openai_task(case):
    client = AsyncOpenAI(api_key=openai_key_2, timeout=60)
    prompt = getPrompt_task(case)

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=1024,
        temperature=1,
        top_p=0.9
    )
    command = response.choices[0].message.content

    if case != 1:

        conversation.append({'role': 'assistant', 'content': command})

        with open('user_files/conversation.json', "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
            json.dump(history, f, indent=4)

    return command

# Chuyển đổi voice của user thành văn bản (STT)
async def openai_audio(audio_url):
    client = AsyncOpenAI(api_key=openai_key_1)
    async with aiohttp.ClientSession() as session:
        async with session.get(audio_url.url) as resp:
            tar_lang = lang_detect(get_bot_answer())
            if resp.status == 200:
                with open(audio_filename, 'wb') as f:
                    f.write(await resp.read())
                # Thực hiện xử lý file âm thanh bằng OpenAI
                with open(audio_filename, 'rb') as audio_file:
                    transcript = await client.audio.translations.create(model='whisper-1', file=audio_file)
                result = transcript.text
                sour_lang = lang_detect(result)
                if sour_lang != tar_lang:
                    transcript_text = transcript.text
                    translator = Translator(to_lang=tar_lang)
                    translated_transcript = translator.translate(transcript_text)
                    result = translated_transcript
            else:
                result = "*I said something but you didn't hear clearly*"
                if tar_lang == "vi":
                    result = f"*vừa nói gì đó nhưng bạn không nghe thấy.*"
                if tar_lang == "ja":
                    result = "*何か言ったけどはっきり聞こえなかった*"
            
            return result

# Image gen
async def openai_images(prompt):
    client = AsyncOpenAI(api_key=openai_key_2, timeout=60)
    response = await client.images.generate(
        prompt=prompt,
        model="dall-e-3",
        quality="standard",
        response_format="url",
        size="1024x1024"
    )
    image_url = response.data[0].url
    return image_url

# Hàm xoá cuộc trò chuyện
def clear_conversation_history():
    global conversation, history

    conversation = []
    history = {"history": conversation}

def clear_conversation_history_public():
    global channel_history, history2

    channel_history = []
    history2 = {"history": channel_history}

if __name__ == "__main__":
    openai_answer()