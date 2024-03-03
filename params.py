from dotenv import load_dotenv
from datetime import datetime
import os
from twitchAPI.type import AuthScope

load_dotenv()

COMAND_TIMER = datetime(1990, 1, 1)
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL").split(',')
APP_ID = os.getenv("APP_ID")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
APP_SECRET = os.getenv("APP_SECRET")
AUDIO_1 = os.getenv("AUDIO_1")
FAKE_AUDIO = os.getenv("FAKE_AUDIO")
FAKE_LANGUAGE = "ru"
COMAND_COOLDOWN = 60