# © @Mr_Dark_Prince 🌚
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputTextMessageContent, InlineQueryResultArticle
from gpytranslate import Translator
import sqlite3, string

# ⚠️ Fill api_id and api_hash from my.telegram.org.. Also fill your bot_token from @botfather

bot = Client(
    "APP_NAME",
    api_id= 5735555,
    api_hash="1bb48af34173b1a1fb2dd0a21e8922aa",
    bot_token= 1962002332:AAG3epfiOA874_eDD1ehRlokriDrWV3jKCI
)

db = sqlite3.connect("userlanguages.db")
dbc = db.cursor()
dbc.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY,
                                                 chat_lang)""")
db.commit()

default_language = "en"

#Get User IDs and save it in DB
def chat_exists(chat_id, chat_type):
    if chat_type == "private":
        dbc.execute("SELECT user_id FROM users where user_id = ?", (chat_id,))
        return bool(dbc.fetchone())
    raise TypeError("Unknown chat type '%s'." % chat_type)

    
def get_db_lang(chat_id: int, chat_type: str) -> str:
    if chat_type == "private":
        dbc.execute("SELECT chat_lang FROM users WHERE user_id = ?", (chat_id,))
        ul = dbc.fetchone()
    return ul[0] if ul else None
    
def add_chat(chat_id, chat_type):
    if chat_type == "private":
        dbc.execute("INSERT INTO users (user_id) values (?)", (chat_id,))
        db.commit()
        
        
def set_db_lang(chat_id: int, chat_type: str, lang_code: str):
    if chat_type == "private":
        dbc.execute("UPDATE users SET chat_lang = ? WHERE user_id = ?", (lang_code, chat_id))
        db.commit()


@bot.on_message(filters.private, group=-1)
async def check_chat(bot, msg):
    chat_id = msg.chat.id
    chat_type = msg.chat.type

    if not chat_exists(chat_id, chat_type):
        add_chat(chat_id, chat_type)
        set_db_lang(chat_id, chat_type, "en")
        
@bot.on_callback_query(filters.regex(r"^back"))
async def backtostart(bot, query: CallbackQuery):
 await query.message.edit(f"Hello {query.from_user.mention}\n \U0001F60E I am GpyTranslatorRoBot \ud83e\udd16 \n\nSend any text which you would like to translate.\n\n**Available commands:**\n⊙ /help - Show this help message\n⊙ /language - Set your main language\n⊙ /tr (language code) as reply to a message in groups\n💡Example: /tr en: translates something to english",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add me to a Group ➕",  url="http://t.me/GpyTranslatorRoBot?startgroup=tr")
                ],
                [
                    InlineKeyboardButton("🔥 Help",  callback_data="help"),
                    InlineKeyboardButton("💚 Credits",  callback_data=b"Credits")
                ],
                [
                    InlineKeyboardButton("⚠️ Source",  url="https://github.com/Mr-Dark-Prince/GpyTranslatorRoBot"),
                    InlineKeyboardButton("⛱️ Owner",  url="https://t.me/mr_dark_prince"),
                ]
            ]
        )
    )
    
##Buttons
@bot.on_message(filters.command("start") & filters.private)
async def welcomemsg(bot, msg):
    await msg.reply(f"Hello {msg.from_user.mention}\n \U0001F60E I am GpyTranslatorRoBot \ud83e\udd16 \n\nSend any text which you would like to translate.\n\n**Available commands:**\n⊙ /help - Show this help message\n⊙ /language - Set your main language\n⊙ /tr (language code) as reply to a message in groups\n💡Example: /tr en: translates something to english",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add me to a Group ➕",  url="http://t.me/GpyTranslatorRoBot?startgroup=tr")
                ],
                [
                    InlineKeyboardButton("🔥 Help",  callback_data="help"),
                    InlineKeyboardButton("💚 Credits",  callback_data=b"Credits")
                ],
                [
                    InlineKeyboardButton("⚠️ Source",  url="https://github.com/Mr-Dark-Prince/GpyTranslatorRoBot"),
                    InlineKeyboardButton("⛱️ Owner",  url="https://t.me/mr_dark_prince"),
                ]
            ]
        )
    )
#Setup Help Message with buttons    
@bot.on_callback_query(filters.regex(r"^help"))
async def helpbutton(bot: Client, query: CallbackQuery):
    await query.message.edit("**GpyTranslateRoBot**\n\nGpyTranslate is a word 'G+Py+Translate' which means 'Google Python Translate'. A bot to help you translate text (with emojis) to few Languages from any other language in world.\n\nGpyTranslatorRoBot is able to detect a wide variety of languages because he is a grand son of Google Translate API.\n\nYou can use GpyTranslatorRoBot in his private chat & Groups.\n\n**How To Use**\nJust send copied text or forward message with other language to GpyTranslator Bot and you'll receive a translation of the message in the language of your choice. Send /language command to know which language is available.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("⬅️ Go Back ⬅️", callback_data="back")],
            ]
        )
    )

#Popup Credits    
@bot.on_callback_query(filters.regex(r"^Credits"))
async def credits(bot: Client, query: CallbackQuery):
    await query.answer("Developers 🧑‍💻\n\n • @Mr_Dark_Prince\n • @MrCentimetre\n • @itayki\n\nInspiration 👨🏻‍🏫\n\n • @DavideGalilei", show_alert=True)
    
# user sent /help command, configure the message that the bot should send   
@bot.on_message(filters.private & filters.command("help"))
async def help(bot, msg):
    await msg.reply_text(f"**GpyTranslateRoBot**\n\nGpyTranslate is a word 'G+Py+Translate' which means 'Google Python Translate'. A bot to help you translate text (with emojis) to few Languages from any other language in world.\n\nGpyTranslatorRoBot is able to detect a wide variety of languages because he is a grand son of Google Translate API.\n\nYou can use GpyTranslatorRoBot in his private chat & Groups.\n\n**How To Use**\nJust send copied text or forward message with other language to GpyTranslator Bot and you'll receive a translation of the message in the language of your choice. Send /language command to know which language is available.")

##When the user sent /language command, configure the message that the bot should send
@bot.on_message(filters.private & filters.command("language"))
async def language(bot, msg):
    await msg.reply_text(f"**Languages**\n\n__Select the language you want to translate.__\n\n•/lang (language code) \n\nExample: ```/lang en``` \n\nList of language codes: https://cloud.google.com/translate/docs/languages   \n\n Send the relevant command. \ud83e\udd20")



@bot.on_message(filters.command("lang") & filters.private)
async def setmylang(bot, msg):
 thelang = msg.command[1]
 await msg.reply(f"{thelang} has been set as your main language👍.")
 set_db_lang(msg.chat.id, msg.chat.type, thelang)



##main translation process
@bot.on_message(filters.private & ~filters.command("tr"))
async def main(bot, msg):
    tr = Translator()
    userlang = get_db_lang(msg.chat.id, msg.chat.type)
    translation = await tr(msg.text, targetlang=[userlang, 'utf-16'])
    language = await tr.detect(msg.text)
    await msg.reply(f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language}")
    
@bot.on_message(filters.command("tr") & filters.group)
async def translategroup(bot, msg) -> None:
    tr = Translator()
    if not msg.reply_to_message:
        await msg.reply("Reply to a message to translate")
        return
    if msg.reply_to_message.caption:
        to_translate = msg.reply_to_message.caption
    elif msg.reply_to_message.text:
        to_translate = msg.reply_to_message.text
    try:
        args = msg.text.split()[1].lower()
        if "//" in args:
            language = args.split("//")[0]
            tolanguage = args.split("//")[1]
        else:
            language = await tr.detect(to_translate)
            tolanguage = args
    except IndexError:
        language = await tr.detect(to_translate)
        tolanguage = "en"
    translation = await tr(to_translate,
                              sourcelang=language, targetlang=tolanguage)
    trmsgtext = f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language} \n\n **Translated to**: {tolanguage}" 
    await msg.reply(trmsgtext, parse_mode="markdown")

@bot.on_message(filters.command("tr") & filters.private)
async def translateprivatetwo(bot, msg) -> None:
    tr = Translator()
    to_translate = msg.text.split(None, 2)[2]
    language = await tr.detect(msg.text.split(None, 2)[2])
    tolanguage = msg.command[1]
    translation = await tr(to_translate,
                              sourcelang=language, targetlang=tolanguage)
    trmsgtext = f"**\ud83c\udf10 Translation**:\n\n```{translation.text}```\n\n**🔍 Detected language:** {language} \n\n **Translated to**: {tolanguage}" 
    await msg.reply(trmsgtext, parse_mode="markdown")

#Inline Bot
@bot.on_inline_query()
async def translateinline(bot, query) -> None:
 try:
    tr = Translator()
    to_translate = query.query.lower().split(None, 1)[1]
    language = await tr.detect(query.query.lower().split(None, 1)[1])
    tolanguage = query.query.lower().split()[0]
    translation = await tr(to_translate,
                              sourcelang=language, targetlang=tolanguage)
    trmsgtext =f"{translation.text}" 
    await query.answer([InlineQueryResultArticle(
       title= f"Translate from {language} to {tolanguage}",description=f"{translation.text}",input_message_content=InputTextMessageContent(trmsgtext)
    )])
 except IndexError:
  return
    
bot.run()
