import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import telegram

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def help(update, context):
    """Send a message when the command /help is issued."""
    user_id = update.effective_user['id']
    #update.message.reply_text('Help!')
    update.message.reply_text(user_id)


def funcion(update, context):
    """Echo the user message."""

    user_id = update.effective_user['id']
    text = update.message.text
    context.bot.sendMessage(chat_id= user_id, text = text + "1")
    text2= programa(update.message.text)
    update.message.reply_text(text + "2")


def error(update, error, bot):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def handle_start(update, context):
    #update.message.reply_text(text='Hello')
    update.message.reply_text(text=str(programa("2 3 4 5")))


if __name__ == '__main__':
    token = os.environ['TOKEN']

    bot = telegram.Bot(token=token)

    updater = Updater(token=token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(
        CommandHandler('start', handle_start)
    )

    print(f'running at @{bot.username}')

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, funcion))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


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
        return f'El resultado es ((({cartas4[0]} {ops[0]} {cartas4[1]}) {ops[1]} {cartas4[2]}) {ops[2]} {cartas4[3]})'

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
            return f'El resultado es (({cartas4[2]} {ops[1]} ({cartas4[0]} {ops[0]} {cartas4[1]})) {ops[2]} {cartas4[3]})'
        else:
            return f'El resultado es ((({cartas4[0]} {ops[0]} {cartas4[1]}) {ops[1]} {cartas4[2]}) {ops[2]} {cartas4[3]})'

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
        return f'El resultado es (({cartas4[2]} {ops[1]} ({cartas4[1]} {ops[0]} {cartas4[0]})) {ops[2]} {cartas4[3]})'

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
        return f'El resultado es ((({cartas4[0]} {ops[0]} {cartas4[1]}) {ops[1]} {cartas4[2]}) {ops[2]} {cartas4[3]})'

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
        return "Datos erroneos"

    cartas = cartas.split()
    if len(cartas) > 4:
        return "Datos erroneos"
    cartas2 = [int(x) for x in cartas]
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
        return "No se encontro resultado"