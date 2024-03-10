from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import os
from playsound import playsound
from datetime import datetime
from dateutil import relativedelta
from gtts import gTTS
from params import *
import random


# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print("Bot is ready for work, joining channels")
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):

    print(f"in {msg.room.name}, {msg.user.name} said: {msg.text}")


# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(
        f"New subscription in {sub.room.name}:\\n"
        f"  Type: {sub.sub_plan}\\n"
        f"  Message: {sub.sub_message}"
    )


# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply("you did not tell me what to reply with")
    else:
        await cmd.reply(f"{cmd.user.name}: {cmd.parameter}")


async def test_audio_command(cmd: ChatCommand):
    global COMAND_TIMER
    if (
        COMAND_TIMER + relativedelta.relativedelta(seconds=COMAND_COOLDOWN)
        < datetime.now()
    ):
        playsound(AUDIO_1)
        COMAND_TIMER = datetime.now()


async def fake_audio(cmd: ChatCommand):
    global COMAND_TIMER
    if (
        COMAND_TIMER + relativedelta.relativedelta(seconds=COMAND_COOLDOWN)
        < datetime.now()
    ):
        text = cmd.parameter
        gTTS(text, lang=FAKE_LANGUAGE).save(FAKE_AUDIO)
        playsound(FAKE_AUDIO)
        os.remove(FAKE_AUDIO)
        COMAND_TIMER = datetime.now()


async def throw(cmd: ChatCommand):
    global chat, COMAND_TIMER
    if not (
        COMAND_TIMER + relativedelta.relativedelta(seconds=COMAND_COOLDOWN)
        < datetime.now()
    ):
        return
    chatter = None
    chatters = await chat.twitch.get_chatters(STREAMER_ID, MODERATOR_ID)
    chatters = [i for i in chatters.data]
    for i in chatters:
        if i.user_login.lower() == cmd.parameter[1:].lower():
            chatter = i
    if not chatter:
        print("Юзера нет в чате")
        return
    if random.randint(1, 10) >= 5:
        await cmd.reply(f"@{cmd.user.name} швырнул на прогиб @{chatter.user_login}")
        await chat.twitch.ban_user(
            STREAMER_ID, MODERATOR_ID, chatter.user_id, "Кинут на прогиб", 30
        )
    else:
        await cmd.reply(
            f"@{cmd.user.name} не смог поднять тушу @{chatter.user_login} и сломал себе спину"
        )
        await chat.twitch.ban_user(
            STREAMER_ID, MODERATOR_ID, cmd.user.id, "Сломал спину", 30
        )


async def poke(cmd: ChatCommand):
    global chat, COMAND_TIMER
    if not (
        COMAND_TIMER + relativedelta.relativedelta(seconds=COMAND_COOLDOWN)
        < datetime.now()
    ):
        return
    chatters = await chat.twitch.get_chatters(STREAMER_ID, MODERATOR_ID)
    chatters = [i.user_login for i in chatters.data]
    random_chatters = random.choice(chatters)
    cmd.send(f"Пошел нахуй, @{random_chatters}")


# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    global chat
    chat = await Chat(twitch)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to channel subscriptions
    chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation

    # you can directly register commands and their handlers, this will register the !reply command
    chat.register_command("reply", test_command)
    chat.register_command("audio", test_audio_command)
    chat.register_command("fake", fake_audio)
    chat.register_command("прогиб", throw)
    chat.register_command("тык", poke)

    # we are done with our setup, lets start this bot up!
    chat.start()
    chatters = await chat.twitch.get_chatters(STREAMER_ID, MODERATOR_ID)
    print([i.user_login for i in chatters.data])

    # lets run till we press enter in the console
    try:
        input("press ENTER to stop\n")
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()


# lets run our setup
asyncio.run(run())
