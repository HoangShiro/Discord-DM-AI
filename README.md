# Discord-DM-AI
### For private DM only with GPT. 

Warning: NSFW
Main file: main.py

Interface language: Vietnamese

## Installation
### Dependencies: <br>
- Python: Tested on python 3.11
- Git (for automatic updates)
- ffmpeg (for bot voice en)

- Libraries used in file requirements.txt and torch, pydub, numpy.

#### One step:
- Download and run the ```first_run.bat``` file

From next time just run the file ```run.bat```

#### From git in windows cmd:
```
git clone https://github.com/HoangShiro/Discord-DM-AI.git
```
- Run the file ```run.bat``` and exit
- Then run the file ```edit_info.bat``` and setting the necessary information.
- Run the file ```run.bat```

### Setting: <br>
```edit_info.bat```

#### Prompt:
- Character:
Description of your character.

- User:
Yourself.

- Behavior:
The way your character chats with you.

There are also other prompts, you can edit them in ```user_files/prompt```

#### APIs and variables:
- Discord bot token:
```https://discord.com/developers```
Create your discord bot if you don't have and get tokens.

- Openai api:
```https://platform.openai.com/account/api-keys```
If you don't have two keys, fill in the same.

- Voice Vox fast api (Japanese AI voice) (optional):
```https://voicevox.su-shiki.com/su-shikiapis```
Follow the steps at the link above to get the api.

- User id, server id:
Your discord id and the discord mutual server.

- speaker, pitch, intonation, speed(optional):
Setting up for voicevox api, speaker id can be obtained based on character/speaker order at the voicevox home page below, starting from 0.
```https://voicevox.hiroshiba.jp/```

## Functions

### Slash commands <br>

#### Chat:
```/newchat```
New conversation.

```/delchat```
Delete the bot's most recent conversations.

```/erate```
Bot emoji reaction rate. Emojis are taken from the server that your bot joins.

#### Voice message:
```/vchat [ja/en]```
Supports 2 voice engines from Voicevox and Silero, put nothing to disable it.

```/vconfig [speaker] [pitch] [intonation] [speed]```
Settings for voice, pitch, intonation, speed values are for Japanese voice only.

#### Reminder:
```/remind [note] [time] [date]```
Same function as alarm.

```/remindlist```
Reminder list.

```/remindremove [index]```
Delete reminder.

#### Other commands:
```/renew```
Restart the bot.

```/chatlog```
Show chat to console.

```/nsfw```
NSFW toggle.

```/status```
Just a test status slash command.

```/pchat```
Allows the bot to reply to your chat or another bot in the Discord server if provided with an id in the user_files/config.py file(Just experience, may not work correctly.).

```/clearchat```
Clear the bot's public "memory".

### Emotions <br>
Based on the bot's current emotions, it will react with the corresponding emoji or change its activity status.

### Good morning or good night <br>
Based on the current time to say good morning or good night when you are online.