#coding=utf-8
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
import sqlite3
from config import *


class DBManager:
    def __init__(self):
        self.database = DATABASE_PATH
        self.__create_table()

    def __execute_sql(self, sql, *data: tuple):
        with sqlite3.connect(self.database) as conn:
            c = conn.cursor()
            c.execute(sql, data)
            conn.commit()

    def __create_table(self):
        self.__execute_sql("""CREATE TABLE IF NOT EXISTS questions (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              question TEXT NOT NULL,
                              theme TEXT NOT NULL,);""")
        self.__execute_sql("""CREATE TABLE IF NOT EXISTS faq (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              question TEXT NOT NULL,
                              answer TEXT NOT NULL,);""")

    def get_faq_list(self):
        self.__execute_sql("""SELECT id, question FROM faq""")

    def get_faq_answer(self, faq_id):
        self.__execute_sql("SELECT answer FROM faq WHERE id = ?", (faq_id,))

    def add_question(self, question, theme):
        self.__execute_sql("INSERT INTO questions (question, theme) VALUES (?, ?)", (question, theme))

    def remove_question(self, question_id):
        self.__execute_sql("DELETE FROM questions WHERE id = ?", (question_id,))

    def get_dev_questions(self):
        self.__execute_sql("SELECT * FROM questions")

    def get_product_questions(self):
        self.__execute_sql("SELECT * FROM questions")


if __name__ == "__main__":
    db = DBManager()