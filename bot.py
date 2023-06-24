import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from uuid import uuid4
import requests
import json

API_URL = 'https://api.jsonbin.io/v3/b/649749cd9d312622a3750331'
API_KEY = os.environ.get('API_KEY', None)
status = ''
shop = -1
order = -1

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_data():
    headers = {'X-Master-Key': API_KEY}
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()["record"]
        print("Data retrieved successfully:")
        print(json.dumps(data, indent=4))
        status = data["status"]
        shop = data["shop"]
        order = data["order"]
    else:
        print(f"Error accessing data. Status code: {response.status_code}")
        print(response.text)

def store_data():
    headers = {'X-Master-Key': API_KEY, 'Content-Type': 'application/json'}
    response = requests.put(
        API_URL,
        headers=headers,
        json={
            "status": status,
            "shop": shop,
            "order": order
        })

    if response.status_code == 200:
        print("Data stored successfully")
    else:
        print(f"Error storing data. Status code: {response.status_code}")
        print(response.text)


async def get_status(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Shop: {}\nOrder: {}".format(shop, order))

async def set_shop(update, context):
    shop = update.message.text.partition(' ')[2]
    store_data()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Shop changed to {}".format(shop))

async def set_order(update, context):
    order = update.message.text.partition(' ')[2]
    store_data()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Order changed to {}".format(order))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi,\nI will notify you once your fotoparadies order is ready.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get('TOKEN', None)).build()

    get_data() 

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('set_shop', set_shop))
    application.add_handler(CommandHandler('set_order', set_order))
    application.add_handler(CommandHandler('status', get_status))
    
    application.run_polling()
