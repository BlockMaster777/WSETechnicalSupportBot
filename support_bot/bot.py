# coding=utf-8
"""
WSETechnicalSupportBot
Copyright (C) 2025  BlockMaster

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import *
from db_manager import DBManager

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def gen_faq_list_markup():
    markup = InlineKeyboardMarkup()
    faq_questions = manager.get_faq_questions()
    for question in faq_questions:
        markup.add(InlineKeyboardButton(question[1], callback_data="fq" + str(question[0])))
    return markup


def gen_options_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Часто задаваемые вопросы", callback_data="fl"))
    markup.add(InlineKeyboardButton("Задать вопрос", callback_data="q"))
    return markup


def gen_back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Обратно в меню", callback_data="m"))
    markup.add(InlineKeyboardButton("Обратно в часто задаваемые вопросы", callback_data="fl"))
    return markup


def gen_theme_options():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Проблема с работой сайта / приложения", callback_data="td"))
    markup.add(InlineKeyboardButton("Проблема с товаром / доставкой", callback_data="tp"))
    return markup


def gen_cancel_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Отмена", callback_data="c"))
    return markup


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id,
                     "Здравствуйте. Это бот технической поддержки интернет магазина 'Мы продаём всё на свете'\n\n"
                     "Выберите опцию:", reply_markup=gen_options_markup())


@bot.callback_query_handler(func=lambda call: call.data == "m")
def start(call):
    bot.edit_message_text("Здравствуйте. Это бот технической поддержки интернет магазина 'Мы продаём всё на свете'\n\n"
                          "Выберите опцию:", call.message.chat.id, call.message.message_id,
                          reply_markup=gen_options_markup())


@bot.callback_query_handler(func=lambda call: call.data == "fl")
def faq_list(call):
    bot.edit_message_text("Выберите интересующий вопрос", call.message.chat.id, call.message.message_id,
                          reply_markup=gen_faq_list_markup())


@bot.callback_query_handler(func=lambda call: call.data.startswith("fq"))
def faq_answer(call):
    answer = manager.get_faq_answer(call.data[2:])
    bot.edit_message_text(answer, call.message.chat.id, call.message.message_id, reply_markup=gen_back_button())


@bot.callback_query_handler(func=lambda call: call.data.startswith("q"))
def ask_theme(call):
    bot.edit_message_text("Выберите тему обращения", call.message.chat.id, call.message.message_id,
                          reply_markup=gen_theme_options())


@bot.callback_query_handler(func=lambda call: call.data.startswith("t"))
def ask_question_text(call):
    theme = "dev" if call.data[1] == "d" else "product"
    bot.edit_message_text("Отправьте текст обращения. Пожалуйста укажите все детали, которые могут понадобиться. "
                          "Вы не сможете изменить или удалить обращение.", call.message.chat.id,
                          call.message.message_id)
    bot.register_next_step_handler(call.message, send_question, theme)


def send_question(message, theme):
    try:
        manager.add_question(message.text, theme)
        bot.reply_to(message, "Обращение было отправлено! Ожидайте ответа отт менеджера.")
    except Exception as e:
        bot.send_message(message.chat.id,
                         "Произошла ошибка. Обращение на было отправлено. Техническая информация: " + repr(e))


@bot.callback_query_handler(func=lambda call: call.data.startswith("c"))
def cancel(call):
    bot.clear_step_handler_by_chat_id(call.message.chat_id)
    bot.edit_message_text("Выполнена отмена", call.message.chat.id, call.message.message_id)


if __name__ == "__main__":
    manager = DBManager(DATABASE_PATH)
    bot.infinity_polling()
