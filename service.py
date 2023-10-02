import os
from tg_bot import TgBot
from dotenv import load_dotenv
from utils import get_logger

load_dotenv()

logger = get_logger(__name__)


def main():
    token = os.getenv("TOKEN")
    url = os.getenv("URL")

    rmb = TgBot(token, url)
    rmb.add_handlers()
    rmb.start_bot()


if __name__ == '__main__':
    main()
