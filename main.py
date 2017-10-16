from telegram import InlineQueryResultArticle, InlineQueryResultCachedPhoto, InputTextMessageContent, ParseMode
from telegram.ext import Updater, MessageHandler, InlineQueryHandler, BaseFilter

from smart_qr_codes import smart_qr_code_by_name
import logging
import os


from uuid import uuid4

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '414610099:AAHG4Mf5lw05PxI4JY9ZP6CpTlkauCk4AAo')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR)


def start(bot, update):
    update.message.reply_text("Hello! I'm a very creative bot! I do QRCodes from your content and description. Just send me a link and a name of object you want to display on your QR-Code")


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


updater = Updater(TELEGRAM_TOKEN)


class IsCorrect(BaseFilter):
    def filter(self, message):
        return True


def do_qr_code(bot, update):
    splitted_text = update.message.text.split()
    content = splitted_text[0]
    name = " ".join(splitted_text[1:])

    def send_qr(qr):
        bot.send_photo(update.message.chat_id,
                       photo=qr,
                       caption=name)


    smart_qr_code_by_name(content, name, suffix=".png", save_name=None, hook=send_qr)


def do_inline_qr_code(bot, update):
    query = update.inline_query.query
    results = list()

    splitted_text = query.split()

    if len(splitted_text) < 2:
        return

    content = splitted_text[0]
    name = ' '.join(splitted_text[1:])

    def send_qr(qr):
        photo_info = bot.send_photo(update.inline_query.from_user.id,
                       photo=qr,
                       caption=name)

        results.append(InlineQueryResultCachedPhoto(id=uuid4(), photo_file_id=photo_info.photo[0].file_id))

        update.inline_query.answer(results)


    smart_qr_code_by_name(content, name, suffix=".png", save_name=None, hook=send_qr)

isCorrectFilter = IsCorrect()


echo_handler = MessageHandler(isCorrectFilter, do_qr_code)
inline_handler = InlineQueryHandler(do_inline_qr_code)
updater.dispatcher.add_handler(echo_handler)
# updater.dispatcher.add_handler(inline_handler)
updater.start_polling()
updater.idle()
