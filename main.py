import os
import telebot
import openai
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Chatbota bağlanmak için /chatgpt")

@bot.message_handler(commands=['chatgpt'])
def send_recursion_poem(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Karmaşık programlama kavramlarını yaratıcı bir yetenekle açıklama konusunda yetenekli, şiirsel bir asistansınız."},
                {"role": "user", "content": "Programlamada özyineleme kavramını açıklayan bir şiir yazın."}
            ]
        )
        poem = response.choices[0].message['content']
        bot.reply_to(message, poem)
    except openai.error.RateLimitError:
        bot.reply_to(message, "Kota sınırı aşıldı. Lütfen daha sonra tekrar deneyiniz.")
    except openai.error.APIError as e:
        bot.reply_to(message, f"APIde bir hata oluştu: {str(e)}")
    except Exception as e:
        bot.reply_to(message, f"Beklenmedik bir hata oluştu: {str(e)}")

bot.infinity_polling()
