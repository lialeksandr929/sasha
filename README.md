# sasha
# Александр Ли
# GUI-приложение «Movie Library» для хранения информации о фильмах с фильтрацией, JSON и Git
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library — Личная кинотека")
        self.root.geometry("800x600")

        # Данные
        self.movies = []
        self.load_data()

        # Создаём интерфейс
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Форма добавления фильма
        form_frame = tk.LabelFrame(self.root, text="Добавить фильм", padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        # Название
        tk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        # Жанр
        tk.Label(form_frame, text="Жанр:").grid(row=1, column=0, sticky="w")
        self.genre_entry = tk.Entry(form_frame, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=2)

        # Год выпуска
        tk.Label(form_frame, text="Год выпуска:").grid(row=2, column=0, sticky="w")
        self.year_entry = tk.Entry(form_frame, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=2)

        # Рейтинг
        tk.Label(form_frame, text="Рейтинг (0–10):").grid(row=3, column=0, sticky="w")
        self.rating_entry = tk.Entry(form_frame, width=30)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=2)

        # Кнопка добавления
        add_button = tk.Button(form_frame, text="Добавить фильм", command=self.add_movie)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, sticky="w")
        self.genre_filter = ttk.Combobox(filter_frame, state="readonly")
        self.genre_filter.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(filter_frame, text="Год:").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.year_filter = tk.Entry(filter_frame, width=10)
        self.year_filter.grid(row=0, column=3, padx=5, pady=2)

        filter_button = tk.Button(filter_frame, text="Применить фильтры", command=self.apply_filters)
        filter_button.grid(row=0, column=4, padx=(20, 0))

        reset_button = tk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters)
        reset_button.grid(row=0, column=5, padx=5)

        # Таблица
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Название", "Жанр", "Год выпуска", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        # Проверка корректности ввода
        if not title:
            messagebox.showerror("Ошибка", "Введите название фильма!")
            return

        try:
            year = int(year_str)
            if year < 1888 or year > datetime.now().year:
                messagebox.showerror("Ошибка", f"Год должен быть от 1888 до {datetime.now().year}!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return

        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return

        # Добавляем фильм
        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(movie)

        # Обновляем интерфейс
        self.refresh_table()
        self.update_genre_filter()

        # Очищаем форму
        self.clear_form()
        self.save_data()

    def refresh_table(self, filtered_movies=None):
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем данными
        movies_to_show = filtered_movies if filtered_movies is not None else self.movies
        for movie in movies_to_show:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"
            ))

    def apply_filters(self):
        genre_filter = self.genre_filter.get()
        year_filter_str = self.year_filter.get().strip()

        filtered_movies = self.movies

        if genre_filter:
            filtered_movies = [m for m in filtered_movies if m["genre"] == genre_filter

        if year_filter_str:
            try:
                year_filter = int(year_filter_str)
                filtered_movies = [m for m in filtered_movies if m["year"] == year_filter]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтрации должен быть числом!")
                return

        self.refresh_table(filtered_movies)

    def reset_filters(self):
        self.genre_filter.set("")
        self.year_filter.delete(0, tk.END)
        self.refresh_table()

    def update_genre_filter(self):
        genres = sorted(set(m["genre"] for m in self.movies))
        self.genre_filter["values"] = genres

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def save_data(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.
