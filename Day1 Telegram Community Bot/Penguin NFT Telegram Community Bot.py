import os
import requests
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater

# 1. Environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')
OPENSEA_API_KEY = os.getenv('OPENSEA_API_KEY')
PENGUIN_CONTRACT_ADDRESS = os.getenv('PENGUIN_CONTRACT_ADDRESS')

def fetch_gif(search_term):
    '''Fetch GIF URL from Giphy according to the search term.'''
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
    '''Handle /gif command and send GIF to the chat.'''
    if not context.args:
        update.message.reply_text("You must provide a search term.")
        return

    search_term = ' '.join(context.args)
    gif_url = fetch_gif(search_term)
    if gif_url is not None:
        chat_id = update.message.chat_id
        context.bot.send_animation(chat_id=chat_id, animation=gif_url)
    else:
        update.message.reply_text("Sorry, I couldn't find any GIF for that.")

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
        update.message.reply_text("You must provide an asset contract address and token ID.")
        return
    asset_contract_address, token_id = context.args
    nft_data = fetch_opensea_nft(asset_contract_address, token_id)
    if nft_data:
        nft_info = nft_data['info']
        image_url = nft_info['image_url']
        name = nft_info['name']
        url = nft_info['permalink']

        keyboard = [[InlineKeyboardButton("Open on OpenSea", url=url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        caption = f"Name: {name}"
        update.message.reply_photo(photo=image_url, caption=caption, reply_markup=reply_markup)
    else:
        update.message.reply_text("Sorry, I couldn't find any information about the NFT.")

def penguin(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("You must provide a token ID.")
        return
    token_id = context.args[0]
    nft_data = fetch_opensea_nft(PENGUIN_CONTRACT_ADDRESS, token_id)
    if nft_data:
        nft_info = nft_data['info']
        image_url = nft_info['image_url']
        name = nft_info['name']
        url = nft_info['permalink']

        keyboard = [[InlineKeyboardButton("Open on OpenSea", url=url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        caption = f"Name: {name}"
        update.message.reply_photo(photo=image_url, caption=caption, reply_markup=reply_markup)
    else:
        update.message.reply_text("Sorry, I couldn't find any information about the NFT.")

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Here are the commands you can use:\n'
        '/penguin [token_id] - Send a penguin NFT image. You need to provide the token ID of the penguin NFT after the command.\n'
        '/nft [address] [token_id] - Get information about an NFT. You need to provide the address and the token ID of the NFT after the command.\n'
        '/gif [keyword] - Get a random GIF related to the keyword. This command will send you a random GIF from Giphy related to the keyword you provided.\n'
        '/help - Show this help message. This will provide you with information about all the available commands.'
    )

# Telegram Bot settings
print("Telegram token:", TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

# Add command handlers
updater.dispatcher.add_handler(CommandHandler('gif', send_gif))
updater.dispatcher.add_handler(CommandHandler('nft', nft))
updater.dispatcher.add_handler(CommandHandler('penguin', penguin))
updater.dispatcher.add_handler(CommandHandler('help', help_command))

# Start the Bot
updater.start_polling()