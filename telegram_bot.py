import os
import asyncio
from decimal import getcontext
from io import BytesIO

import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from telepot.namedtuple import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)

from dotenv import load_dotenv
from arbitrage import arbitrage
from luno import Luno
from fnb import FNB
from gdax import GDAX
from coinbase_ex import CoinbaseEx

token = "btc"
buy_currency = "eur"

async def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print("Chatting in {} with {}".format(chat_type, chat_id))

    if (content_type != "text"):
        return()

    cmd = msg['text'].lower()

    amount = 0
    try:
        amount = int(cmd)
    except ValueError:
        pass

    if cmd == '/help':
        await bot.sendMessage(chat_id, 'Type /arb to simulate an arbitrage position')

    elif cmd == '/arb':
        kybrd = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='BTC'),
            KeyboardButton(text='ETH')],
        ])

        await bot.sendMessage(chat_id, 'Which asset would you like to buy', reply_markup=kybrd)

    elif cmd in ['btc', 'eth']:
        global token
        token = cmd.upper()

        kybrd = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='EUR'),
            KeyboardButton(text='USD')],
        ])

        await bot.sendMessage(chat_id, 'Which forex asset would you like to use', reply_markup=kybrd)
    elif cmd in ['usd', 'eur']:
        global buy_currency

        buy_currency = cmd.upper()

        kybrd = ReplyKeyboardRemove()
        await bot.sendMessage(chat_id, "How much ZAR do you want to spend on {}?".format(token), reply_markup=kybrd)
    
    elif amount > 0:
        await bot.sendMessage(chat_id, "Simulating {} ZAR for {} via {}...".format(amount, token, buy_currency))

        forex_ex = FNB(buy_currency)
        buy_ex = CoinbaseEx(CB_KEY, CB_SECRET, buy_currency, token)
        sell_ex = Luno(LUNO_KEY,LUNO_SECRET, currency_from="ZAR", currency_to=token)

        profit, margin = arbitrage(amount, buy_ex, sell_ex, forex_ex, verbose=False)
        
        await bot.sendMessage(chat_id, "Arbitrage of {:.2f} would yield {:.2f} profit.\nCurrent margin is {:.2f}".format(amount, profit, margin), 
            reply_to_message_id=msg['message_id'])

    else:
        print('Ooops')

load_dotenv('.env')
CB_KEY = os.environ.get('CB_KEY')
CB_SECRET = os.environ.get('CB_SECRET')
LUNO_KEY = os.environ.get('LUNO_KEY')
LUNO_SECRET = os.environ.get('LUNO_SECRET')
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = telepot.aio.Bot(TELEGRAM_TOKEN)
answerer = telepot.aio.helper.Answerer(bot)
loop = asyncio.get_event_loop()

loop.create_task(MessageLoop(bot, {
    'chat': on_chat_message,
    }).run_forever())

print('Running...')

loop.run_forever()
