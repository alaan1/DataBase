import telebot
import sqlite3, os
from datetime import datetime
import re
from time import time, sleep
from telegram.error import BadRequest
from telebot.apihelper import ApiTelegramException
from collections import defaultdict
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
sql_special_chars = ['%', '_', "'", '"', '\\', ';', '--', '/*', '*/', '#', '|', '&', '$', '@', '!', '`', '~', '^', '<', '>', '=', '+', '-', '*', '/', ',', '.', ':', '?', '(', ')', '[', ']']
banned_from_bot = []
	
admin_ids=[
	"2067261869",
]
mandatory_subscription_message = {
    "text": '''• عذراً عزيزي #الاسم_كرابط
• يجب عليك الاشتراك في قناة المطور أولا
• اشترك ثم ارسل /start ''',
    "photo": None,
    "video": None
}
admin_id = "2067261869"
bot_token="7972716815:AAEcU3sqko0E4tqIr4qkQ8PhaVsyFk4ficU"




def extract_non_empty_strings(nested_list):
	return [item for sublist in nested_list for item in sublist if item]

bot = telebot.TeleBot(token=bot_token,skip_pending=True)

admin_user=bot.get_chat(admin_id).username


MODE_FILE = "mode2.txt"
def check_and_create_files():
	if not os.path.exists(MODE_FILE):
		with open(MODE_FILE, 'w') as file:
			file.write('public')
	if not os.path.exists('users.txt'):
		with open('users.txt', 'w') as h:
			pass
	if not os.path.exists('ids.txt'):
		with open('ids.txt') as g:
			pass
	if not os.path.exists('ch.txt'):
		with open('ch.txt') as k:
			pass
def get_mode():
    try:
        with open(MODE_FILE, "r") as file:
            mode = file.read().strip()
            if mode not in ["private", "public"]:
                raise ValueError
            return mode
    except (FileNotFoundError, ValueError):
        with open(MODE_FILE, "w") as file:
            file.write("public")
        return "public"

def toggle_mode():
    new_mode = "private" if get_mode() == "public" else "public"
    with open(MODE_FILE, "w") as file:
        file.write(new_mode)
    return new_mode
def translate_mode(mode):
    return "المدفوع" if mode == "private" else "المجاني"

user_last_request_time = defaultdict(lambda: 0)
RATE_LIMIT_SECONDS = 2
def rate_limited(func):
	def wrapper(message):
		user_id = message.from_user.id
		current_time = time()
		if current_time - user_last_request_time[user_id] > RATE_LIMIT_SECONDS:
			user_last_request_time[user_id] = current_time
			return func(message)
		else:
			bot.send_message(user_id, "انتضر عزيزي / حاول بعد قليل")
	return wrapper

#############BUTTONS###########


admin_main_page = telebot.types.InlineKeyboardMarkup()
admin_main_page.row_width = 2
ooio = telebot.types.InlineKeyboardButton(text =' اداره المستخدمين', callback_data= "show_oo")
change_mode = telebot.types.InlineKeyboardButton(text ='الوضع الحالي : {}', callback_data= "toggle_mode")
show_userss = telebot.types.InlineKeyboardButton(text ='عدد المشتركين', callback_data= "show_number_ad")
ch_mumber = telebot.types.InlineKeyboardButton(text="اعـداد القنـوات",callback_data="channel_number")
broadcast=telebot.types.InlineKeyboardButton(text ='اذاعة للكل 📢 ', callback_data= 'broadcast')
broadcast2=telebot.types.InlineKeyboardButton(text ='اعـداد رسائل الـ /𝑆𝒕𝒂𝒓𝒕 الاضـافي', callback_data= 'set_message_menu')
habit_board_st=telebot.types.InlineKeyboardButton(text ='عـرض لـوحه الاعضـاء ', callback_data= "habit_board_start")
admin_main_page.row(ooio)
admin_main_page.row(ch_mumber)
admin_main_page.row(change_mode)
admin_main_page.row(show_userss)
admin_main_page.row(broadcast)
admin_main_page.row(broadcast2)
admin_main_page.row(habit_board_st)
admin_main_page.row(telebot.types.InlineKeyboardButton('( جلب التخزين )',callback_data='GetFiles'))
all_city=telebot.types.InlineKeyboardMarkup()
all_city.row_width=3
mesan=telebot.types.InlineKeyboardButton(text ='ميسان', callback_data= 'ct_mesan')
muthana=telebot.types.InlineKeyboardButton(text ='مثنى', callback_data= 'ct_muthana')
najaf=telebot.types.InlineKeyboardButton(text ='نجف', callback_data= 'ct_najaf')
nineveh=telebot.types.InlineKeyboardButton(text ='نينوى', callback_data= 'ct_nineveh')
diyala=telebot.types.InlineKeyboardButton(text ='ديالى', callback_data= 'ct_diyala')
duhok=telebot.types.InlineKeyboardButton(text ='دهوك', callback_data= 'ct_duhok')
erbil=telebot.types.InlineKeyboardButton(text ='اربيل', callback_data= 'ct_erbil')
karbalaa=telebot.types.InlineKeyboardButton(text ='كربلاء', callback_data= 'ct_karbalaa')
kirkuk=telebot.types.InlineKeyboardButton(text ='كركوك', callback_data= 'ct_kirkuk')
qadisiya=telebot.types.InlineKeyboardButton(text ='قادسية', callback_data= 'ct_qadisiya')
salahaldeen=telebot.types.InlineKeyboardButton(text ='صلاح الدين', callback_data= 'ct_salahaldeen')
sulaymaniyah=telebot.types.InlineKeyboardButton(text ='سليمانية', callback_data= 'ct_sulaymaniyah')
wasit=telebot.types.InlineKeyboardButton(text ='واسط', callback_data= 'ct_wasit')
babylon=telebot.types.InlineKeyboardButton(text ='بابل', callback_data= 'ct_babylon')
baghdad=telebot.types.InlineKeyboardButton(text ='بغداد', callback_data= 'ct_baghdad')
balad=telebot.types.InlineKeyboardButton(text ='بلد', callback_data= 'ct_balad')
basrah=telebot.types.InlineKeyboardButton(text ='البصرة', callback_data= 'ct_basrah')
dhiqar=telebot.types.InlineKeyboardButton(text ='ذي قار', callback_data= 'ct_dhiqar')
alanbar=telebot.types.InlineKeyboardButton(text ='الأنبار', callback_data= 'ct_alanbar')
get_linked_all_button=telebot.types.InlineKeyboardButton(text ='بحث عام 🔎', callback_data= 'ct_all')
all_city.add(mesan, muthana, najaf, nineveh, diyala, duhok, erbil, karbalaa, kirkuk, qadisiya, salahaldeen, sulaymaniyah, wasit, babylon, baghdad, balad, basrah, dhiqar)
all_city.row(alanbar, get_linked_all_button)

back_to_admin_menu=telebot.types.InlineKeyboardMarkup()
back_to_admin_menu.row_width=1
back_to_admin_button=telebot.types.InlineKeyboardButton(text ='🔙', callback_data= 'back_to_admin')
back_to_admin_menu.add(back_to_admin_button)

back_to_set_message_menu=telebot.types.InlineKeyboardMarkup()
back_to_set_message_menu.row_width=1
back_to_set_message_start_menu=telebot.types.InlineKeyboardButton(text ='🔙', callback_data= "set_message_menu")
back_to_set_message_menu.add(back_to_set_message_start_menu)


back_to_cities_menu=telebot.types.InlineKeyboardMarkup()
back_to_cities_menu.row_width=1
back_to_cities_button=telebot.types.InlineKeyboardButton(text ='🔙', callback_data= 'back_to_cities')
back_to_cities_menu.add(back_to_cities_button)

back_to_show_oo_menu=telebot.types.InlineKeyboardMarkup()
back_to_show_oo_menu.row_width=1
back_to_show_oo=telebot.types.InlineKeyboardButton(text ='🔙', callback_data= "show_oo")
back_to_show_oo_menu.add(back_to_show_oo)

find_familly=telebot.types.InlineKeyboardMarkup()
find_familly.row_width=1
find_familly_button=telebot.types.InlineKeyboardButton(text ='البحث عن العائلة 🔍', callback_data= 'find_familly')
find_familly.add(find_familly_button)

#############BUTTONS###########


def verify_access(message):
    try:
        # Validate message object
        if not message or not hasattr(message, 'chat') or not hasattr(message, 'from_user'):
            raise ValueError("Invalid message object")
            
        user_id_bot = message.chat.id
        user_id = message.from_user.id
        
        # Read mode file with error handling
        try:
            with open('mode2.txt', 'r') as f:
                mode = f.read().strip()
        except FileNotFoundError:
            print("mode2.txt file not found")
            return None
        except IOError as e:
            print(f"Error reading mode2.txt: {e}")
            return None
            
        # Read users file with error handling    
        try:
            with open('users.txt', 'r') as f:
                subscribed_users = f.read().splitlines()
        except FileNotFoundError:
            print("users.txt file not found")
            return None
        except IOError as e:
            print(f"Error reading users.txt: {e}")
            return None

        if str(user_id_bot) in admin_ids:
            return "admin"
        else:
            is_premium = False
            is_subscribed = 0
            is_public = False
            
            # Check bot channel subscriptions
            try:
                for bot_channel in bot_channels():
                    member = bot.get_chat_member(chat_id=bot_channel, user_id=message.chat.id)
                    if member.status in ["member", "administrator", "creator"]:
                        is_subscribed += 1
            except Exception as e:
                print(f"Error checking channel membership: {e}")
                return None

            if mode == "public":
                is_public = True
            elif mode == "private":
                for idd in subscribed_users:
                    if str(idd) == str(user_id_bot):
                        is_premium = True
                        break

        # Return access status
        if is_public and is_subscribed == len(bot_channels()):
            return "done"
        elif not is_public and is_premium and is_subscribed == len(bot_channels()):
            return "done" 
        elif not is_public and not is_premium and int(is_subscribed) == len(bot_channels()):
            return "not premium"
        elif not is_public and not is_premium and int(is_subscribed) != len(bot_channels()):
            return "not subscribed"
        elif int(is_subscribed) != len(bot_channels()):
            return "not subscribed"
            
    except Exception as e:
        print(f"Unexpected error in verify_access: {e}")
        return None

@bot.message_handler(commands=['help'])
def help_command(message):
    HELP_MESSAGE = """
اهلا بك في لوحه التعليم: 👨‍🏫

يمكنك الان البحث بعدة طرق تابع الخطوات:
- يمكنك البحث عبر الاسم الثلاثي مع المواليد
مثال على ذالك : 🏅
- محمد علي محمد 2005

- يمكنك البحث عن طريق الاسم الثلاثي ايضا : 🎗️

مثال على ذالك : 🎯
- محمد علي محمد

- كيف البحث عن الاسماء مركبه : 🎲
الاسماء المركبه تدمج مثال: 🪄

- عبدالكريم حسن محمد 2005
- نورالهدى حسن عبدالكريم 2000

- كيف ابحث البحث الصحيح :

كتابه الاسماء الذي يكون فيها. ( ة )
لا تكتب ( ة )
- مثال على ذالك. : 🖋️

- فاطمه وليس فاطمة ❌
- فاطمه علي محمد ✅

اضغط /start مره اخرا
"""
    bot.reply_to(message, HELP_MESSAGE)

def back_to_admin_menu_function(message):
	mode = get_mode()
	admin_main_page.keyboard[2][0].text = "الوضع الحالي : {}".format(translate_mode(mode))
	bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=f"مرحبا بك عزيزي المالك يمكنك التحكم بالبوت من خلال الازرار التاليه :", reply_markup=admin_main_page)

@bot.message_handler(commands=['start'])
@rate_limited
def start_messaging(message):
	stats=verify_access(message)
	mode = get_mode()
	user_id = message.from_user.id
	if bot_channels() and not check_mandatory_subscription(message):
		return
	elif user_id in banned_from_bot:
		bot.send_message(user_id, "نجب لك انته ضاربيك نعال ⁴²")
		return
	elif stats=="admin":
		for msg in custom_messages:
			bot.send_message(user_id, msg)
		admin_main_page.keyboard[2][0].text = "الوضع الحالي : {}".format(translate_mode(mode))
		bot.reply_to(message, "مرحبا بك عزيزي المالك يمكنك التحكم بالبوت من خلال الازرار التاليه :", reply_markup=admin_main_page)
	elif stats=="done":
		for msg in custom_messages:
			bot.send_message(user_id, msg)
		bot.reply_to(message,'''>  **✦ اهــلًا بـك فـي بـوت داتا بيس العراق 🇮🇶**\n
>||**🔎 يمكنك معرفة جميع العوائل العراقية**||\n
> **📝 وذلك عبر البحث بالاسم الثلاثي**\n
> **📌 اختر المدينة للمتابعة:**\n
> **ارسل /help و اتبع التعليمات ♦️**\n
    ''',reply_markup=all_city,parse_mode='MarkdownV2')
	elif stats=="not premium":
		for msg in custom_messages:
			bot.send_message(user_id, msg)
		bot.reply_to(message, f"انت غير مشترك في البوت، للاشتراك الVIP راسل الادمن : @{admin_user}")
	id=str(message.from_user.id)
	username=str(message.from_user.username)
	name=str(message.from_user.first_name)
	is_new_user=True
	read=open('ids.txt', 'r').read().splitlines()
	for idd in read:
		if str(idd)==str(id):
			is_new_user=False
		else:
			pass
	if is_new_user==True:
		with open('ids.txt', 'a') as f:
			f.write(str(id)+'\n')
			f.close()
		users=str(len(open('ids.txt', 'r').read().splitlines()))
		for admin_id in admin_ids:
			bot.send_message(admin_id, f"""
• معلومات العضو الجديد .
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
• الاسم : {name}
• معرف : @{username}
• الايدي : {id}
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
• عدد الأعضاء الكليي :  > {users} <
""")
	else:
		pass

def broadcast_function(message):
	br_msg=bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="حسنا، الان ارسل الرسالة لاذاعتها لكل مستخدمين البوت.", reply_markup=back_to_admin_menu)
	bot.register_next_step_handler(br_msg, broadcast_message_handler)

def broadcast_message_handler(message):
    user_id = message.chat.id
    broadcast_content = {}
    broadcast_type = "غير معرف 😕"
    if message.photo and (message.text or message.caption):
        broadcast_type = "نص 💬 + صورة 📷"
        broadcast_content = {
            "type": "photo",
            "photo": message.photo[-1].file_id,
            "caption": message.text or message.caption
        }
    elif message.video and (message.text or message.caption):
        broadcast_type = "نص 💬 + فيديو 🎥"
        broadcast_content = {
            "type": "video",
            "video": message.video.file_id,
            "caption": message.text or message.caption
        }
    elif message.document and (message.text or message.caption):
        broadcast_type = "نص 💬 + ملف 📂"
        broadcast_content = {
            "type": "document",
            "document": message.document.file_id,
            "caption": message.text or message.caption
        }
    elif message.animation and (message.text or message.caption):
        broadcast_type = "نص 💬 + متحركة 🎞️"
        broadcast_content = {
            "type": "animation",
            "animation": message.animation.file_id,
            "caption": message.text or message.caption
        }
    elif message.voice and (message.text or message.caption):
        broadcast_type = "نص 💬 + بصمة صوتية 🎙️"
        broadcast_content = {
            "type": "voice",
            "voice": message.voice.file_id,
            "caption": message.text or message.caption
        }
    elif message.audio and (message.text or message.caption):
        broadcast_type = "نص 💬 + صوت 🎵"
        broadcast_content = {
            "type": "audio",
            "audio": message.audio.file_id,
            "caption": message.text or message.caption
        }
    elif message.text:
        broadcast_type = "نص 💬"
        broadcast_content = {"type": "text", "text": message.text}
    elif message.photo:
        broadcast_type = "صورة 📷"
        broadcast_content = {"type": "photo", "photo": message.photo[-1].file_id}
    elif message.video:
        broadcast_type = "فيديو 🎥"
        broadcast_content = {"type": "video", "video": message.video.file_id}
    elif message.document:
        broadcast_type = "ملف 📂"
        broadcast_content = {"type": "document", "document": message.document.file_id}
    elif message.animation:
        broadcast_type = "متحركة 🎞️"
        broadcast_content = {"type": "animation", "animation": message.animation.file_id}
    elif message.voice:
        broadcast_type = "بصمة صوتية 🎙️"
        broadcast_content = {"type": "voice", "voice": message.voice.file_id}
    elif message.audio:
        broadcast_type = "صوت 🎵"
        broadcast_content = {"type": "audio", "audio": message.audio.file_id}
    elif message.sticker:
        broadcast_type = "ملصق 🏷️"
        broadcast_content = {"type": "sticker", "sticker": message.sticker.file_id}
    broadcast_message(message)
    user_link = f"[{message.from_user.first_name}](tg://user?id={user_id})"
    confirmation_message = (
        f"⌔︙عـزيـزي : {user_link}\n"
        f"⌔︙تم الاذاعه الى مستخدمين البوت بنجاح \n"
        f"⌔︙نوع الاذاعه : 「 `{broadcast_type}` 」"
    )
    bot.reply_to(message, confirmation_message, parse_mode="Markdown")


def broadcast_message(message):
    if message.photo and (message.text or message.caption):
        broadcast_type = "نص 💬 + صورة 📷"
        broadcast_content = {
            "type": "photo",
            "photo": message.photo[-1].file_id,
            "caption": message.text or message.caption
        }
    elif message.video and (message.text or message.caption):
        broadcast_type = "نص 💬 + فيديو 🎥"
        broadcast_content = {
            "type": "video",
            "video": message.video.file_id,
            "caption": message.text or message.caption
        }
    elif message.document and (message.text or message.caption):
        broadcast_type = "نص 💬 + ملف 📂"
        broadcast_content = {
            "type": "document",
            "document": message.document.file_id,
            "caption": message.text or message.caption
        }
    elif message.animation and (message.text or message.caption):
        broadcast_type = "نص 💬 + متحركة 🎞️"
        broadcast_content = {
            "type": "animation",
            "animation": message.animation.file_id,
            "caption": message.text or message.caption
        }
    elif message.voice and (message.text or message.caption):
        broadcast_type = "نص 💬 + بصمة صوتية 🎙️"
        broadcast_content = {
            "type": "voice",
            "voice": message.voice.file_id,
            "caption": message.text or message.caption
        }
    elif message.audio and (message.text or message.caption):
        broadcast_type = "نص 💬 + صوت 🎵"
        broadcast_content = {
            "type": "audio",
            "audio": message.audio.file_id,
            "caption": message.text or message.caption
        }
    elif message.text:
        broadcast_type = "نص 💬"
        broadcast_content = {"type": "text", "text": message.text}
    elif message.photo:
        broadcast_type = "صورة 📷"
        broadcast_content = {"type": "photo", "photo": message.photo[-1].file_id}
    elif message.video:
        broadcast_type = "فيديو 🎥"
        broadcast_content = {"type": "video", "video": message.video.file_id}
    elif message.document:
        broadcast_type = "ملف 📂"
        broadcast_content = {"type": "document", "document": message.document.file_id}
    elif message.animation:
        broadcast_type = "متحركة 🎞️"
        broadcast_content = {"type": "animation", "animation": message.animation.file_id}
    elif message.voice:
        broadcast_type = "بصمة صوتية 🎙️"
        broadcast_content = {"type": "voice", "voice": message.voice.file_id}
    elif message.audio:
        broadcast_type = "صوت 🎵"
        broadcast_content = {"type": "audio", "audio": message.audio.file_id}
    elif message.sticker:
        broadcast_type = "ملصق 🏷️"
        broadcast_content = {"type": "sticker", "sticker": message.sticker.file_id}
    users_ids=open('ids.txt').read().splitlines()
    for user_id in users_ids:
        try:
            if broadcast_content["type"] == "text":
                bot.send_message(user_id, broadcast_content["text"])
            elif broadcast_content["type"] == "photo":
                bot.send_photo(user_id, broadcast_content["photo"], caption=broadcast_content["caption"])
            elif broadcast_content["type"] == "video":
                bot.send_video(user_id, broadcast_content["video"], caption=broadcast_content["caption"])
            elif broadcast_content["type"] == "document":
                bot.send_document(user_id, broadcast_content["document"], caption=broadcast_content["caption"])
            elif broadcast_content["type"] == "animation":
                bot.send_animation(user_id, broadcast_content["animation"], caption=broadcast_content["caption"])
            elif broadcast_content["type"] == "voice":
                bot.send_voice(user_id, broadcast_content["voice"], caption=broadcast_content["caption"])
            elif broadcast_content["type"] == "audio":
                bot.send_audio(user_id, broadcast_content["audio"], caption=broadcast_content["caption"])
            elif broadcast_content["type"] == "sticker":
                bot.send_sticker(user_id, broadcast_content["sticker"])
        except:
            pass
custom_messages = [] 

def save_custom_message(message):
	global custom_messages
	custom_messages.append(message.text)
	bot.send_message(message.chat.id, "تم حفـظ الرساله بنجـاح .")

def list_to_numbered_string(input_list):
	return '\n'.join([f"{i+1}- `{item}`" for i, item in enumerate(input_list)])
user_states = {}


def channel_number_qn(call):
    user_id = call.message.chat.id
    markup_kk_krem = telebot.types.InlineKeyboardMarkup()
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("مسح قناة", callback_data='delqn'),
                           telebot.types.InlineKeyboardButton("تفعيل قناة", callback_data='qn'))
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("تغيير كليـشه الاشـتراك الاجباري ", callback_data="change_subscription_message"))
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("القنوات المضافه ", callback_data='listqn'))
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("🔙", callback_data="back_to_admin"))
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text="اختر ما تريد من الأزرار",
            reply_markup=markup_kk_krem
        )
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error sending message: {e}")
def back_channel_number_qn(call):
    user_id = call.message.chat.id
    user_states.pop(user_id, None)
    markup_kk_krem = telebot.types.InlineKeyboardMarkup()
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("مسح قناة ", callback_data='delqn'),
                           telebot.types.InlineKeyboardButton("تفعيل قناة ", callback_data='qn'))
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("تغيير كليـشه الاشـتراك الاجباري ", callback_data="change_subscription_message"))
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("القنوات المضافه ", callback_data='listqn'))
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("🔙", callback_data="back_to_admin"))
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text="اختر ما تريد من الأزرار",
            reply_markup=markup_kk_krem
        )
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error sending message: {e}")
def ser_message_start_menu(call):
    user_id = call.message.chat.id
    markup_kk_krem = telebot.types.InlineKeyboardMarkup()
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("تـعييـن رسـالـه  ", callback_data='set_message'),
                           telebot.types.InlineKeyboardButton("مـسـح الرسـالـه  ", callback_data='delete_message'))
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("عـرض الرسـائـل  ", callback_data="view_messages"))
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("🔙", callback_data="back_to_admin"))
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text="اختر ما تريد من الأزرار",
            reply_markup=markup_kk_krem
        )
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error sending message: {e}")


@bot.callback_query_handler(func=lambda call: call.data == "change_subscription_message")
def change_subscription_message(call):
    user_states[call.from_user.id] = "waiting_for_new_message"
    markup = telebot.types.InlineKeyboardMarkup()
    back_admin = telebot.types.InlineKeyboardButton("🔙", callback_data="channel_number2")
    markup.add(back_admin)
    bot.edit_message_text(chat_id=call.message.chat.id, 
message_id=call.message.message_id,
text='''⌯︙ارسل لي تغيير كـليشه الاشتـراك الاجبـاري ↫ ⤈

⌯︙يمكنك اضافة الى النص ↫ ⤈
ꔹ┉ ┉ ┉ ┉ ┉ ┉ ┉ꔹ
⌯︙  `#ايدي` ↬ ايدي المستخدم
⌯︙  `#يوزر` ↬ يوزر المستخدم
⌯︙ `#اسم` ↬ اسم المستخدم
⌯︙ `#الاسم_كرابط` ↬ الاسم كرابط للحساب
⌯︙ `#قناه` ↬ لاضهار معرفات القنوات في الاشتراك الاحباري في الرساله
⌯︙ `#القناه_كرابط` ↬ لاضهار اسماء القنوات كرابط في الاشتراك الاحباري في الرساله
ꔹ┉ ┉ ┉ ┉ ┉ ┉ ┉ꔹ
⌯︙ اضغط على الزر للإلغاء '''
,reply_markup=markup)

@bot.message_handler(func=lambda msg: user_states.get(msg.chat.id) == "waiting_for_new_message")
def save_new_subscription_message(message):
    global mandatory_subscription_message
    new_message = {"text": None, "photo": None, "video": None}
    try:
        user_info = message.from_user
        if message.text:
            new_message["text"] = message.text
        elif message.photo:
            new_message["photo"] = message.photo[-1].file_id
            if message.caption:
                new_message["text"] = message.caption
        elif message.video:
            new_message["video"] = message.video.file_id
            if message.caption:
                new_message["text"] = message.caption

        if not any(new_message.values()):
            bot.send_message(
                message.chat.id,
                "⌔︙الرسالة التي أرسلتها لا تحتوي على محتوى صالح. يرجى المحاولة مرة أخرى.",reply_to_message_id=message.message_id
            )
            return
        mandatory_subscription_message.update(new_message)
        user_states.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "⇜ تـم تغـيير الكـليشه بـنجاح",reply_to_message_id=message.message_id)
    except Exception as e:
        bot.send_message(message.chat.id, f"⌔︙حدث خطأ أثناء تحديث الكليشة: {e}",reply_to_message_id=message.message_id)


def extract_channel_id(text):
    if text.startswith('@'):
        return text
    elif 't.me/' in text:
        match = re.search(r"t\.me/(.+)", text)
        if match:
            return '@' + match.group(1)
    elif text.startswith('-100'):
        return text
    return None

def show_banned_from_bot(call,user_id):
    if banned_from_bot:
        markup = InlineKeyboardMarkup()
        banned_list = "\n".join(
            [f"{i+1}- `@{bot.get_chat(user).username}`" for i, user in enumerate(banned_from_bot)]
        )
        bot.edit_message_text(chat_id=call.message.chat.id, 
message_id=call.message.message_id,
text=f"المحـظورين \n{banned_list}"
,parse_mode='Markdown',reply_markup=back_to_show_oo_menu)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, 
message_id=call.message.message_id,
text="ماكو محظورين من البوت"
,parse_mode='Markdown',reply_markup=back_to_show_oo_menu)
def ban_user(message):
    try:
        user_id_to_ban = int(message.text)
        if user_id_to_ban in admin_ids:
            bot.send_message(
                message.chat.id, 
                "⌔︙ماتكـدر تحظـر ادمـن 🗿"
            )
            return
        user_info = bot.get_chat(user_id_to_ban)
        if user_id_to_ban not in banned_from_bot:
            banned_from_bot.append(user_id_to_ban)
            bot.send_message(
                message.chat.id, 
                f"⌔︙عـزيـزي : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                f"⌔︙الهـيوان [{user_info.first_name}](tg://user?id={user_id_to_ban})\n↯︙تم حظره من البوت",
                parse_mode='Markdown'
            )
        else:
            bot.send_message(message.chat.id, "المستخدم محظور بل فعل")
    except ValueError:
        bot.send_message(message.chat.id, "هنالك خطأ")

def unban_user(message):
    try:
        user_id_to_unban = int(message.text)
        user_info = bot.get_chat(user_id_to_unban)
        if user_id_to_unban in banned_from_bot:
            banned_from_bot.remove(user_id_to_unban)
            bot.send_message(
                message.chat.id, 
                f"عـزيـزي : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                f"المستخدم [{user_info.first_name}](tg://user?id={user_id_to_unban})\nتم فك الحظر عنـه",
                parse_mode='Markdown'
            )
        else:
            bot.send_message(message.chat.id, "المستخدم ما محظور اصلاً")
    except ValueError:
        bot.send_message(message.chat.id, "هنالك خطأ ")


def get_users_from_file():
    try:
        with open("ids.txt", "r") as file:
            users = file.read().splitlines()
            cleaned_users = set(
                re.sub(r'[^\d]', '', user_id.strip()) for user_id in users if user_id.strip().isdigit()
            )
            return list(cleaned_users)
    except FileNotFoundError:
        return []
def split_message(text, max_length=2000):
    parts = []
    while len(text) > max_length:
        split_index = text[:max_length].rfind('\n')
        if split_index == -1:
            split_index = max_length
        parts.append(text[:split_index])
        text = text[split_index:].lstrip()
    parts.append(text)
    return parts

def show_users_uu(call):
    users = get_users_from_file()
    if not users:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="لايـوجد مستـخدمين في البوت",
            parse_mode='Markdown',
            reply_markup=back_to_show_oo_menu
        )
        return

    total_count = len(users)
    message_text = f"العـدد الكـلي : {total_count}\n"
    message_text += "— — — — — — — — — — — — — —\n"
    message_text += "المستخدمين:\n"
    valid_users = []

    for i, user_id in enumerate(users, start=1):
        try:
            user = bot.get_chat(chat_id=int(user_id))
            username = user.username if user.username else "لا يوجد"
            message_text += f"{i} ~ {user_id} ~ @{username}\n" if user.username else f"{i} ~ {user_id} ~ {username}\n"
            valid_users.append(user_id)
        except ApiTelegramException:
            continue
    with open("ids.txt", "w") as file:
        file.write("\n".join(valid_users))
    messages = split_message(message_text)
    for i, msg in enumerate(messages):
        if i == 0:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=msg,
                 reply_markup=back_to_show_oo_menu
            )
        else:
            bot.send_message(
                chat_id=call.message.chat.id,
                text=msg,
                 reply_markup=back_to_show_oo_menu
            )
def show_number_ad(call):
    users = get_users_from_file()
    if not users:
        bot.answer_callback_query(call.id, "لايـوجد مستـخدمين في البوت", show_alert=True)
        return
    total_count = len(users)
    bot.answer_callback_query(call.id, f"عـدد الاعضـاء : {total_count}", show_alert=True)

def get_manage_users_in_boted_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton("ازاله ادمن ", callback_data="delete_user"),        InlineKeyboardButton("اضف ادمن ", callback_data="add_user")
    )
    markup.row(
        InlineKeyboardButton("عرض الادمنيه ", callback_data="show_admins")
    )
    markup.row(
        InlineKeyboardButton("ازاله مشتـرك 𝒗𝒊𝒑 ", callback_data="delete_user_users"),        InlineKeyboardButton("اضف مشتـرك 𝒗𝒊𝒑 ", callback_data="add_user_users")
    )
    markup.row(
        InlineKeyboardButton("عرض المشـتركين 𝒗𝒊𝒑 ", callback_data="show_user_users")
    )
    
    markup.row(

        InlineKeyboardButton("فك حظر ", callback_data="unban_user"),        InlineKeyboardButton("حظر مستخدم ", callback_data="ban_user")
    )
    markup.row(
        InlineKeyboardButton("عرض المحظورين ", callback_data="show_banned_from_bot")
    )
    markup.row(
        InlineKeyboardButton("عرض مستخدمين البوت ", callback_data="show_userss")
    )
    markup.add(InlineKeyboardButton("🔙", callback_data='back_to_admin'))
    return markup
@bot.callback_query_handler(func=lambda call: call.data == "GetFiles")
def GetFils(call):
	    bot.answer_callback_query(callback_query_id=call.id, text='انتظر ...', show_alert=True)
	    bot.send_document(call.message.chat.id,document=open('ids.txt','rb'),caption='- ملف تخزين البوت ..')

@bot.callback_query_handler(func=lambda call: call.data == "toggle_mode")
def toggjle_mode(call):
    current_mode = get_mode()
    new_mode = "private" if current_mode == "public" else "public"
    with open(MODE_FILE, "w") as file:
        file.write(new_mode)
    admin_main_page.keyboard[2][0].text = "الوضع الحالي : {}".format(translate_mode(new_mode))
    bot.answer_callback_query(call.id, f"تم تغيير الوضع إلى {translate_mode(new_mode)}")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=admin_main_page)


@bot.callback_query_handler(func=lambda call: True)
def handle_qwery(call):
	bot.clear_step_handler_by_chat_id(call.message.chat.id)
	stats=verify_access(call.message)
	user_id = call.from_user.id
	if call.data == "set_message":
		msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="ارسل الرساله التي تريد تعيينها مع /𝑆𝒕𝒂𝒓𝒕", reply_markup=back_to_set_message_menu)
		bot.register_next_step_handler(msg, save_custom_message)
	elif call.data == "show_userss":
		show_users_uu(call)
	elif call.data == "show_number_ad":
		show_number_ad(call)
	elif call.data == "show_oo":
		bot.edit_message_text(chat_id=call.message.chat.id, 
message_id=call.message.message_id,
text='اداره المسـتخدمين'
,parse_mode='Markdown',reply_markup=get_manage_users_in_boted_menu())
	elif call.data == "add_user_users":
		add_user_function_users(call)
	elif call.data == "delete_user_users":
		delete_user_function_users(call)
	elif call.data == "show_user_users":
		show_users_users(call)
	elif call.data == "channel_number":
		channel_number_qn(call)
	elif call.data == "set_message_menu":
		ser_message_start_menu(call)
	elif call.data == "channel_number2":
		back_channel_number_qn(call)
	elif call.data == "unban_user":
		msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="ارسـل ايدي المستخـدم لفك حظـره", reply_markup=back_to_show_oo_menu)
		bot.register_next_step_handler(msg, unban_user)
	elif call.data == "show_admins":
		show_administrative_in_bot(call,user_id)
	elif call.data == "show_banned_from_bot":
		show_banned_from_bot(call,user_id)
	elif call.data == "ban_user":
		msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="ارسـل ايدي المستخـدم لحظـره", reply_markup=back_to_show_oo_menu)
		bot.register_next_step_handler(msg, ban_user)
	elif call.data == "delete_message":
		if custom_messages:
			custom_messages.clear()
			bot.edit_message_text(chat_id=user_id, 
message_id=call.message.message_id,
text="تـم مسـح جميـع الرسـائل ."
,parse_mode='Markdown',reply_markup=back_to_set_message_menu)
		else:
			bot.edit_message_text(chat_id=user_id, 
message_id=call.message.message_id,
text="لاتـوجـد ࢪسائـل تـم تعيينهـا لازالتـها ."
,parse_mode='Markdown',reply_markup=back_to_set_message_menu)
	elif call.data == "view_messages":
		if custom_messages:
			messages_text = "\n".join([f"{i + 1} - {msg}" for i, msg in enumerate(custom_messages)])
			bot.edit_message_text(chat_id=call.message.chat.id, 
message_id=call.message.message_id,
text=f"الࢪسائـل التـي تم تعييـنها هـي \n{messages_text}"
,parse_mode='Markdown',reply_markup=back_to_set_message_menu)
		else:
			bot.edit_message_text(chat_id=call.message.chat.id, 
message_id=call.message.message_id,
text="لا توجـد ࢪسائـل تـم تعييـنها ."
,parse_mode='Markdown',reply_markup=back_to_set_message_menu)
	if stats=="done" or stats=="admin":		 
		if call.data == 'delqn':
			txt = bot_channels()
			o = list_to_numbered_string(txt) or "ماكو قنوات"
			r = f'القنوات المضافه \n{o}'
			h = bot.send_message(call.message.chat.id,f'ارسل يوزر القناة معه @ .\n— — — — — — — — — — — — — —\n{r}',parse_mode="Markdown")
			bot.register_next_step_handler(h,delqna)
		elif call.data == 'qn':
			txt = bot_channels()
			o = list_to_numbered_string(txt) or "ماكو قنوات"
			r = f'القنوات المضافه \n{o}'
			h = bot.send_message(call.message.chat.id,f'ارسل يوزر القناة معه @ .\n— — — — — — — — — — — — — —\n{r}',parse_mode="Markdown")
			bot.register_next_step_handler(h,qna)
		elif call.data == 'listqn':
			show_eech(call, user_id)
		elif call.data == 'add_user':
			add_user_function(call.message)
		elif call.data == 'delete_user':
			delete_user_function(call.message)
		elif call.data == "habit_board_start":
			try:
				bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text= '''>  **✦ اهــلًا بـك فـي بـوت داتا بيس العراق 🇮🇶**\n
>||**🔎 يمكنك معرفة جميع العوائل العراقية**||\n
> **📝 وذلك عبر البحث بالاسم الثلاثي**\n
> **📌 اختر المدينة للمتابعة:**\n
> **ارسل /help و اتبع التعليمات ♦️**\n 
    ''',
            reply_markup=all_city,parse_mode='MarkdownV2'
        )
			except telebot.apihelper.ApiTelegramException as e:
				print(f"Error sending message: {e}")
		elif call.data == 'back_to_admin':
			back_to_admin_menu_function(call.message)
		elif call.data == 'back_to_cities':
			back_to_cities_menu_function(call.message)
		elif 'ct_' in str(call.data):
			city=str(call.data).split('ct_')[1]
			chose_serch  = telebot.types.InlineKeyboardMarkup()
			chose_serch.row_width = 2
			chose_serch_button = telebot.types.InlineKeyboardButton(text ='بحث برقم التموينيه🔍', callback_data= f'tamon_number_{city}')
			chose_serch_button2 = telebot.types.InlineKeyboardButton(text ='بحث بالاسم الثلاثي 🔍', callback_data= f'name_search_city_{city}')
			chose_serch.add(chose_serch_button,chose_serch_button2)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f' اختر البحث في المدينه : {city}',parse_mode='Markdown',reply_markup=chose_serch)
		elif  'tamon_number_' in str(call.data):
			city=str(call.data).split('tamon_number_')[1]
			tamon_number_handler(call.message, city)
		elif  'name_search_city_' in str(call.data):
			city=str(call.data).split('name_search_city_')[1]
			search_function(call.message, city)

		elif call.data == 'find_familly':
			find_familly_function(call.message)
		elif call.data=='broadcast':
			broadcast_function(call.message)
	elif stats=="not premium":
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f"انت غير مشترك في البوت، للاشتراك الvip راسل الادمن : @{admin_user}")
	elif stats=="not subscribed":
		if bot_channels() and not check_mandatory_subscription_2(user_id,call):
			return
		

def show_eech(call, user_id):
    with open(CH_FILE, "r") as file:
        channels = file.read().strip().splitlines()
    markup_kk_krem = telebot.types.InlineKeyboardMarkup()
    markup_kk_krem.add(telebot.types.InlineKeyboardButton("🔙", callback_data="channel_number"))
    if not channels:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=" ماكو قـنوات في الاشتراك الاجباري",
            parse_mode='Markdown',
            reply_markup=markup_kk_krem
        )
        return
    channels_list = []
    for i, channel_id in enumerate(channels, start=1):
        try:
            chat = bot.get_chat(channel_id)
            chat_type = "عامة" if chat.username else "خاصة"
            if chat.username:
                channel_display = f"`@{chat.username}`"
            else:
                channel_display = f"`{channel_id}`"
        except Exception:
            channel_display = f"`{channel_id}`"
            chat_type = "غير معروفة"

        channels_list.append(f"{i} ~ {channel_display} ~  {chat_type} ")

    channels_text = "\n".join(channels_list)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f" القنـوات والمجمـوعات في الاشتـراك الاجبـاري\n— — — — — — — — — — — — —\n{channels_text}",
        parse_mode='Markdown',
        reply_markup=markup_kk_krem
    )


		
def bot_channels():
	bot_channels = []
	f = open('ch.txt').read().splitlines()
	bot_channels.append(f)
	ff = extract_non_empty_strings(bot_channels)
	return ff

CH_FILE = "ch.txt"
def replace_placeholders(text, user, unsubscribed_entities):
    placeholders = {
        "#ايدي": str(user.id),
        "#يوزر": f"@{user.username}" if user.username else "لا يـوجد يـوزر لـك",
        "#اسم": user.first_name or "لايـوجد اسـم لـك",
        "#الاسم_كرابط": f"[{user.first_name}](tg://user?id={user.id})" if user.first_name else "مـاكو 🗿",
        "#قناه": "\n".join(
            [f"{bot.get_chat(entity).title}" for entity in unsubscribed_entities]
        ) if unsubscribed_entities else "انـت منضـم في كـل القـنوات",
        "#القناه_كرابط": "\n".join(
            [f"[{bot.get_chat(entity).title}](https://t.me/c/{entity[4:]})" if str(entity).startswith('-100') else f"[{bot.get_chat(entity).title}](https://t.me/{bot.get_chat(entity).username})" for entity in unsubscribed_entities]
        ) if unsubscribed_entities else "انـت منضـم في كـل القـنوات"
    }
    for placeholder, value in placeholders.items():
        text = text.replace(placeholder, value)
    return text
def check_mandatory_subscription(message):
    unsubscribed_entities = []
    with open(CH_FILE, "r") as file:
        eech2 = file.read().strip().splitlines()
    user_id = message.from_user.id
    for entity in eech2:
        try:
            status = bot.get_chat_member(entity, user_id).status
            if status in ['left', 'kicked']:
                unsubscribed_entities.append(entity)
        except telebot.apihelper.ApiException:
            pass
    if unsubscribed_entities:
        markup = telebot.types.InlineKeyboardMarkup()
        for entity in unsubscribed_entities:
            try:
                entity_info = bot.get_chat(entity)
                entity_name = entity_info.title
                if str(entity).startswith('-100'):
                    if entity_info.invite_link:
                        entity_url = entity_info.invite_link
                    else:
                        entity_url = f"https://t.me/c/{entity[4:]}"
                else:
                    entity_url = f"https://t.me/{entity_info.username}" if entity_info.username else "RQSRR"
                markup.add(
                    telebot.types.InlineKeyboardButton(
                        text=entity_name,
                        url=entity_url
                    )
                )
            except telebot.apihelper.ApiException:
                pass

        user_info = bot.get_chat(user_id)
        customized_message = replace_placeholders(
            mandatory_subscription_message.get("text", ""), user_info, unsubscribed_entities
        )

        try:
            if mandatory_subscription_message.get("photo"):
                bot.send_photo(
                    user_id,
                    mandatory_subscription_message["photo"],
                    caption=customized_message,
                    reply_markup=markup,
                    parse_mode='Markdown',
                    reply_to_message_id=message.message_id
                )
            elif mandatory_subscription_message.get("video"):
                bot.send_video(
                    user_id,
                    mandatory_subscription_message["video"],
                    caption=customized_message,
                    reply_markup=markup,
                    parse_mode='Markdown',
                    reply_to_message_id=message.message_id
                )
            else:
                bot.reply_to(message, customized_message, reply_markup=markup, parse_mode='Markdown')
        except Exception as e:
            print(f"Error sending subscription message: {e}")
        return False
    return True
def check_mandatory_subscription_2(call,user_id):
    unsubscribed_entities = []
    with open(CH_FILE, "r") as file:
        eech2 = file.read().strip().splitlines()
    for entity in eech2:
        try:
            status = bot.get_chat_member(entity, user_id).status
            if status in ['left', 'kicked']:
                unsubscribed_entities.append(entity)
        except telebot.apihelper.ApiException:
            pass
    if unsubscribed_entities:
        markup = telebot.types.InlineKeyboardMarkup()
        for entity in unsubscribed_entities:
            try:
                entity_info = bot.get_chat(entity)
                entity_name = entity_info.title
                if str(entity).startswith('-100'):
                    if entity_info.invite_link:
                        entity_url = entity_info.invite_link
                    else:
                        entity_url = f"https://t.me/c/{entity[4:]}"
                else:
                    entity_url = f"https://t.me/{entity_info.username}" if entity_info.username else "RQSRR"
                markup.add(
                    telebot.types.InlineKeyboardButton(
                        text=entity_name,
                        url=entity_url
                    )
                )
            except telebot.apihelper.ApiException:
                pass
        user_info = bot.get_chat(user_id)
        customized_message = replace_placeholders(
            mandatory_subscription_message.get("text", ""), user_info, unsubscribed_entities
        )
        try:
            if mandatory_subscription_message.get("photo"):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=customized_message,parse_mode='Markdown')
            elif mandatory_subscription_message.get("video"):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=customized_message,parse_mode='Markdown')
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=customized_message,parse_mode='Markdown')
        except Exception as e:
            print(f"Error sending subscription message: {e}")
        return False
    return True


def search_function(message, city):
	city_keys={
	'mesan':'ميسان',
	'muthana':'مثنى',
	'najaf':'نجف',
	'nineveh':'نينوى',
	'diyala':'ديالى',
	'duhok':'دهوك',
	'erbil':'اربيل',
	'karbalaa':'كربلاء',
	'kirkuk':'كركوك',
	'qadisiya':'قادسية',
	'salahaldeen':'صلاح الدين',
	'sulaymaniyah':'سليمانية',
	'wasit':'واسط',
	'babylon':'بابل',
	'baghdad':'بغداد',
	'balad':'بلد',
	'basrah':'بصرة',
	'dhiqar':'ذي قار',
	'alanbar':'الانبار',
	'all':'بحث عام',
	'developer_button':'المطور',
	'channel_button':'القناة'
	}
	user_id = message.from_user.id
	if bot_channels() and not check_mandatory_subscription(message):
		return
	elif user_id in banned_from_bot:
		bot.send_message(user_id, "نجب لك انته ضاربيك نعال ⁴²")
		return
	elif city == 'all':
		name_msg=bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=f'اخترت :  {str(city_keys[str(city)])}\nيجب عليك ارسال  الاسم الثلاثي  \nمثال :  محمود علي شاكر  1998', reply_markup=back_to_cities_menu)
	else:
		name_msg=bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=f'اخترت :  {str(city_keys[str(city)])}\nارسل الاسم الثلاثي من فضلك ✓ :', reply_markup=back_to_cities_menu)
	bot.register_next_step_handler(name_msg, search_name_handler, str(city))

def tamon_number_handler(message, city):
    city_keys={
	'mesan':'ميسان',
	'muthana':'مثنى',
	'najaf':'نجف',
	'nineveh':'نينوى',
	'diyala':'ديالى',
	'duhok':'دهوك',
	'erbil':'اربيل',
	'karbalaa':'كربلاء',
	'kirkuk':'كركوك',
	'qadisiya':'قادسية',
	'salahaldeen':'صلاح الدين',
	'sulaymaniyah':'سليمانية',
	'wasit':'واسط',
	'babylon':'بابل',
	'baghdad':'بغداد',
	'balad':'بلد',
	'basrah':'بصرة',
	'dhiqar':'ذي قار',
	'alanbar':'الانبار',
	'all':'بحث عام',
	'developer_button':'المطور',
	'channel_button':'القناة'
	}
    number_msg = bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=f'اخترت :  {str(city_keys[str(city)])}\nارسل رقم التموينيه من فضلك ✓ :', reply_markup=back_to_cities_menu)
    bot.register_next_step_handler(number_msg, search_tamon_number_handler, str(city))

def search_tamon_number_handler(message, city):
    number = message.text
    user_id = message.from_user.id
    if bot_channels() and not check_mandatory_subscription(message):
        return
    elif user_id in banned_from_bot:
        bot.send_message(user_id, "نجب لك انته ضاربيك نعال ⁴²")
        return
    bot.send_message(user_id, "الرجاء الانتضار...")
    search_info_by_tamon_number(message, number, city)




def search_name_handler(message, city):
	name = message.text
	user_id = message.from_user.id
	if bot_channels() and not check_mandatory_subscription(message):
		return
	elif user_id in banned_from_bot:
		bot.send_message(user_id, "نجب لك انته ضاربيك نعال ⁴²")
		return
	if city == "all":
		bot.reply_to(message, "الرجاء الانتضار...")
		search_all_by_name(message, name)
		return
	if any(char in name for char in sql_special_chars):
		bot.send_message(message.chat.id, 'انتضر عزيزي')
		return

	try:
		nameg = name.split(' ')[1]
		w_msg = bot.reply_to(message, "الرجاء الانتضار...")
		search_info_by_name(w_msg, name, city)
	except IndexError:
		bot.reply_to(message, "اسم غير صحيح", reply_markup=back_to_cities_menu)


def search_all_by_name(message, name):
	city_keys = {
		'mesan': 'ميسان',
		'muthana': 'مثنى',
		'najaf': 'نجف',
		'nineveh': 'نينوى',
		'diyala': 'ديالى',
		'duhok': 'دهوك',
		'erbil': 'اربيل',
		'karbalaa': 'كربلاء',
		'kirkuk': 'كركوك',
		'qadisiya': 'قادسية',
		'salahaldeen': 'صلاح الدين',
		'sulaymaniyah': 'سليمانية',
		'wasit': 'واسط',
		'babylon': 'بابل',
		'alanbar': 'الانبار',
		'balad': 'بلد',
		'basrah': 'بصرة',
		'dhiqar': 'ذي قار',
		'baghdad': 'بغداد',
		'developer_button':'المطور',
		'channel_button':'القناة'
	}
	user_id = message.from_user.id
	if bot_channels() and not check_mandatory_subscription(message):
		return
	elif user_id in banned_from_bot:
		bot.send_message(user_id, "نجب لك انته ضاربيك نعال ⁴²")
		return
	name_parts = name.split(' ')
	if len(name_parts) < 2 or len(name_parts) > 4:
		bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="تم ادخال معلومات غير كافية سوف يتم البحث عن الاحصائيات للاسم المدخل الرجاء الانتضار قليلا!.", reply_markup=back_to_cities_menu)
		count_matching_results(message, name)
		return

	fname = name_parts[0]
	sname = name_parts[1]
	lname = name_parts[2] if len(name_parts) > 2 else None
	birth_year = name_parts[3] if len(name_parts) == 4 else None

	def query_city(city, city_name):
		nonlocal count
		town_var = "rc_name" if city == "baghdad" else "ss_br_nm"
		street_var = "f_street" if city == "baghdad" else "ss_lg_no"
		work_var = "p_job" if city == "baghdad" else "p_work"

		try:
			connection = sqlite3.connect(f'db/{city}.db')
			connection.text_factory = str
			cursor = connection.cursor()

			if lname and birth_year:
				query = f"""
					SELECT fam_no, p_first, p_father, p_grand, p_birth, {town_var}, rc_no, seq_no, {street_var}, {work_var}
					FROM person
					WHERE p_first LIKE ? AND p_father LIKE ? AND p_grand LIKE ? AND p_birth LIKE ?
				"""
				params = (f'{fname}%', f'{sname}%', f'{lname}%', f'{birth_year}%')
			elif lname:
				query = f"""
					SELECT fam_no, p_first, p_father, p_grand, p_birth, {town_var}, rc_no, seq_no, {street_var}, {work_var}
					FROM person
					WHERE p_first LIKE ? AND p_father LIKE ? AND p_grand LIKE ?
				"""
				params = (f'{fname}%', f'{sname}%', f'{lname}%')
			elif birth_year:
				query = f"""
					SELECT fam_no, p_first, p_father, p_grand, p_birth, {town_var}, rc_no, seq_no, {street_var}, {work_var}
					FROM person
					WHERE p_first LIKE ? AND p_father LIKE ? AND p_birth LIKE ?
				"""
				params = (f'{fname}%', f'{sname}%', f'{birth_year}%')
			else:
				query = f"""
					SELECT fam_no, p_first, p_father, p_grand, p_birth, {town_var}, rc_no, seq_no, {street_var}, {work_var}
					FROM person
					WHERE p_first LIKE ? AND p_father LIKE ?
				"""
				params = (f'{fname}%', f'{sname}%')

			cursor.execute(query, params)
			rows = cursor.fetchall()
			return rows

		except sqlite3.OperationalError as e:
			if "unable to open database file" in str(e):
				print(f"Error: Unable to open database file for city: {city}")
			elif "no such table: person" in str(e):
				print(f"Error: No such table 'person' in database for city: {city}")
			else:
				print(f"OperationalError: {str(e)}")
			return []

		finally:
			if 'cursor' in locals():
				cursor.close()
			if 'connection' in locals():
				connection.close()

	results_found = False
	count = 0

	for city, city_name in city_keys.items():
		rows = query_city(city, city_name)
		if rows:
			results_found = True
			bot.delete_message(chat_id=message.chat.id, message_id=message.id)
			for row in rows:
				nbr, first, second, last, birth, town, locality, house, alley, work = row
				first = first.replace("\x84", "")
				second = second.replace("\x84", "")
				last = last.replace("\x84", "")
				birth = str(birth)[:4]
				current_year = datetime.now().year
				age = str(current_year - int(birth)) if birth.isdigit() else "None"

				mes = f"""
			   رقم التموينية : {nbr}
			   الاسم الاول : {first}
			   الاسم الثاني : {second}
			   الاسم الثالث : {last}
			   سنة الولادة : {birth}
			   العمر : {age}
			   الوضيفة : {work}
			  المحافظة : {city_name}
			  القضاء : {town}
			  المحلة : {locality}
			  الزقاق : {alley}
			   الدار : {house}
				"""
				count += 1
				bot.send_message(message.chat.id, mes, reply_markup=find_familly)
				if count >= 20:
					# Call another function named statsss
					bot.send_message(message.chat.id, 'لكثرة النتائج سوف يتم البحث عن احصائيات الاسم في جميع المحافظات لمنع الضغط على البوت و حساب المستخدم!')
					count_matching_results(message, name)
					return

	if results_found:
		bot.send_message(message.chat.id, "تم الانتهاء من البحث ✓", reply_markup=back_to_cities_menu)
	else:
		bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="لم يتم العثور على نتائج ✘", reply_markup=back_to_cities_menu)



def count_matching_results(message, name):
	city_keys = {
		'mesan': 'ميسان',
		'muthana': 'مثنى',
		'najaf': 'نجف',
		'nineveh': 'نينوى',
		'diyala': 'ديالى',
		'duhok': 'دهوك',
		'erbil': 'اربيل',
		'karbalaa': 'كربلاء',
		'kirkuk': 'كركوك',
		'qadisiya': 'قادسية',
		'salahaldeen': 'صلاح الدين',
		'sulaymaniyah': 'سليمانية',
		'wasit': 'واسط',
		'babylon': 'بابل',
		'alanbar': 'الانبار',
		'balad': 'بلد',
		'basrah': 'بصرة',
		'dhiqar': 'ذي قار',
		'baghdad': 'بغداد',
		'developer_button':'المطور',
		'channel_button':'القناة'
	}

	name_parts = name.split(' ')
	fname = name_parts[0]
	sname = name_parts[1] if len(name_parts) > 1 else '%'
	lname = name_parts[2] if len(name_parts) > 2 else '%'
	birth_year = name_parts[3] if len(name_parts) == 4 else '%'
	results_summary = []
	for city, city_name in city_keys.items():
		print(city)
		town_var = "rc_name" if city == "baghdad" else "ss_br_nm"
		street_var = "f_street" if city == "baghdad" else "ss_lg_no"
		work_var = "p_job" if city == "baghdad" else "p_work"

		try:
			connection = sqlite3.connect(f'db/{city}.db')
			connection.text_factory = str
			cursor = connection.cursor()

			if lname and birth_year:
				query = f"""
					SELECT COUNT(*)
					FROM person
					WHERE p_first LIKE ? AND p_father LIKE ? AND p_grand LIKE ? AND p_birth LIKE ?
				"""
				cursor.execute(query, (f'{fname}%', f'{sname}%', f'{lname}%', f'{birth_year}%'))
			elif lname:
				query = f"""
					SELECT COUNT(*)
					FROM person
					WHERE p_first LIKE ? AND p_father LIKE ? AND p_grand LIKE ?
				"""
				cursor.execute(query, (f'{fname}%', f'{sname}%', f'{lname}%'))
			elif birth_year:
				query = f"""
					SELECT COUNT(*)
					FROM person
					WHERE p_first LIKE ? AND p_father LIKE ? AND p_birth LIKE ?
				"""
				cursor.execute(query, (f'{fname}%', f'{sname}%', f'{birth_year}%'))
			else:
				query = f"""
					SELECT COUNT(*)
					FROM person
					WHERE p_first LIKE ? AND p_father LIKE ?
				"""
				cursor.execute(query, (f'{fname}%', f'{sname}%'))

			count = cursor.fetchone()[0]
			results_summary.append(f"{city_name}: {count} مواطن")

		except sqlite3.OperationalError as e:
			if "unable to open database file" in str(e):
				print(f"Error: Unable to open database file for city: {city}")
				results_summary.append(f"{city_name}: خطأ في فتح قاعدة البيانات")
			elif "no such table: person" in str(e):
				print(f"Error: No such table 'person' in database for city: {city}")
				results_summary.append(f"{city_name}: قاعدة البيانات لا تحتوي على الجدول المطلوب")
			else:
				print(f"OperationalError: {str(e)}")
				results_summary.append(f"{city_name}: خطأ في قاعدة البيانات")
		finally:
			if 'cursor' in locals():
				cursor.close()
			if 'connection' in locals():
				connection.close()

	result_message = "\n".join(results_summary)
	result_message += f"\nالاسم الذي بحثت عنه : {name}"
	bot.send_message(message.chat.id, f"عدد النتائج المطابقة لكل محافظة:\n\n{result_message}", reply_markup=back_to_cities_menu)



def search_info_by_name(message, name, city):
	city_keys={
	'mesan':'ميسان',
	'muthana':'مثنى',
	'najaf':'نجف',
	'nineveh':'نينوى',
	'diyala':'ديالى',
	'duhok':'دهوك',
	'erbil':'اربيل',
	'karbalaa':'كربلاء',
	'kirkuk':'كركوك',
	'qadisiya':'قادسية',
	'salahaldeen':'صلاح الدين',
	'sulaymaniyah':'سليمانية',
	'wasit':'واسط',
	'babylon':'بابل',
	'baghdad':'بغداد',
	'balad':'بلد',
	'basrah':'بصرة',
	'dhiqar':'ذي قار',
	'alanbar':'الانبار',
	'developer_button':'المطور',
	'channel_button':'القناة'
	}
	if city=="baghdad":
		town_var="rc_name"
		street_var="f_street"
		work_var="p_job"
	else:
		town_var="ss_br_nm"
		street_var="ss_lg_no"
		work_var="p_work"
	connection = sqlite3.connect(f'{str(city)}.db')
	connection.text_factory = str
	cursor = connection.cursor()
	fname=str(str(name).split(' ')[0])
	sname=str(str(name).split(' ')[1])
	try:
		lname=str(str(name).split(' ')[2])
		three=True
	except:
		three=False
	found=False
	deleted=False
	if three:
		query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth, {str(town_var)}, rc_no, seq_no, {str(street_var)}, {str(work_var)} FROM person WHERE p_first LIKE '{fname}%' AND p_father LIKE '{sname}%' AND p_grand LIKE '{lname}%'"
		cursor.execute(query)
		rows = cursor.fetchall()
		if rows:
			found=True
		for row in rows:
			nbr=str(list(row)[0])
			first=str(list(row)[1]).replace("\x84", "")
			second=str(list(row)[2]).replace("\x84", "")
			last=str(list(row)[3]).replace("\x84", "")
			birth=str(list(row)[4])[:4]
			town=str(list(row)[5])
			current_year = int(datetime.now().year)
			try:
				age=str(int(current_year)-int(birth))
			except:
				age="None"
			locality=str(list(row)[6])
			house=str(list(row)[7])
			alley=str(list(row)[8])
			work=str(list(row)[9])
			if not deleted:
				bot.delete_message(chat_id=message.chat.id, message_id=message.id)
				deleted=True
			mes=f"""\nرقم التموينية : {nbr}
 الاسم الاول : {first}
 الاسم الثاني : {second}
 الاسم الثالث : {last}
 سنة الولادة : {birth}
 العمر : {age}
 الوضيفة : {work}
 المحافظة : {str(city_keys[str(city)])}
 القضاء : {town}
 المحلة : {locality}
 الزقاق : {alley}
 الدار : {house}\n"""
			bot.send_message(message.chat.id, mes, reply_markup=find_familly)
	else:
		query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth, {str(town_var)}, rc_no, seq_no, {str(street_var)}, {str(work_var)} FROM person WHERE p_first LIKE '{fname}%' AND p_father LIKE '{sname}%'"
		cursor.execute(query)
		rows = cursor.fetchall()
		if rows:
			found=True
		for row in rows:
			nbr=str(list(row)[0])
			first=str(list(row)[1]).replace("\x84", "")
			second=str(list(row)[2]).replace("\x84", "")
			last=str(list(row)[3]).replace("\x84", "")
			birth=str(list(row)[4])[:4]
			town=str(list(row)[5])
			current_year = int(datetime.now().year)
			try:
				age=str(int(current_year)-int(birth))
			except:
				age="None"
			locality=str(list(row)[6])
			house=str(list(row)[7])
			alley=str(list(row)[8])
			work=str(list(row)[9])
			if not deleted:
				bot.delete_message(chat_id=message.chat.id, message_id=message.id)
				deleted=True
			mes=f"""\nرقم التموينية : {nbr}
 الاسم الاول : {first}
 الاسم الثاني : {second}
 الاسم الثالث : {last}
 سنة الولادة : {birth}
 العمر : {age}
 الوضيفة : {work}
 المحافظة : {str(city_keys[str(city)])}
 القضاء : {town}
 المحلة : {locality}
 الزقاق : {alley}
 الدار : {house}\n"""
			bot.send_message(message.chat.id, mes, reply_markup=find_familly)
	if found:
		bot.send_message(message.chat.id, "تم الانتهاء من البحث ✓", reply_markup=back_to_cities_menu)
	else:
		bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="لم يتم العثور على نتائج ✘", reply_markup=back_to_cities_menu)

def search_info_by_tamon_number(message, number, city):
	city_keys={
	'mesan':'ميسان',
	'muthana':'مثنى',
	'najaf':'نجف',
	'nineveh':'نينوى',
	'diyala':'ديالى',
	'duhok':'دهوك',
	'erbil':'اربيل',
	'karbalaa':'كربلاء',
	'kirkuk':'كركوك',
	'qadisiya':'قادسية',
	'salahaldeen':'صلاح الدين',
	'sulaymaniyah':'سليمانية',
	'wasit':'واسط',
	'babylon':'بابل',
	'baghdad':'بغداد',
	'balad':'بلد',
	'basrah':'بصرة',
	'dhiqar':'ذي قار',
	'alanbar':'الانبار',
	'developer_button':'المطور',
	'channel_button':'القناة'
	}
	if city=="baghdad":
		town_var="rc_name"
		street_var="f_street"
		work_var="p_job"
	else:
		town_var="ss_br_nm"
		street_var="ss_lg_no"
		work_var="p_work"
	connection = sqlite3.connect(f'{str(city)}.db')
	connection.text_factory = str
	cursor = connection.cursor()
	found=False
	deleted=False
	if number.isdigit():
		query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth, {str(town_var)}, rc_no, seq_no, {str(street_var)}, {str(work_var)} FROM person WHERE fam_no LIKE '{number}%' ORDER BY p_birth ASC LIMIT 1"
		cursor.execute(query)
		rows = cursor.fetchall()
		if rows:
			found=True
		for row in rows:
			nbr=str(list(row)[0])
			first=str(list(row)[1]).replace("\x84", "")
			second=str(list(row)[2]).replace("\x84", "")
			last=str(list(row)[3]).replace("\x84", "")
			birth=str(list(row)[4])[:4]
			town=str(list(row)[5])
			current_year = int(datetime.now().year)
			try:
				age=str(int(current_year)-int(birth))
			except:
				age="None"
			locality=str(list(row)[6])
			house=str(list(row)[7])
			alley=str(list(row)[8])
			work=str(list(row)[9])
			if not deleted:
				bot.delete_message(chat_id=message.chat.id, message_id=message.id)
				deleted=True
			mes=f"""\nرقم التموينية : {nbr}
 الاسم الاول : {first}
 الاسم الثاني : {second}
 الاسم الثالث : {last}
 سنة الولادة : {birth}
 العمر : {age}
 الوضيفة : {work}
 المحافظة : {str(city_keys[str(city)])}
 القضاء : {town}
 المحلة : {locality}
 الزقاق : {alley}
 الدار : {house}\n"""
			bot.send_message(message.chat.id, mes, reply_markup=find_familly)
	else:
		bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="يجب ان يكون رقم التموينيه عبارة عن ارقام", reply_markup=back_to_cities_menu)
	if found:
		bot.send_message(message.chat.id, "تم الانتهاء من البحث ✓", reply_markup=back_to_cities_menu)
	else:
		bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="لم يتم العثور على نتائج ✘", reply_markup=back_to_cities_menu)



def find_familly_function(message):
	mess=""
	city_keys={
	'mesan':'ميسان',
	'muthana':'مثنى',
	'najaf':'نجف',
	'nineveh':'نينوى',
	'diyala':'ديالى',
	'duhok':'دهوك',
	'erbil':'اربيل',
	'karbalaa':'كربلاء',
	'kirkuk':'كركوك',
	'qadisiya':'قادسية',
	'salahaldeen':'صلاح الدين',
	'sulaymaniyah':'سليمانية',
	'wasit':'واسط',
	'babylon':'بابل',
	'baghdad':'بغداد',
	'balad':'بلد',
	'basrah':'بصرة',
	'dhiqar':'ذي قار',
	'alanbar':'الانبار',
	'developer_button':'المطور',
	'channel_button':'القناة'
	}
	inv_city_keys={v: k for k, v in city_keys.items()}
	fam_num=str(message.text.split('رقم التموينية : ')[1].split('\n')[0])
	ar_city=str(message.text.split('المحافظة : ')[1].split('\n')[0])
	city=str(inv_city_keys[str(ar_city)])
	if city=="baghdad":
		town_var="rc_name"
	else:
		town_var="ss_br_nm"
	connection = sqlite3.connect(f'{str(city)}.db')
	connection.text_factory = str
	cursor = connection.cursor()
	bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="الرجاء الانتضار...", reply_markup=back_to_cities_menu)
	query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth, {str(town_var)} FROM person WHERE fam_no LIKE '{fam_num}%'"
	cursor.execute(query)
	rows = cursor.fetchall()
	for row in rows:
		nbr=str(list(row)[0])
		first=str(list(row)[1]).replace("\x84", "")
		second=str(list(row)[2]).replace("\x84", "")
		last=str(list(row)[3]).replace("\x84", "")
		birth=str(list(row)[4])[:4]
		town=str(list(row)[5])
		current_year = int(datetime.now().year)
		try:
			age=str(int(current_year)-int(birth))
		except:
			age="None"
		mess+=f"""\nرقم التموينية : {nbr}\nالاسم الاول : {first}\nالاسم الثاني : {second}\nالاسم الثالث : {last}\nسنة الولادة : {birth}\nالعمر : {age}\nالقضاء : {town}\nالمحافظة : {str(city_keys[str(city)])}\n"""
		bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=mess, reply_markup=back_to_cities_menu)
	mess+="\nتم الانتهاء من البحث ✓"
	bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=mess, reply_markup=back_to_cities_menu)









def back_to_cities_menu_function(message):
	bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text='''>  **✦ اهــلًا بـك فـي بـوت داتا بيس العراق 🇮🇶**\n
>||**🔎 يمكنك معرفة جميع العوائل العراقية**||\n
> **📝 وذلك عبر البحث بالاسم الثلاثي**\n
> **📌 اختر المدينة للمتابعة:**\n
> **ارسل /help و اتبع التعليمات ♦️**\n 
    ''', reply_markup=all_city,parse_mode='MarkdownV2')


def add_user_function(message):
	msg1=bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="ارسل ايدي المستخدم لرفعه", reply_markup=back_to_show_oo_menu)
	bot.register_next_step_handler(msg1, add_user_id_handler)

def add_user_id_handler(message):
    try:
        new_admin = message.text
        if new_admin.startswith('@'):
            new_admin_id = bot.get_chat(new_admin).id
        else:
            new_admin_id = int(new_admin)

        user_info = bot.get_chat(new_admin_id)

        if new_admin_id not in admin_ids:
            admin_ids.append(new_admin_id)
            bot.send_message(
                message.chat.id, 
                f"عـزيـزي : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                f"المستخدم :  [{user_info.first_name}](tg://user?id={new_admin_id})\nتم رفعه الى ادمن في البوت",
                parse_mode='Markdown'
            )
        else:
            bot.send_message(message.chat.id, "الـحلـو ادمـن بـل فـعل ")
    except (ValueError, telebot.apihelper.ApiException):
        bot.send_message(message.chat.id, "هـنالـك خطـأ ")



def show_administrative_in_bot(call,user_id):
    if admin_ids:
        administrative_in_bot_list = "\n".join(
            [f"{i+1}- [{bot.get_chat(admin).first_name}](tg://user?id={admin})" for i, admin in enumerate(admin_ids)]
        )
        bot.edit_message_text(chat_id=call.message.chat.id, 
message_id=call.message.message_id,
text=f"الادمنيه في البوت\n— — — — — — — — — — — — — —\n{administrative_in_bot_list}"
,parse_mode='Markdown',reply_markup=back_to_show_oo_menu)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, 
message_id=call.message.message_id,
text="ماكو ادمنيه في البوت"
,parse_mode='Markdown',reply_markup=back_to_show_oo_menu)


def delete_user_function(message):
	msg2=bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="ارسل ايدي الادمـن لازالـته", reply_markup=back_to_show_oo_menu, parse_mode="markdown")
	bot.register_next_step_handler(msg2, delete_user_id_handler)

def delete_user_id_handler(message):
    try:
        admin_to_remove = message.text
        if admin_to_remove.startswith('@'):
            admin_id_to_remove = bot.get_chat(admin_to_remove).id
        else:
            admin_id_to_remove = int(admin_to_remove)

        user_info = bot.get_chat(admin_id_to_remove)

        if admin_id_to_remove in admin_ids:
            admin_ids.remove(admin_id_to_remove)
            bot.send_message(
                message.chat.id, 
                f"عزيزي : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                f"المستخدم : [{user_info.first_name}](tg://user?id={admin_id_to_remove})\nتم تنزيله من قائمه الادمنيه",
                parse_mode='Markdown'
            )
        else:
            bot.send_message(message.chat.id, "المستخدم ليس ادمن في البوت")
    except (ValueError, telebot.apihelper.ApiException):
        bot.send_message(message.chat.id, "حدث خطأ ")

def add_user_function_users(call):
	msg1=bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="حسنا الان ارسل ايدي الشخص لاضافته", reply_markup=back_to_show_oo_menu)
	bot.register_next_step_handler(msg1, add_user_id_handler_u)


def add_user_id_handler_u(message):
	msg=bot.reply_to(message, "الرجاء الانتضار...")
	user_id=message.text
	lst=[]
	f=open('users.txt', 'r').read().splitlines()
	already=False
	for idd in f:
		if str(idd)==str(user_id):
			already=True
	if already==True:
		bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=f"موجود من قبل ❌", reply_markup=back_to_admin_menu)
	else:
		f=open('users.txt', 'a')
		f.write(user_id+'\n')
		f.close()
		bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=f"تم اضافة {user_id} ✅", reply_markup=back_to_admin_menu)



def delete_user_function_users(call):
    ids_msg = "جميع ايديات المشتركين:\n—————————————\n"
    valid_ids = set()
    unique_ids = []
    counter = 1
    with open('users.txt', 'r') as file:
        lines = file.read().splitlines()
    for line in lines:
        line = line.strip()
        if line.isdigit() and line not in valid_ids:
            try:
                user = bot.get_chat(chat_id=int(line))
                username = user.username if user.username else "لا يوجد"
                valid_ids.add(line)
                unique_ids.append(line)
                ids_msg += f"{counter} ~ {line} ~ @{username}\n" if user.username else f"{counter} ~ {line} ~ {username}\n"
                counter += 1
            except BadRequest:
                continue
    with open('users.txt', 'w') as file:
        file.write('\n'.join(unique_ids))
    msg2=bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f"{ids_msg}\n\nحسنا الان ارسل ايدي الشخص لحذفه", reply_markup=back_to_show_oo_menu)
    bot.register_next_step_handler(msg2, delete_user_id_handler_u)


def split_message2(text, max_length=2000):
    parts = []
    while len(text) > max_length:
        split_index = text[:max_length].rfind('\n')
        if split_index == -1:
            split_index = max_length
        parts.append(text[:split_index])
        text = text[split_index:].lstrip()
    parts.append(text)
    return parts

def show_users_users(call):
    ids_msg = "جميع ايديات المشتركين:\n—————————————\n"
    valid_ids = set()
    unique_ids = []
    counter = 1
    with open('users.txt', 'r') as file:
        lines = file.read().splitlines()

    for line in lines:
        line = line.strip()
        if line.isdigit() and line not in valid_ids:
            try:
                user = bot.get_chat(chat_id=int(line))
                username = user.username if user.username else "لا يوجد"
                valid_ids.add(line)
                unique_ids.append(line)
                ids_msg += f"{counter} ~ {line} ~ @{username}\n" if user.username else f"{counter} ~ {line} ~ {username}\n"
                counter += 1
            except BadRequest:
                continue

    with open('users.txt', 'w') as file:
        file.write('\n'.join(unique_ids))
    messages = split_message2(ids_msg)
    for i, msg in enumerate(messages):
        if i == 0:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=msg,
                reply_markup=back_to_show_oo_menu
            )
        else:
            bot.send_message(
                chat_id=call.message.chat.id,
                text=msg,
                reply_markup=back_to_show_oo_menu
            )

def delete_user_id_handler_u(message):
	msg=bot.reply_to(message, "الرجاء الانتضار...")
	user_id=message.text
	lst=[]
	f=open('users.txt', 'r').read().splitlines()
	found=False
	for idd in f:
		if str(idd)==str(user_id):
			found=True
		else:
			lst.append(idd)
	if found==True:
		ff=open('users.txt', 'w')
		for i in lst:
			ff.write(i+'\n')
		ff.close()
		bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=f"تم حذف {user_id} ✅", reply_markup=back_to_show_oo_menu)
	else:
		bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=f"غير موجود ❌", reply_markup=back_to_show_oo_menu)


def qna(message):
    channel_id = extract_channel_id(message.text)
    if channel_id:
        try:
            if channel_id.startswith('@'):
                try:
                    chat_info = bot.get_chat(channel_id)
                    channel_id = str(chat_info.id)
                except telebot.apihelper.ApiException:
                    return bot.send_message(message.chat.id, " لم يتم العثور على القناة، تأكد من المعرف.")
            with open(CH_FILE, "r") as file:
                existing_channels = [line.strip() for line in file.readlines()]

            if channel_id in existing_channels:
                bot.send_message(
                    message.chat.id, 
                    f"عـزيزي : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                    f"القـناة ← {channel_id}\n"
                    "مـوجودة بالفعل في ملف الاشتراك ⭐.",
                    parse_mode='Markdown', 
                    reply_to_message_id=message.message_id
                )
                return
            member_status = bot.get_chat_member(channel_id, bot.get_me().id).status
            if member_status in ['administrator', 'creator']:
                with open(CH_FILE, "a") as file:
                    file.write(f"{channel_id}\n")
                bot.send_message(
                    message.chat.id, 
                    f"عـزيزي : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                    f"تمت إضافة القناة ← {channel_id} إلى الاشتراك الإجباري ✅",
                    parse_mode='Markdown', 
                    reply_to_message_id=message.message_id
                )
            else:
                bot.send_message(
                    message.chat.id, 
                    " البوت ليس أدمن في القناة، لا يمكن إضافتها.",
                    reply_to_message_id=message.message_id
                )
        except telebot.apihelper.ApiException as e:
            if 'chat not found' in str(e):
                bot.send_message(message.chat.id, " لم يتم العثور على القناة.", reply_to_message_id=message.message_id)
            else:
                bot.send_message(message.chat.id, " حدث خطأ أثناء إضافة القناة.", reply_to_message_id=message.message_id)
    else:
        bot.send_message(message.chat.id, " أدخل معرف أو آيدي قناة صالح.", reply_to_message_id=message.message_id)

def delqna(message):
    text = message.text.strip()
    if text.startswith('@'):
        try:
            chat = bot.get_chat(text)
            channel_id = str(chat.id)
        except telebot.apihelper.ApiException:
            bot.send_message(message.chat.id, " المعرف غير صالح أو القناة غير موجودة", reply_to_message_id=message.message_id)
            return
    elif text.startswith('-100'):
        channel_id = text
    else:
        bot.send_message(message.chat.id, " ادخل معرف (@) أو ايدي صحيح (-100...)", reply_to_message_id=message.message_id)
        return
    try:
        with open(CH_FILE, "r") as file:
            channels = file.read().splitlines()
        
        if channel_id in channels:
            channels.remove(channel_id)
            with open(CH_FILE, "w") as file:
                file.write("\n".join(channels) + "\n")
            bot.send_message(
                message.chat.id, 
                f"عـزيـزي : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                f"القـناه {channel_id}\n↯︙تم ازالتـها مـن الاشتراك الاجباري",
                parse_mode='Markdown',
                reply_to_message_id=message.message_id
            )
        else:
            bot.send_message(message.chat.id, " الـقناة مامـوجوده بل اشتراك الاجـباري", reply_to_message_id=message.message_id)
    except FileNotFoundError:
        bot.send_message(message.chat.id, " لا توجد قنوات مسجله حاليًا", reply_to_message_id=message.message_id)
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ حدث خطأ: {e}", reply_to_message_id=message.message_id)
bot.infinity_polling()
