import os
import json
import requests
import base64

from user_files.config import *

# Thay đổi token của bot Discord ở đây
BOT_TOKEN = discord_bot_key

async def voice_message(channel_id, console_log):
    CHANNEL_ID = channel_id
    # Đọc dữ liệu âm thanh từ tệp âm thanh
    voice_data = open(os.getcwd() + "/user_files/ai_voice_msg.ogg", "rb").read()

    # Xây dựng dữ liệu JSON
    attach_data = {
        'files': [{
            'file_size': len(voice_data),
            'filename': 'voice-message.ogg',
            'id': '2'
        }]
    }

    # Gửi yêu cầu để đính kèm tệp âm thanh
    attach_url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/attachments'
    attach_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bot {BOT_TOKEN}'
    }
    attach_response = requests.post(attach_url, headers=attach_headers, data=json.dumps(attach_data))
    attach_json = attach_response.json()
    upload_url = attach_json['attachments'][0]['upload_url']
    upload_filename = attach_json['attachments'][0]['upload_filename']

    # Gửi tệp âm thanh lên Discord
    upload_headers = {'Content-Type': 'audio/ogg'}
    requests.put(upload_url, headers=upload_headers, data=voice_data)

    # Gửi tin nhắn với tệp âm thanh đã đính kèm
    message_url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages'
    message_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bot {BOT_TOKEN}',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5OTk5OTk5fQ=='
    }
    message_data = {
        'flags': 8192,
        'attachments': [{
            'id': '0',
            'filename': 'voice-message.ogg',
            'uploaded_filename': upload_filename,
            'duration_secs': 0.000001,
            'waveform': base64.b64encode(voice_data[:100]).decode("utf-8") 
        }]
    }

    # Gửi tin nhắn
    response = requests.post(message_url, headers=message_headers, data=json.dumps(message_data))
    if console_log:
        print("Voice Message send:", response.status_code)