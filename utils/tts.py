import requests
from utils.config import *
from utils.katakana import *
import re
import requests

def tts_get(text, speaker, pitch, intonation_scale, speed, console_log):
    text_fill = remove_act(text)
    if not text_fill:
        if not text:
            text = "エラー エラー"
        text_fill = text
    cnv_text = romaji_to_katakana(text_fill)
    url = f"https://deprecatedapis.tts.quest/v2/voicevox/audio/?key={vv_key}&text={cnv_text}&speaker={speaker}&pitch={pitch}&intonationScale={intonation_scale}&speed={speed}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        # Lưu audio vào file .ogg
        with open('ai_voice_msg.ogg', 'wb') as f:
            f.write(response.content)
        if console_log:
            print(f"Voice của {ai_name} đã được tải về thành công.")
    else:
        print(f"Lỗi khi tạo voice, mã lỗi: {response.status_code}")

def remove_act(text):
    # Xoá các phần trong cặp hoa thị
    text = re.sub(r'\*([^*]+)\*', '', text)

    # Xoá các phần trong cặp ngoặc tròn
    text = re.sub(r'\([^)]+\)', '', text)

    # Xoá các phần trong cặp ngoặc nhọn
    text = re.sub(r'<[^>]+>', '', text)

    # Xoá đường link
    text = re.sub(r'https?://\S+', '', text)

    return text

if __name__ == "__main__":
    tts_get()