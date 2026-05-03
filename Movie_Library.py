import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []
        self.load_data()

        # Поля ввода
        tk.Label(root, text="Название").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр").grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(root)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Год выпуска").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(root)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Рейтинг (0–10)").grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = tk.Entry(root)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(root, text="Добавить фильм", command=self.add_movie).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        # Таблица вывода
        self.tree = ttk.Treeview(root, columns=("title", "genre", "year", "rating"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(root, text="Фильтр по жанру").grid(row=6, column=0, padx=5, pady=5)
        self.genre_filter = ttk.Combobox(root, state="readonly")
        self.genre_filter.grid(row=6, column=1, padx=5, pady=5)
        self.genre_filter.bind("<<ComboboxSelected>>", self.filter_by_genre)

        tk.Label(root, text="Фильтр по году").grid(row=7, column=0, padx=5, pady=5)
        self.year_filter = tk.Entry(root)
        self.year_filter.grid(row=7, column=1, padx=5, pady=5)

        tk.Button(root, text="Фильтровать по году", command=self.filter_by_year).grid(
            row=8, column=0, columnspan=2, pady=5
        )
        tk.Button(root, text="Сбросить фильтры", command=self.reset_filters).grid(
            row=9, column=0, columnspan=2, pady=5
        )

        self.update_table()
        self.update_genre_filter()

    def validate_input(self, title, genre, year, rating):
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр обязательны!")
            return False
        try:
            year = int(year)
            if year < 1888 or year > datetime.now().year:
                messagebox.showerror("Ошибка", f"Год должен быть от 1888 до {datetime.now().year}")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return False

        try:
            rating = float(rating)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
            return False

        return True

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()

        if self.validate_input(title, genre, year, rating):
            movie = {
                "title": title,
                "genre": genre,
                "year": int(year),
                "rating": float(rating)
            }
            self.movies.append(movie)
            self.save_data()
            self.update_table()
            self.update_genre_filter()

            # Очистка полей
            self.title_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.rating_entry.delete(0, tk.END)

    def filter_by_genre(self, event=None):
        selected_genre = self.genre_filter.get()
        filtered = [m for m in self.movies if m["genre"] == selected_genre]
        self.update_table(filtered)

    def filter_by_year(self):
        try:
            year = int(self.year_filter.get())
            filtered = [m for m in self.movies if m["year"] == year]
            self.update_table(filtered)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный год!")

    def reset_filters(self):
        self.year_filter.delete(0, tk.END)
        self.genre_filter.set("")
        self.update_table()

    def save_data(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists("movies.json"):
            with open("movies.json", "r", encoding="utf-8") as f:
                self.movies = json.load(f)
        else:
            self.movies = []

    def update_table(self, data=None):
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Определяем данные для отображения
        display_data = data if data is not None else self.movies

        # Заполняем таблицу
        for movie in display_data:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"  # Форматируем рейтинг до 1 знака после запятой
            ))

    def update_genre_filter(self):
        # Получаем уникальные жанры
        genres = sorted(set(movie["genre"] for movie in self.movies))
        self.genre_filter["values"] = genres

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
