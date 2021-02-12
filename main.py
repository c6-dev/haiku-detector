import logging
import re

from rusyll import rusyll
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def getHaiku(text):
    syllables = rusyll.token_to_syllables(text)
    if (len(syllables) == 17):
        haiku = [[], [], []]
        words = re.sub(r'/\s+/g', ' ', text).split(' ')
        i = 0
        for word in words:
            haiku[i].append(word)
            paragraphSyllableCount = len(rusyll.token_to_syllables(' '.join(haiku[i])))
            maxSyllables = [5, 7, 5]
            if (paragraphSyllableCount == maxSyllables[i]):
                i += 1
                continue
            if (paragraphSyllableCount > maxSyllables[i]):
                return 0
        retnText = '\n'.join(map(lambda line: ' '.join(line), haiku))
        return retnText
    return 0

def echo(update: Update, context: CallbackContext) -> None:

    text = update.message.text
    haiku = getHaiku(text)
    if (haiku != 0):
        user = update.effective_user.full_name
        update.message.reply_text(f'{haiku}\n\n - {user}')


def main():
    updater = Updater("TOKEN")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()