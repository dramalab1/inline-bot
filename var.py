from decouple import config


class Var(object):
    API_ID = config("API_ID", cast=int)
    API_HASH = config("API_HASH")
    BOT_TOKEN = config("BOT_TOKEN")
    SESSION = config("SESSION", default=None)
    INVITE_LINK = config("INVITE_LINK", default=None)
    CHANNEL_ID = config("CHANNEL_ID", default=0, cast=int)
    RANDOM_CHANNEL = config("RANDOM_CHANNEL", default=None)
