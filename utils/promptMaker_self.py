import json
import sys
import datetime
import pytz

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

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
        with open(file_name, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")    

def getPrompt():
    timezone = pytz.timezone('Asia/Bangkok')
    time = datetime.datetime.now(timezone)
    total_len = 0
    prompt = []
    vals = vals_open('vals.json')
    nsfw_toggle = vals['nsfw']

    nsfw_text = ""
    if nsfw_toggle:
        nsfw_text = getIdentity("prompt/nsfw.txt")
    sys_prompt = getIdentity("prompt/sys_prompt.txt")
    char_info = getIdentity("prompt/character.txt")
    user_info = getIdentity("prompt/user.txt")
    goal = getIdentity("prompt/goal.txt")
    current_time = time.strftime('%Y-%m-%d %H:%M:')
    current_time = ("Current time:", current_time)
    current_mood = getIdentity("prompt/current_mood.txt")
    behavior = getIdentity("prompt/behavior.txt")

    iden = f"{nsfw_text}\n{sys_prompt}\n{char_info}\n{user_info}\n{goal}\n{current_time}\n{current_mood}\n{behavior}"
    prompt.append({"role": "system", "content": iden})

    hist = vals_open('conversation.json')
    history = hist["history"]
    for message in history[:-1]:
        prompt.append(message)

    prompt.append(history[-1])

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

def getPrompt_channel():
    timezone = pytz.timezone('Asia/Bangkok')
    time = datetime.datetime.now(timezone)
    total_len = 0
    prompt = []

    sys_prompt = getIdentity("prompt/sys_prompt.txt")
    char_info = getIdentity("prompt/character.txt")
    user_info = getIdentity("prompt/user.txt")
    friends_info = getIdentity("prompt/friends.txt")
    current_time = time.strftime('%Y-%m-%d %H:%M:')
    current_time = ("Current time:", current_time)
    current_mood = getIdentity("prompt/current_mood.txt")
    channel_behavior = getIdentity("prompt/behavior.txt")

    iden = f"{sys_prompt}\n{char_info}\n{user_info}\n{friends_info}\n{current_time}\n{current_mood}\n{channel_behavior}"
    prompt.append({"role": "system", "content": iden})

    hist2 = vals_open('channel_history.json')
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

    hist = vals_open('conversation.json')
    history = hist["history"]

    if case == 1:
        prompt.append(getprompt_normal("prompt/mood.txt"))
        recent_history = history[-2:]
        for message in recent_history:
            prompt.append(message)

    elif case == 2:
        timezone = pytz.timezone('Asia/Bangkok')
        time = datetime.datetime.now(timezone)
        total_len = 0
        prompt = []
        vals = vals_open('vals.json')
        nsfw_toggle = vals['nsfw']

        nsfw_text = ""
        if nsfw_toggle:
            nsfw_text = getIdentity("prompt/nsfw.txt")
        sys_prompt = getIdentity("prompt/sys_prompt.txt")
        char_info = getIdentity("prompt/character.txt")
        user_info = getIdentity("prompt/user.txt")
        goal = getIdentity("prompt/goal.txt")
        current_time = time.strftime('%Y-%m-%d %H:%M:')
        current_time = ("Current time:", current_time)
        current_mood = getIdentity("prompt/current_mood.txt")
        behavior = getIdentity("prompt/behavior.txt")

        iden = f"{nsfw_text}\n{sys_prompt}\n{char_info}\n{user_info}\n{goal}\n{current_time}\n{current_mood}\n{behavior}"
        prompt.append({"role": "system", "content": iden})

        for message in history[:-1]:
            prompt.append(message)

        prompt.append(history[-1])

        total_len = sum(len(d['content']) for d in prompt)
        
        while total_len > 3900:
            try:
                # print(total_len)
                # print(len(prompt))
                prompt.pop(2)
                total_len = sum(len(d['content']) for d in prompt)
            except:
                print("Error: Prompt too long!")

        msg = "Continue the conversation or action where you left off proactively and creatively without asking."
        prompt.append({"role": "system", "content": msg})

    elif case == 3:
        prompt.append(getprompt_normal("prompt/schedule.txt"))
        recent_history = history[-1:]

        for message in recent_history:
            prompt.append(message)

    return prompt

if __name__ == "__main__":
    prompt = getPrompt()
    print(prompt)
    print(len(prompt))