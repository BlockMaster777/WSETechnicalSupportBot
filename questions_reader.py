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
import tkinter as tk
from tkinter import messagebox
from support_bot.db_manager import DBManager
from support_bot.config import DATABASE_PATH

class QuestionsApp:
    def __init__(self, root):
        self.db_manager = DBManager(DATABASE_PATH)
        self.root = root
        self.root.title("Questions Reader")
        self.root.resizable(False, False)

        dev_label = tk.Label(root, text="Dev")
        dev_label.pack(padx=5, pady=10)
        self.dev_questions_listbox = tk.Listbox(root, width=200, height=15)
        self.dev_questions_listbox.pack(pady=0)
        prod_label = tk.Label(root, text="Product")
        prod_label.pack(padx=5, pady=20)
        self.prod_questions_listbox = tk.Listbox(root, width=200, height=15)
        self.prod_questions_listbox.pack(pady=0)

        self.delete_button = tk.Button(root, text="Delete Question", command=self.delete_question)
        self.delete_button.pack(pady=10)

        self.load_questions()


    def load_questions(self):
        self.dev_questions_listbox.delete(0, tk.END)
        self.prod_questions_listbox.delete(0, tk.END)
        dev_questions = self.db_manager.get_dev_questions()
        for question in dev_questions:
            self.dev_questions_listbox.insert(tk.END, f"{question[0]}: {question[1]}")
        prod_questions = self.db_manager.get_product_questions()
        for question in prod_questions:
            self.prod_questions_listbox.insert(tk.END, f"{question[0]}: {question[1]}")

    def delete_question(self):
        dev_selected = self.dev_questions_listbox.curselection()
        prod_selected = self.prod_questions_listbox.curselection()
        if dev_selected:
            selected = dev_selected
            question_id = int(self.dev_questions_listbox.get(selected[0]).split(":")[0])
        elif prod_selected:
            selected = prod_selected
            question_id = int(self.prod_questions_listbox.get(selected[0]).split(":")[0])
        else:
            messagebox.showwarning("Warning", "No question selected")
            return

        self.db_manager.remove_question(question_id)
        self.load_questions()
        messagebox.showinfo("Info", "Question deleted successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionsApp(root)
    root.mainloop()

