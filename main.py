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
    "gym-girl",
    "cosplay-girl",
    "body-girl",
    "micro-bikini",
    "korean-girl",
    "gai-viet",
]

# key_words_random = random.randint(0, len(key_words_list) - 1)

# images_url_list = get_images_list(key_words_list[key_words_random])

# image_random = random.randint(0, len(images_url_list) - 1)


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.send_photo(message, "HELLO, how are you doing?")


# ảnh gái xinh
@bot.message_handler(commands=["bulul"])
def them_bu_lul(message):
    key_words_random = random.randint(0, len(key_words_list) - 1)
    print(get_images_list(key_words_list[key_words_random]))
    images_url_list = get_images_list(key_words_list[key_words_random])
    image_random = random.randint(0, len(images_url_list) - 1)
    # print(images_url_list[image_random], key_words_list[key_words_random])
    bot.send_photo(chat_id=message.chat.id, photo=images_url_list[image_random])


###################################################################################################

# call api get vids
url = "https://tiktok-video-no-watermark2.p.rapidapi.com/feed/search"
headers = {
    "X-RapidAPI-Key": "edf50f496amshfb8471d5b2ae4f6p15f8d3jsn65e9d00b9773",
    "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com",
}


def get_video():
    videos_result = []
    cursor = random.randint(1, 50)
    keyword = random.choice(["#gaixinh", "#gaixinhtiktok", "gái xinh", "bikini"])
    querystring = {
        "keywords": keyword,
        "count": "30",  # maximum 30 video 1 time
        "cursor": cursor,
        "region": "VN",
        "publish_time": "0",
        "sort_type": "0",
    }
    response = requests.get(url, headers=headers, params=querystring).json()
    videos = response["data"]["videos"]
    for video in videos:
        videos_result.append(video["play"])
    try:
        random_vid = videos_result[random.randint(0, len(videos_result) - 1)]
    except Exception as err:
        print(err)
    return random_vid


# vid gái xinh
@bot.message_handler(commands=["buvid"])
def tiktok_random(message):
    tiktok_video = get_video()
    bot.send_video(chat_id=message.chat.id, video=tiktok_video)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "?????")


bot.infinity_polling()
