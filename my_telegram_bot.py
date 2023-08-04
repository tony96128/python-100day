import os
import requests
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater

# 1. 環境變數
os.environ['TELEGRAM_TOKEN'] = '6217528436:AAHaDoRtFSTuPNL1wFcGExjRU4x01PL6YSQ'
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

os.environ['GIPHY_API_KEY'] = 'K8e8gV22TDP3EqDDLJpQnMk7mC9rGabd'
GIPHY_API_KEY = os.environ.get('GIPHY_API_KEY')

os.environ['OPENSEA_API_KEY'] = '2877331895414bdf8991a1cdfc9f50bc'
OPENSEA_API_KEY = os.environ.get('OPENSEA_API_KEY')

def fetch_gif(search_term):
    '''根據搜尋條件從 Giphy 獲取 GIF URL。'''
    params = {'q': search_term, 'api_key': GIPHY_API_KEY, 'limit': 1}
    url = 'http://api.giphy.com/v1/gifs/search'
    resp = requests.get(url, params=params)
    data = resp.json()
    if len(data['data']) > 0:
        gif_url = data['data'][0]['images']['original']['url']
        return gif_url
    else:
        return None

def send_gif(update, context):
    '''處理 /gif 命令並將 GIF 發送到聊天中。'''
    if not context.args:
        update.message.reply_text("你必須提供搜尋條件。")
        return

    search_term = ' '.join(context.args)
    gif_url = fetch_gif(search_term)
    if gif_url is not None:
        chat_id = update.message.chat_id
        context.bot.send_animation(chat_id=chat_id, animation=gif_url)
    else:
        update.message.reply_text("對不起，我找不到該條件的任何 GIF。")

def fetch_opensea_nft(asset_contract_address, token_id):
    url = f"https://api.opensea.io/api/v1/asset/{asset_contract_address}/{token_id}/"
    headers = {
    "X-API-KEY": OPENSEA_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {'info': data}
    else:
        return None

def nft(update: Update, context: CallbackContext):
    if len(context.args) != 2:
        update.message.reply_text("你必須提供資產合約地址和代幣 ID。")
        return
    asset_contract_address, token_id = context.args
    nft_data = fetch_opensea_nft(asset_contract_address, token_id)
    if nft_data:
        nft_info = nft_data['info']
        image_url = nft_info['image_url']
        name = nft_info['name']
        url = nft_info['permalink']

        keyboard = [[InlineKeyboardButton("在 OpenSea 上開啟", url=url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        caption = f"名稱: {name}"
        update.message.reply_photo(photo=image_url, caption=caption, reply_markup=reply_markup)
    else:
        update.message.reply_text("對不起，我找不到該 NFT 的任何資訊。")

def penguin(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("你必須提供代幣 ID。")
        return
    token_id = context.args[0]
    asset_contract_address = '0xBd3531dA5CF5857e7CfAA92426877b022e612cf8'  # 將此替換為你的企鵝的合約地址
    nft_data = fetch_opensea_nft(asset_contract_address, token_id)
    if nft_data:
        nft_info = nft_data['info']
        image_url = nft_info['image_url']
        name = nft_info['name']
        url = nft_info['permalink']

        keyboard = [[InlineKeyboardButton("在 OpenSea 上開啟", url=url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        caption = f"名稱: {name}"
        update.message.reply_photo(photo=image_url, caption=caption, reply_markup=reply_markup)
    else:
        update.message.reply_text("對不起，我找不到該 NFT 的任何資訊。")

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Here are the commands you can use:\n'
        '/penguin [token_id] - Send a penguin NFT image. You need to provide the token ID of the penguin NFT after the command.\n'
        '/nft [address] [token_id] - Get information about an NFT. You need to provide the address and the token ID of the NFT after the command.\n'
        '/gif [keyword] - Get a random GIF related to the keyword. This command will send you a random GIF from Giphy related to the keyword you provided.\n'
        '/help - Show this help message. This will provide you with information about all the available commands.'
    )

# Telegram Bot 設定
print("Telegram token:", TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

# Add command handlers
updater.dispatcher.add_handler(CommandHandler('gif', send_gif))
updater.dispatcher.add_handler(CommandHandler('nft', nft))
updater.dispatcher.add_handler(CommandHandler('penguin', penguin))
updater.dispatcher.add_handler(CommandHandler('help', help_command))

# 啟動 Bot
updater.start_polling()