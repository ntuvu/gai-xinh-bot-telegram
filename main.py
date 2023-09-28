import requests
import urllib.parse
import random
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# print(BOT_TOKEN)

####################################################################################################

source = "https://www.pinterest.com/resource/BaseSearchResource/get/"


def source_url_param(keyword):
    return f"/search/pins/?q={urllib.parse.quote(keyword)}"


def data_param(keyword):
    return f"""
    {{"options":{{"isPrefetch":false,"query":"{urllib.parse.quote(keyword)}","scope":"pins","no_fetch_context_on_resource":false}},"context":{{}}}}
    """


def call_api(url, keyword):
    try:
        params = {"source_url": source_url_param(keyword), "data": data_param(keyword)}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except Exception as e:
        print(e)


def get_images_list(keyword):
    try:
        response_data = call_api(source, keyword)
        # image_url = response_data["resource_response"]["data"]["results"][0]["images"][
        #     "orig"
        # ]
        resource_response = response_data["resource_response"]
        data = resource_response["data"]
        results = data["results"]
        res = []
        for result in results:
            res.append(result["images"]["orig"]["url"])
        return res
    except Exception as e:
        print(e)


key_words_list = [
    "asiangirl",
    "gymgirl-vietnam",
    "vietnamesegirl",
    "bikini-asian",
    "vietnam-tiktoker",
    "chinesegirl",
]

# key_words_random = random.randint(0, len(key_words_list) - 1)

# images_url_list = get_images_list(key_words_list[key_words_random])

# image_random = random.randint(0, len(images_url_list) - 1)

# print(images_url_list[image_random], key_words_list[key_words_random])


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.send_photo(message, "HELLO, how are you doing?")


@bot.message_handler(commands=["bulul"])
def them_bu_lul(message):
    key_words_random = random.randint(0, len(key_words_list) - 1)
    images_url_list = get_images_list(key_words_list[key_words_random])
    image_random = random.randint(0, len(images_url_list) - 1)
    bot.send_photo(chat_id=message.chat.id, photo=images_url_list[image_random])


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
