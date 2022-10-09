import telebot

from config import API_TOKEN
from db import Session
from utils import get_or_create_user, add_debt, get_message

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        bot.reply_to(message, f"Попробуй еще раз")
        return

    with Session.begin() as session:
        username = message.from_user.username
        user = get_or_create_user(session=session, username=username)
        if first_name := message.from_user.first_name:
            user.first_name = first_name

        add_debt(session=session, amount=amount, user=user)
        debt_sum = user.debt_sum

        session.commit()

    bot.reply_to(message, f"{first_name or username}, {get_message(debt_sum)}")


if __name__ == "__main__":
    bot.infinity_polling()
