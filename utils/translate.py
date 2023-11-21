from translate import Translator
from langdetect import detect
from mtranslate import translate

def text_translate(text, target_lang):
    # Xác định ngôn ngữ của văn bản đầu vào
    source_lang = detect(text)
    
    # Kiểm tra xem ngôn ngữ đầu vào và ngôn ngữ đích có giống nhau hay không
    if source_lang == target_lang:
        return text
    
    # Dịch văn bản nếu ngôn ngữ đầu vào và ngôn ngữ đích khác nhau
    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    translated_text = translator.translate(text)
    return translated_text

def lang_detect(text):
    source_lang = detect(text)
    return source_lang

def text_translate2(text, to_language='ja'):
    translated_text = translate(text, to_language)
    return translated_text

if __name__ == "__main__":
    text_translate()