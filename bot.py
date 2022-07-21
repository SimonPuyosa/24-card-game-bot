import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import telegram

def operacion(numero: int, cartas4: list[int], operaciones: list[int]) -> str:
    result = cartas4[0]
    ops = []
    for i in range(0, 3):
        if operaciones[i] == 0:
            result += cartas4[i + 1]
            ops += ["+"]
        elif operaciones[i] == 1:
            result = result - cartas4[i + 1]
            if result < 0:
                break
            ops += ["-"]
        elif operaciones[i] == 2:
            result *= cartas4[i + 1]
            ops += ["*"]
        else:
            if result % cartas4[i + 1] != 0: # si se puede floats 4 / 10 + 2 * 10
                break
            result //= cartas4[i + 1]
            ops += ["/"]
    if result == numero and len(ops) == 3:
        return f'The result is: (({cartas4[0]} {ops[0]} {cartas4[1]}) {ops[1]} {cartas4[2]}) {ops[2]} {cartas4[3]}'

    ops = []
    result = cartas4[0]
    for i in range(0, 3):
        if operaciones[i] == 0:
            result += cartas4[i + 1]
            ops += ["+"]
        elif operaciones[i] == 1:
            result = result - cartas4[i + 1]
            if result < 0:
                break
            ops += ["-"]
        elif operaciones[i] == 2:
            result *= cartas4[i + 1]
            ops += ["*"]
        else:
            if result == 0:
                break
            if cartas4[i + 1] % result != 0:
                break
            result = cartas4[i + 1] // result
            ops += ["/"]
    if result == numero and len(ops) == 3:
        if ops[1] == "/":
            return f'The result is: ({cartas4[2]} {ops[1]} ({cartas4[0]} {ops[0]} {cartas4[1]})) {ops[2]} {cartas4[3]}'
        else:
            return f'The result is: (({cartas4[0]} {ops[0]} {cartas4[1]}) {ops[1]} {cartas4[2]}) {ops[2]} {cartas4[3]}'

    result = cartas4[0]
    ops = []
    for i in range(0, 3):
        if operaciones[i] == 0:
            result += cartas4[i + 1]
            ops += ["+"]
        elif operaciones[i] == 1:
            result = cartas4[i + 1] - result
            if result < 0:
                break
            ops += ["-"]
        elif operaciones[i] == 2:
            result *= cartas4[i + 1]
            ops += ["*"]
        else:
            if result % cartas4[i + 1] != 0: # 7 - (11 / 5)) * 5
                break
            result //= cartas4[i + 1]
            ops += ["/"]
    if result == numero and len(ops) == 3:
        return f'The result is: ({cartas4[2]} {ops[1]} ({cartas4[1]} {ops[0]} {cartas4[0]})) {ops[2]} {cartas4[3]}'

    result = cartas4[0]
    ops = []
    for i in range(0, 3):
        if operaciones[i] == 0:
            result += cartas4[i + 1]
            ops += ["+"]
        elif operaciones[i] == 1:
            result = cartas4[i + 1] - result
            if result < 0:
                break
            ops += ["-"]
        elif operaciones[i] == 2:
            result *= cartas4[i + 1]
            ops += ["*"]
        else:
            if result == 0:
                break
            if cartas4[i + 1] % result != 0:
                break
            result = cartas4[i + 1] // result
            ops += ["/"]
    if result == numero and len(ops) == 3:
        return f'The result is: (({cartas4[0]} {ops[0]} {cartas4[1]}) {ops[1]} {cartas4[2]}) {ops[2]} {cartas4[3]}'

    return 'no'

def parse_message(message) -> bool:
    pattern = r'[0-9]+[ ][0-9]+[ ][0-9]+[ ][0-9]+'
    ticker = re.findall(pattern, message)

    if ticker:
        return True
    else:
        return False

def prueba(numero: int, cartas3: list[int], operaciones: list[int]) -> str:

    for i in range(0, 4):
        for j in range(0, 4):
            if i == j:
                continue
            for k in range(0, 4):
                if i == k or j == k:
                    continue
                l = 6 - i - j - k
                salida = operacion(numero, [cartas3[i], cartas3[j], cartas3[k], cartas3[l]], operaciones)
                if salida != 'no':
                    return salida
    return 'no'


def programa(cartas) -> str:
    numero = 24
    if not parse_message(cartas):
        return "Input data error"

    cartas = cartas.split()
    if len(cartas) > 4:
        return "Input data Error"

    cartas2 = []
    for x in cartas:
        try:
            cartas2 += [int(x)]
        except Exception:
            return "Input Data Error"
        if int(x) == 0:
            return "Input Data error"
    result = False
    i = j = k = 0

    while not result and i < 4:
        while not result and j < 4:
            while not result and k < 4:
                salida = prueba(numero, cartas2, [i, j, k])
                if salida != 'no':
                    return salida
                k += 1
            j += 1
            k = 0
        i += 1
        j = 0

    if not result:
        return "There is not a possible result"



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(text="This is a 24 card game solver. \nIf you do not know the game you can learn it here: https://en.wikipedia.org/wiki/24_(puzzle) "
                                   "\nTo see if it is possible to make 24 with 4 numbers/cards please put 4 numbers separating them with one space ' '."
                                   "\nDo not use letters or no positive numbers, instead of the letters use A = 1, J = 11, Q = 12, K = 13."
                                   "\nExample: 7 1 8 11\nResulting: The result is: (11 - (1 + 7)) * 8")


def funcion(update, context):
    """Echo the user message."""

    user_id = update.effective_user['id']
    text = programa(update.message.text)
    context.bot.sendMessage(chat_id=user_id, text=text)


def error(update, context):
    """Log Errors caused by Updates."""
    update.message.reply_text('If you found any error in the bot or a combination of numbers with a solution that the bot did not found, you can communicate it to @arabekaboom')


def handle_start(update, context):
    update.message.reply_text(text="This is a 24 card game solver. \nIf you do not know the game you can learn it here: https://en.wikipedia.org/wiki/24_(puzzle) "
                                   "\nTo see if it is possible to make 24 with 4 numbers/cards please put 4 numbers separating them with one space ' '."
                                   "\nDo not use letters or no positive numbers, instead of the letters use A = 1, J = 11, Q = 12, K = 13."
                                   "\nExample: 7 1 8 11\nResulting: The result is: (11 - (1 + 7)) * 8")

if __name__ == '__main__':
    token = os.environ['TOKEN']

    bot = telegram.Bot(token=token)

    updater = Updater(token=token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(
        CommandHandler('start', handle_start)
    )

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("error", error))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, funcion))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()