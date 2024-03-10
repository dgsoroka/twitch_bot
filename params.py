from dotenv import load_dotenv
from datetime import datetime
import os
from twitchAPI.type import AuthScope

load_dotenv()

COMMAND_TIMER = datetime(1990, 1, 1)
TARGET_CHANNEL = [i.lstrip().rstrip() for i in os.getenv("TARGET_CHANNEL").split(",")]
APP_ID = os.getenv("APP_ID")
USER_SCOPE = [
    AuthScope.CHAT_READ,
    AuthScope.CHAT_EDIT,
    AuthScope.CHANNEL_BOT,
    AuthScope.MODERATOR_READ_CHATTERS,
    AuthScope.MODERATOR_READ_FOLLOWERS,
    AuthScope.MODERATOR_MANAGE_BANNED_USERS,
    AuthScope.MODERATOR_MANAGE_CHAT_MESSAGES,
    AuthScope.MODERATOR_MANAGE_BLOCKED_TERMS,
    AuthScope.MODERATOR_MANAGE_SHOUTOUTS,
    AuthScope.CHANNEL_MODERATE,
]
APP_SECRET = os.getenv("APP_SECRET")
AUDIO_1 = os.getenv("AUDIO_1")
FAKE_AUDIO = os.getenv("FAKE_AUDIO")
FAKE_LANGUAGE = "ru"
COMMAND_COOLDOWN = 10
STREAMER_ID = os.getenv("STREAMER_ID")
MODERATOR_ID = os.getenv("MODERATOR_ID")
LIST_COMMANDS = [i.lstrip().rstrip() for i in os.getenv("LIST_COMMANDS").split(",")]