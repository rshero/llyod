from llyod import ids
from functools import wraps
from telethon.events.callbackquery import CallbackQuery


def is_sha1_hashed(string):
    if len(string) == 40 and all(c in "0123456789abcdef" for c in string):
        return True
    else:
        return False


short_names = {
    "csm": "chainsaw man",
    "jjk": "jujutsu kaisen",
    "jjk 0": "jujutsu kaisen 0",
    "tog": "Tower of God",
    "lnb": "The Legend of the Northern Blade",
    "orv": "Omniscient Reader",
    "fmab": "fullmetal alchemist",
    "mha": "my hero academia",
    "opm": "one punch man",
    "wmmap": "who made me a princess",
    "ngnl": "no game no life",
}


# create a decorator to check if the user is the same as the one who clicked on the button
def check_user(func):
    @wraps(func)
    async def same_user(event: CallbackQuery.Event, *args, **kwargs):
        try:
            if ids[f"{event.message_id}"] == event.sender_id:
                return await func(event, *args, **kwargs)
            else:
                await event.answer("This is not for you", alert=True)
        except (KeyError, IndexError):
            await event.answer(
                "Query has been expired. Please remake the query.", alert=True
            )

    return same_user
