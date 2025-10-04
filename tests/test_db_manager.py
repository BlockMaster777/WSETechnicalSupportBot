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
import sqlite3

import pytest

import support_bot.db_manager


@pytest.fixture
def temp_db():
    db_path = "./test_database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS questions")
    cursor.execute("DROP TABLE IF EXISTS faq")
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      question TEXT NOT NULL,
                      theme TEXT NOT NULL);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS faq (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      question TEXT NOT NULL,
                      answer TEXT NOT NULL);""")
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def temp_conn(temp_db):
    conn = sqlite3.connect(temp_db)
    with conn:
        return conn


@pytest.fixture
def temp_manager(temp_db):
    manager = support_bot.db_manager.DBManager(temp_db)
    return manager


def test_get_faq_questions(temp_conn, temp_manager):
    c = temp_conn.cursor()
    c.execute("INSERT INTO faq (question, answer) VALUES (?, ?)", ("testq1", "testa1"))
    c.execute("INSERT INTO faq (question, answer) VALUES (?, ?)", ("testq2", "testa2"))
    temp_conn.commit()
    assert temp_manager.get_faq_questions() == [(1, "testq1"), (2, "testq2")]


def test_get_faq_answer(temp_conn, temp_manager):
    c = temp_conn.cursor()
    c.execute("INSERT INTO faq (question, answer) VALUES (?, ?)", ("testq1", "testa1"))
    temp_conn.commit()
    assert temp_manager.get_faq_answer(1) == "testa1"


def test_add_question(temp_conn, temp_manager):
    c = temp_conn.cursor()
    temp_manager.add_question("testq1", "dev")
    assert c.execute("SELECT question, theme FROM questions").fetchall() == [("testq1", "dev")]


def test_remove_question(temp_conn, temp_manager):
    c = temp_conn.cursor()
    c.execute("INSERT INTO questions (question, theme) VALUES (?, ?)", ("testq1", "dev"))
    temp_conn.commit()
    temp_manager.remove_question(1)
    assert c.execute("SELECT * FROM questions").fetchall() == []


def test_get_dev_questions(temp_conn, temp_manager):
    c = temp_conn.cursor()
    c.execute("INSERT INTO questions (question, theme) VALUES (?, ?)", ("testq1", "dev"))
    c.execute("INSERT INTO questions (question, theme) VALUES (?, ?)", ("testq2", "product"))
    temp_conn.commit()
    assert temp_manager.get_dev_questions() == [(1, "testq1")]


def test_get_product_questions(temp_conn, temp_manager):
    c = temp_conn.cursor()
    c.execute("INSERT INTO questions (question, theme) VALUES (?, ?)", ("testq1", "dev"))
    c.execute("INSERT INTO questions (question, theme) VALUES (?, ?)", ("testq2", "product"))
    temp_conn.commit()
    assert temp_manager.get_product_questions() == [(2, "testq2")]
