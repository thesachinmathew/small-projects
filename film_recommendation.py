import sqlite3
import os
import tkinter as tk
from tkinter import messagebox

# Database setup
DB_PATH = "film_ratings.db"

# Create database and table if not exists
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY,
            film TEXT NOT NULL,
            genre TEXT NOT NULL,
            rating INTEGER NOT NULL
        )
    ''')

    # Add dummy data if empty
    cursor.execute("SELECT COUNT(*) FROM ratings")
    if cursor.fetchone()[0] == 0:
        dummy_data = [
            ('Inception', 'Sci-Fi', 5), ('Interstellar', 'Sci-Fi', 5), ('The Matrix', 'Sci-Fi', 4),
            ('The Godfather', 'Crime', 5), ('Pulp Fiction', 'Crime', 5), ('Goodfellas', 'Crime', 4),
            ('The Dark Knight', 'Action', 5), ('Mad Max: Fury Road', 'Action', 5), ('John Wick', 'Action', 4),
            ('Spirited Away', 'Animation', 5), ('Coco', 'Animation', 5), ('Toy Story', 'Animation', 4),
            ('La La Land', 'Romance', 5), ('Titanic', 'Romance', 5), ('The Notebook', 'Romance', 4)
        ]
        cursor.executemany("INSERT INTO ratings (film, genre, rating) VALUES (?, ?, ?)", dummy_data)

    conn.commit()
    conn.close()

# Fetch film recommendations
def recommend_films():
    selected_genres = [genre for genre, var in genres.items() if var.get()]

    if not selected_genres:
        messagebox.showerror("Error", "Please select at least one genre.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    result_text = ""
    for genre in selected_genres:
        cursor.execute('''
            SELECT film, AVG(rating) as avg_rating 
            FROM ratings 
            WHERE genre = ? 
            GROUP BY film 
            ORDER BY avg_rating DESC 
            LIMIT 3
        ''', (genre,))
        
        films = cursor.fetchall()

        result_text += f"\n🎬 Recommended Films for {genre}:\n"
        if films:
            for film, rating in films:
                result_text += f"   - {film} (⭐ {round(rating, 1)}/5)\n"
        else:
            result_text += "   No ratings available yet.\n"

    conn.close()
    
    messagebox.showinfo("Film Recommendations", result_text)

# Open film rating window
def open_rating_window():
    rating_window = tk.Toplevel(root)
    rating_window.title("Rate a Film")
    rating_window.geometry("300x250")
    rating_window.configure(bg="#222222")

    tk.Label(rating_window, text="Film Name:", fg="white", bg="#222222").pack(pady=5)
    film_entry = tk.Entry(rating_window)
    film_entry.pack(pady=5)

    tk.Label(rating_window, text="Genre:", fg="white", bg="#222222").pack(pady=5)
    genre_entry = tk.Entry(rating_window)
    genre_entry.pack(pady=5)

    tk.Label(rating_window, text="Rating (1-5):", fg="white", bg="#222222").pack(pady=5)
    rating_entry = tk.Entry(rating_window)
    rating_entry.pack(pady=5)

    def submit_rating():
        film = film_entry.get().strip()
        genre = genre_entry.get().strip()
        try:
            rating = int(rating_entry.get().strip())
            if not (1 <= rating <= 5):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number between 1 and 5.")
            return

        if not film or not genre:
            messagebox.showerror("Error", "Please enter all fields.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ratings (film, genre, rating) VALUES (?, ?, ?)", 
                       (film, genre, rating))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Rating submitted successfully!")
        rating_window.destroy()

    submit_button = tk.Button(rating_window, text="Submit Rating", command=submit_rating, bg="#333333", fg="white")
    submit_button.pack(pady=10)

# Initialize main application
initialize_database()
root = tk.Tk()
root.title("Film Recommendation System")
root.geometry("500x400")
root.configure(bg="#111111")
root.resizable(False, False)

# Centering the window
root.eval('tk::PlaceWindow . center')

tk.Label(root, text="Film Recommendation System", font=("Arial", 14, "bold"), fg="white", bg="#111111").pack(pady=10)
tk.Label(root, text="Enter Your Name:", fg="white", bg="#111111").pack()
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Label(root, text="Enter Age:", fg="white", bg="#111111").pack()
age_entry = tk.Entry(root)
age_entry.pack(pady=5)

tk.Label(root, text="Select Genres:", fg="white", bg="#111111").pack()

# Genres with checkboxes
genre_list = ["Sci-Fi", "Crime", "Action", "Animation", "Romance"]
genres = {genre: tk.IntVar() for genre in genre_list}

for genre, var in genres.items():
    tk.Checkbutton(root, text=genre, variable=var, fg="white", bg="#111111", selectcolor="#222222").pack(anchor="w", padx=140)

# Buttons for recommendations and rating
recommend_button = tk.Button(root, text="Get Recommendations", command=recommend_films, bg="#222222", fg="white")
recommend_button.pack(pady=10)

rate_button = tk.Button(root, text="Rate a Film", command=open_rating_window, bg="#333333", fg="white")
rate_button.pack()

root.mainloop()
