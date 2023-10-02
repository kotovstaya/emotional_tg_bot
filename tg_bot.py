from typing import Optional
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from utils import get_logger
from llm_bot import EmotionalChatBot

logger = get_logger(__name__)


class TgBot:
    def __init__(
        self,
        token: str,
        url: str
    ):
        self.token = token
        self.updater: Updater = self._init_updater()
        self.dp = self._init_dispatcher()
        self.url = url
        self.emotional_bot: Optional[EmotionalChatBot] = None

    def _init_emotional_bot(self):
        self.emotional_bot = EmotionalChatBot()

    def _init_updater(self) -> Updater:
        return Updater(self.token, use_context=True)

    def _init_dispatcher(self):
        return self.updater.dispatcher

    def echo(self, update, context):
        if self.emotional_bot is not None:
            response = self.emotional_bot.tell(update.message.text)
            update.message.reply_text(response)
        else:
            update.message.reply_text("There is no active emotional bot. Please write /start and init one bot")

    def error(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def start(self, update, context):
        logger.info("Init emotional bot")
        self._init_emotional_bot()
        logger.info("Init emotional bot is done")
        update.message.reply_text("Emotional bot is created. Say Hi to him")

    def end(selfself, update, context):
        update.message.reply_text('GoodBye!')

    def show_history(self, update, context):
        if self.emotional_bot is not None:
            update.message.reply_text(self.emotional_bot.show_history)
        else:
            update.message.reply_text("There is no active emotional bot. Please write /start and init one bot")

    def help(self, update, context):
        help_string = """
        @emotional_tg_bot
        /start - start the conversion
        /end - end the conversion 
        /help - info 
        /history - show history of the conversation
        """
        update.message.reply_text(help_string)

    def add_handler(self, name, func):
        self.dp.add_handler(CommandHandler(name, func))
        return self

    def add_message_handler(self, func):
        self.dp.add_handler(MessageHandler(Filters.text, func))
        return self

    def add_error_handler(self, func):
        self.dp.add_error_handler(func)
        return self

    def add_handlers(self):
        (
            self.add_handler("start", self.start)
            .add_handler("end", self.end)
            .add_handler("help", self.help)
            .add_handler("history", self.show_history)
            .add_message_handler(self.echo)
            .add_error_handler(self.error)
        )

    def start_bot(self):
        self.updater.start_polling()
        self.updater.idle()