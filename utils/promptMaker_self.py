import json
import sys
import datetime
import pytz

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

def correct_role(role):
    # Chỉ chấp nhận "user" hoặc "assistant", chuyển đổi thành chữ thường để so sánh không phân biệt chữ hoa chữ thường
    return "user" if role.lower() == "user" else "assistant" if role.lower() == "assistant" else None

def get_schat(path):
    with open(path, 'r', encoding='utf-8') as file:
        if file:
            lines = file.readlines()
        else:
            lines = file
    return lines

def getIdentity(identityPath):  
    with open(identityPath, "r", encoding="utf-8") as f:
        identityContext = f.read()
    return identityContext

def getprompt_normal(identityPath):  
    with open(identityPath, "r", encoding="utf-8") as f:
        identityContext = f.read()
    return {"role": "assistant", "content": identityContext}

def vals_open(file_name):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        conversation = []
        history = {"history": conversation}
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        print(f"An error occurred: {str(e)}")    

def getPrompt():
    timezone = pytz.timezone('Asia/Bangkok')
    time = datetime.datetime.now(timezone)
    total_len = 0
    prompt = []
    vals = vals_open('user_files/vals.json')
    nsfw_toggle = vals['nsfw']
    beha_down = vals['beha_down']
    hist = vals_open('user_files/conversation.json')
    history = hist["history"]

    nsfw_text = ""
    if nsfw_toggle:
        nsfw_text = getIdentity("user_files/prompt/nsfw.txt")
    sys_prompt = getIdentity("user_files/prompt/sys_prompt.txt")
    char_info = getIdentity("user_files/prompt/character.txt")
    user_info = getIdentity("user_files/prompt/user.txt")
    goal = getIdentity("user_files/prompt/goal.txt")
    current_time = time.strftime('%Y-%m-%d %H:%M:')
    current_time = ("Current time:", current_time)
    current_mood = getIdentity("user_files/prompt/current_mood.txt")
    behavior = getIdentity("user_files/prompt/behavior.txt")
    chat_samp = get_schat("user_files/prompt/chat_samp.txt")
    chat_s = []
    if chat_samp:
        for i in range(0, len(chat_samp), 2):
            role, content = chat_samp[i].strip().split(': ')
            corrected_role = correct_role(role)
            if corrected_role:
                chat_s.append({"role": corrected_role, "content": content})
            else:
                print(f"Ignoring invalid role in chat_samp.txt: {role} - {content}")
    if not beha_down:
        if chat_s:
            iden = f"{nsfw_text}\n{sys_prompt}\n{char_info}\n{user_info}\n{goal}\n{current_time}\n{current_mood}\n{behavior}\n{chat_s}"
        else:
            iden = f"{nsfw_text}\n{sys_prompt}\n{char_info}\n{user_info}\n{goal}\n{current_time}\n{current_mood}\n{behavior}"
        prompt.append({"role": "system", "content": iden})
        for message in history[:-1]:
            prompt.append(message)
        prompt.append(history[-1])
    else:
        if chat_s:
            iden = f"{nsfw_text}\n{sys_prompt}\n{char_info}\n{user_info}\n{goal}\n{current_time}\n{current_mood}\n{chat_s}"
        else:
            iden = f"{nsfw_text}\n{sys_prompt}\n{char_info}\n{user_info}\n{goal}\n{current_time}\n{current_mood}"
        prompt.append({"role": "system", "content": iden})
        for message in history[:-1]:
            prompt.append(message)
        prompt.append(history[-1])
        prompt.append({"role": "system", "content": behavior})

    total_len = sum(len(d['content']) for d in prompt)
    
    while total_len > 4000:
        try:
            # print(total_len)
            # print(len(prompt))
            prompt.pop(2)
            total_len = sum(len(d['content']) for d in prompt)
        except:
            print("Error: Prompt too long!")

    # total_characters = sum(len(d['content']) for d in prompt)
    # print(f"Total characters: {total_characters}")
    print(prompt)
    return prompt

def getPrompt_channel():
    timezone = pytz.timezone('Asia/Bangkok')
    time = datetime.datetime.now(timezone)
    total_len = 0
    prompt = []

    sys_prompt = getIdentity("user_files/prompt/sys_prompt.txt")
    char_info = getIdentity("user_files/prompt/character.txt")
    user_info = getIdentity("user_files/prompt/user.txt")
    friends_info = getIdentity("user_files/prompt/friends.txt")
    current_time = time.strftime('%Y-%m-%d %H:%M:')
    current_time = ("Current time:", current_time)
    current_mood = getIdentity("user_files/prompt/current_mood.txt")
    channel_behavior = getIdentity("user_files/prompt/behavior.txt")

    iden = f"{sys_prompt}\n{char_info}\n{user_info}\n{friends_info}\n{current_time}\n{current_mood}\n{channel_behavior}"
    prompt.append({"role": "system", "content": iden})

    hist2 = vals_open('user_files/channel_history.json')
    history2 = hist2["history"]
    for message in history2[:-1]:
        prompt.append(message)

    prompt.append(history2[-1])

    total_len = sum(len(d['content']) for d in prompt)
    
    while total_len > 4000:
        try:
            # print(total_len)
            # print(len(prompt))
            prompt.pop(2)
            total_len = sum(len(d['content']) for d in prompt)
        except:
            print("Error: Prompt too long!")

    # total_characters = sum(len(d['content']) for d in prompt)
    # print(f"Total characters: {total_characters}")
    return prompt

def getPrompt_task(case):
    prompt = []
    total_len = 0
    hist = vals_open('user_files/conversation.json')
    history = hist["history"]
    timezone = pytz.timezone('Asia/Bangkok')
    time = datetime.datetime.now(timezone)
    vals = vals_open('user_files/vals.json')
    nsfw_toggle = vals['nsfw']
    beha_down = vals['beha_down']
    nsfw_text = ""

    if case == 1:
        prompt.append(getprompt_normal("user_files/prompt/mood.txt"))
        recent_history = history[-2:]
        for message in recent_history:
            prompt.append(message)
    elif case == 2:
        char_info = getIdentity("user_files/prompt/character.txt")
        pt = "Returns ONLY ONE sentence that is the description of the character's appearance in the description above, in English. Replace character name to 'a girl', eliminate personal pronouns. Remove sensitive words like 'thighs' and 'chest'"
        prompt.append({"role": "user", "content": char_info})
        prompt.append({"role": "system", "content": pt})
    elif case.startswith("3"):
        case = case[1:]
        si = case.find("[")
        ei = case.find("]")
        o_prompt = case[si + 1:ei]
        n_prompt = case[ei + 2:-1]
        rq = f"Correct the above sentence according to the following description: [{n_prompt}]"
        prompt.append({"role": "user", "content": o_prompt})
        prompt.append({"role": "system", "content": rq})
    else:
        if nsfw_toggle:
            nsfw_text = getIdentity("user_files/prompt/nsfw.txt")
        sys_prompt = getIdentity("user_files/prompt/sys_prompt.txt")
        char_info = getIdentity("user_files/prompt/character.txt")
        user_info = getIdentity("user_files/prompt/user.txt")
        goal = getIdentity("user_files/prompt/goal.txt")
        current_time = time.strftime('%Y-%m-%d %H:%M:')
        current_time = ("Current time:", current_time)
        current_mood = getIdentity("user_files/prompt/current_mood.txt")
        behavior = getIdentity("user_files/prompt/behavior.txt")
        chat_samp = get_schat("user_files/prompt/chat_samp.txt")
        chat_s = []
        if chat_samp:
            for i in range(0, len(chat_samp), 2):
                role, content = chat_samp[i].strip().split(': ')
                corrected_role = correct_role(role)
                if corrected_role:
                    chat_s.append({"role": corrected_role, "content": content})
                else:
                    print(f"Ignoring invalid role in chat_samp.txt: {role} - {content}")
        if not beha_down:
            if chat_s:
                iden = f"{nsfw_text}\n{sys_prompt}\n{char_info}\n{user_info}\n{goal}\n{current_time}\n{current_mood}\n{behavior}\n{chat_s}"
            else:
                iden = f"{nsfw_text}\n{sys_prompt}\n{char_info}\n{user_info}\n{goal}\n{current_time}\n{current_mood}\n{behavior}"
            prompt.append({"role": "system", "content": iden})
            for message in history[:-1]:
                prompt.append(message)
            prompt.append(history[-1])
            prompt.append({"role": "system", "content": case})
        else:
            if chat_s:
                iden = f"{nsfw_text}\n{sys_prompt}\n{char_info}\n{user_info}\n{goal}\n{current_time}\n{current_mood}\n{chat_s}"
            else:
                iden = f"{nsfw_text}\n{sys_prompt}\n{char_info}\n{user_info}\n{goal}\n{current_time}\n{current_mood}"
            prompt.append({"role": "system", "content": iden})
            for message in history[:-1]:
                prompt.append(message)
            prompt.append(history[-1])
            prompt.append({"role": "system", "content": behavior})


        total_len = sum(len(d['content']) for d in prompt)
        
        while total_len > 4000:
            try:
                prompt.pop(2)
                total_len = sum(len(d['content']) for d in prompt)
            except:
                print("Error: Prompt too long!")

    return prompt

if __name__ == "__main__":
    prompt = getPrompt()
    print(prompt)
    print(len(prompt))