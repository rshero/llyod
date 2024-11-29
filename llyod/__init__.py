import logging
from telethon import TelegramClient
from llyod.config import api_hash, api_id, bot_token

# some usable variables
queries = {}
ids = {}

logging.basicConfig(
    format="[%(levelname)s/%(asctime)s] %(name)s %(lineno)d: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


app = TelegramClient("llyod", api_id, api_hash).start(bot_token=bot_token)
