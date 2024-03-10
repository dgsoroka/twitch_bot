from dateutil import relativedelta
from datetime import datetime
from params import COMMAND_COOLDOWN, COMMAND_TIMER


async def cooldown():
    if not (
        COMMAND_TIMER + relativedelta.relativedelta(seconds=COMMAND_COOLDOWN)
        < datetime.now()
    ):
        return True