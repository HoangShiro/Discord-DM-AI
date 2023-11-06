import discord

now_mood = discord.Activity(
        type=discord.ActivityType.watching,
        name="idle"
    )

idle_status = discord.Status.idle
onl_status = discord.Status.online
dnd_status = discord.Status.dnd

def bot_activ(bot, mood_name):
    global now_mood
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=mood_name
    )
    now_mood = activity
    bot.change_presence(
        activity=activity,
        status=onl_status
    )

def bot_activ_non_chat(bot, mood_name):
    global now_mood
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=mood_name
    )
    now_mood = activity
    bot.change_presence(
        activity=activity,
        status=idle_status
    )

def bot_status_change(bot):
    bot.change_presence(activity=now_mood, status=idle_status)

def bot_status_change_sad(bot):
    bot.change_presence(activity=now_mood, status=dnd_status)