import os
import telebot
import youtube_dl
import glob
from telebot import types
from django.conf import settings

bot = telebot.TeleBot(settings.BOT_TOKEN)


def delete_history_files():
    for f in glob.glob("*.mp3"):
        os.remove(f)
    for f in glob.glob("*.ogg"):
        os.remove(f)
    for f in glob.glob("*.mp4"):
        os.remove(f)
    for f in glob.glob("*.mkv"):
        os.remove(f)
    for f in glob.glob("*.mov"):
        os.remove(f)
    
def button():
    types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    markup.add("video", "sound")
    return markup


user_dict = {}

class Url:
    def __init__(self, url):
        self.url = url

def handler(message):
    delete_history_files()
    id_user = message.chat.id
    url = message.text
    video_url = Url(url)
    user_dict[id_user] = video_url
    message = bot.send_message(id_user, "Choose what you want to download", reply_markup=button())
    bot.register_next_step_handler(message, chooser)

def chooser(message):
    id_user = message.chat.id
    text = message.text
    print(text)
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=Url.url, download=False
    )
    if text == 'sound':
        filename = f"{video_info['title']}.mp3"
        options = {
            "format": "bestaudio/best",
            "keepvideo": False,
            "outtmpl": filename,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info["webpage_url"]])
        
        bot.send_audio(id_user, audio=open(filename, 'rb'))

# def download_sound(self):
#     print(self.video_url)   
#     self.delete_history_files()
#     video_info = youtube_dl.YoutubeDL().extract_info(
#         url=self.video_url, download=False
#     )
#     filename = f"{video_info['title']}.mp3"
#     options = {
#         "format": "bestaudio/best",
#         "keepvideo": False,
#         "outtmpl": filename,
#     }

#     with youtube_dl.YoutubeDL(options) as ydl:
#         ydl.download([video_info["webpage_url"]])
    
#     # with youtube_dl.YoutubeDL({}) as ydl:
#     #     ydl.download([video_info["webpage_url"]])

    
#     bot.send_audio(self.user_id, audio=open(filename, 'rb'))


# def download_video(self):
#     pass



class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


# Handle '/start' and '/help'
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, I am Example bot.
What's your name?
""")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Male') or (sex == u'Female'):
            user.sex = sex
        else:
            raise Exception("Unknown sex")
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'oooops')