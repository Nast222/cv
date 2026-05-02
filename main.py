import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

FILE_HISTORY = "tasks.json"

# Предопределённые задачи с типами
PREDEFINED_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
    {"text": "Посмотреть лекцию", "type": "учёба"},
    {"text": "Пробежка 3 км", "type": "спорт"},
    {"text": "Провести созвон", "type": "работа"},
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("500x400")

        self.history = self.load_history()

        # Виджеты
        self.create_widgets()
        self.update_history_list()

    def create_widgets(self):
        # Кнопка генерации
        self.btn_generate = tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task)
        self.btn_generate.pack(pady=10)

        # Поле для новой задачи
        self.entry_task = tk.Entry(self.root, width=40)
        self.entry_task.pack(pady=5)

        # Поле для типа задачи
        self.combo_type = ttk.Combobox(self.root, values=["учёба", "спорт", "работа"], state="readonly")
        self.combo_type.current(0)
        self.combo_type.pack(pady=5)

        # Кнопка добавления своей задачи
        self.btn_add = tk.Button(self.root, text="Добавить свою задачу", command=self.add_custom_task)
        self.btn_add.pack(pady=5)

        # Фильтр по типу
        self.label_filter = tk.Label(self.root, text="Фильтр по типу:")
        self.label_filter.pack()

        self.filter_var = tk.StringVar(value="все")
        for val in ["все", "учёба", "спорт", "работа"]:
            tk.Radiobutton(self.root, text=val.capitalize(), variable=self.filter_var, value=val,
                           command=self.update_history_list).pack(anchor="w")

        # Список истории
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox_history = tk.Listbox(self.root, yscrollcommand=self.scrollbar.set, width=60, height=10)
        self.listbox_history.pack(pady=10)
        self.scrollbar.config(command=self.listbox_history.yview)

    def generate_task(self):
        task = random.choice(PREDEFINED_TASKS)
        self.history.append(task)
        self.save_history()
        self.update_history_list()

    def add_custom_task(self):
        text = self.entry_task.get().strip()
        task_type = self.combo_type.get()

        if not text:
            messagebox.showerror("Ошибка", "Введите текст задачи!")
            return

        task = {"text": text, "type": task_type}
        self.history.append(task)
        self.save_history()
        self.entry_task.delete(0, tk.END)
        self.update_history_list()

    def update_history_list(self):
        self.listbox_history.delete(0, tk.END)
        filter_type = self.filter_var.get()

        for task in self.history:
            if filter_type == "все" or task["type"] == filter_type:
                self.listbox_history.insert(tk.END, f"{task['text']} ({task['type']})")

    def load_history(self):
        if os.path.exists(FILE_HISTORY):
            with open(FILE_HISTORY, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(FILE_HISTORY, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
