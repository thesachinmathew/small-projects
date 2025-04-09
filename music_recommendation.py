import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox,
    QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpinBox
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

# Database Setup
def initialize_db():
    conn = sqlite3.connect("music_recommendation.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        artist TEXT,
        genre TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        song_id INTEGER,
        user_name TEXT,
        age INTEGER,
        rating INTEGER,
        FOREIGN KEY (song_id) REFERENCES songs(id)
    )''')

    songs = [
    ("Lose Yourself", "Eminem", "Rap"), ("Mockingbird", "Eminem", "Rap"),
    ("Let You Down", "NF", "Rap"), ("No Name", "NF", "Rap"),
    ("Without Me", "Eminem", "Rap"), ("The Search", "NF", "Rap"),
    ("Smells Like Teen Spirit", "Nirvana", "Rock"), ("Bohemian Rhapsody", "Queen", "Rock"),
    ("Do I Wanna Know?", "Arctic Monkeys", "Indie Rock"), ("Creep", "Radiohead", "Alternative Rock"),
    ("Where Is My Mind?", "Pixies", "Alternative Rock"), ("Blinding Lights", "The Weeknd", "Pop"),
    ("Bad Guy", "Billie Eilish", "Pop"), ("Crazy Train", "Ozzy Osbourne", "Heavy Metal"),
    ("Hit Me", "Therapie Taxi", "French Pop"), ("Enter Sandman", "Metallica", "Heavy Metal"),
    ("November Rain", "Guns N' Roses", "Rock"), ("Seven Nation Army", "The White Stripes", "Alternative Rock"),
    ("Take Me Out", "Franz Ferdinand", "Indie Rock"), ("Lithium", "Nirvana", "Rock"),
    ("All the Small Things", "Blink-182", "Pop Punk"), ("Misery Business", "Paramore", "Pop Punk"),
    ("In the End", "Linkin Park", "Rock"), ("Numb", "Linkin Park", "Rock"),
    ("Boulevard of Broken Dreams", "Green Day", "Rock"), ("Holiday", "Green Day", "Rock"),
    ("Feeling Good", "Nina Simone", "Jazz"), ("Fly Me to the Moon", "Frank Sinatra", "Jazz"),
    ("Hotel California", "Eagles", "Rock"), ("Comfortably Numb", "Pink Floyd", "Progressive Rock"),
    ("Wish You Were Here", "Pink Floyd", "Progressive Rock"), ("Money", "Pink Floyd", "Progressive Rock"),
    ("Riders on the Storm", "The Doors", "Classic Rock"), ("Light My Fire", "The Doors", "Classic Rock"),
    ("Highway to Hell", "AC/DC", "Hard Rock"), ("Back in Black", "AC/DC", "Hard Rock"),
    ("Thunderstruck", "AC/DC", "Hard Rock"), ("Sweet Child O' Mine", "Guns N' Roses", "Rock"),
    ("Paradise City", "Guns N' Roses", "Rock"), ("Welcome to the Jungle", "Guns N' Roses", "Rock"),
    ("Iron Man", "Black Sabbath", "Heavy Metal"), ("Paranoid", "Black Sabbath", "Heavy Metal"),
    ("War Pigs", "Black Sabbath", "Heavy Metal"), ("Master of Puppets", "Metallica", "Heavy Metal"),
    ("Nothing Else Matters", "Metallica", "Heavy Metal"), ("One", "Metallica", "Heavy Metal"),
    ("Fade to Black", "Metallica", "Heavy Metal"), ("Hallowed Be Thy Name", "Iron Maiden", "Heavy Metal"),
    ("The Trooper", "Iron Maiden", "Heavy Metal"), ("Run to the Hills", "Iron Maiden", "Heavy Metal"),
    ("Fear of the Dark", "Iron Maiden", "Heavy Metal"), ("Breaking the Law", "Judas Priest", "Heavy Metal"),
    ("Painkiller", "Judas Priest", "Heavy Metal"), ("Livin' on a Prayer", "Bon Jovi", "Rock"),
    ("It's My Life", "Bon Jovi", "Rock"), ("You Give Love a Bad Name", "Bon Jovi", "Rock"),
    ("Uptown Funk", "Mark Ronson ft. Bruno Mars", "Pop"), ("24K Magic", "Bruno Mars", "Pop"),
    ("Grenade", "Bruno Mars", "Pop"), ("Just the Way You Are", "Bruno Mars", "Pop"),
    ("Stay", "The Kid LAROI & Justin Bieber", "Pop"), ("Sorry", "Justin Bieber", "Pop"),
    ("Love Yourself", "Justin Bieber", "Pop"), ("Baby", "Justin Bieber", "Pop"),
    ("Shape of You", "Ed Sheeran", "Pop"), ("Perfect", "Ed Sheeran", "Pop"),
    ("Thinking Out Loud", "Ed Sheeran", "Pop"), ("Photograph", "Ed Sheeran", "Pop"),
    ("Shallow", "Lady Gaga & Bradley Cooper", "Pop"), ("Bad Romance", "Lady Gaga", "Pop"),
    ("Poker Face", "Lady Gaga", "Pop"), ("Born This Way", "Lady Gaga", "Pop"),
    ("Halo", "Beyoncé", "Pop"), ("Single Ladies", "Beyoncé", "Pop"),
    ("Crazy in Love", "Beyoncé", "Pop"), ("Irreplaceable", "Beyoncé", "Pop"),
    ("Take On Me", "A-ha", "80s Pop"), ("Billie Jean", "Michael Jackson", "80s Pop"),
    ("Thriller", "Michael Jackson", "80s Pop"), ("Beat It", "Michael Jackson", "80s Pop"),
    ("Smooth Criminal", "Michael Jackson", "80s Pop"), ("Like a Prayer", "Madonna", "80s Pop"),
    ("Material Girl", "Madonna", "80s Pop"), ("Livin’ la Vida Loca", "Ricky Martin", "Latin Pop"),
    ("Despacito", "Luis Fonsi ft. Daddy Yankee", "Latin Pop"), ("Bailando", "Enrique Iglesias", "Latin Pop"),
    ("Hips Don't Lie", "Shakira", "Latin Pop"), ("Waka Waka", "Shakira", "Latin Pop"),
    ("Gasolina", "Daddy Yankee", "Reggaeton"), ("Dákiti", "Bad Bunny", "Reggaeton"),
    ("Ella Baila Sola", "Eslabón Armado & Peso Pluma", "Regional Mexican"),
    ("Titi Me Preguntó", "Bad Bunny", "Reggaeton"), ("Ojitos Lindos", "Bad Bunny", "Reggaeton"),
    ("Bodak Yellow", "Cardi B", "Hip-Hop"), ("Money", "Cardi B", "Hip-Hop"),
    ("WAP", "Cardi B & Megan Thee Stallion", "Hip-Hop"), ("Hotline Bling", "Drake", "Hip-Hop"),
    ("God's Plan", "Drake", "Hip-Hop"), ("In My Feelings", "Drake", "Hip-Hop"),
    ("Sicko Mode", "Travis Scott", "Hip-Hop"), ("Goosebumps", "Travis Scott", "Hip-Hop"),
    ("The Box", "Roddy Ricch", "Hip-Hop"), ("Rockstar", "Post Malone", "Hip-Hop"),
    ("Circles", "Post Malone", "Hip-Hop"), ("Sunflower", "Post Malone & Swae Lee", "Hip-Hop"),
    ("Congratulations", "Post Malone", "Hip-Hop"), ("Lucid Dreams", "Juice WRLD", "Hip-Hop"),
    ("Robbery", "Juice WRLD", "Hip-Hop"), ("All Girls Are the Same", "Juice WRLD", "Hip-Hop"),
    ("Legends", "Juice WRLD", "Hip-Hop"), ("Superstition", "Stevie Wonder", "Soul"),
    ("Ain’t No Mountain High Enough", "Marvin Gaye & Tammi Terrell", "Soul"),
    ("What's Going On", "Marvin Gaye", "Soul"), ("Respect", "Aretha Franklin", "Soul"),
    ("Chain of Fools", "Aretha Franklin", "Soul"), ("Sittin' On The Dock of the Bay", "Otis Redding", "Soul"),
    ("My Girl", "The Temptations", "Soul"), ("I Want You Back", "The Jackson 5", "Motown"),
    ("Ain't Too Proud to Beg", "The Temptations", "Motown"), ("Dancing in the Street", "Martha and the Vandellas", "Motown"),
]


    cursor.executemany("INSERT INTO songs (name, artist, genre) VALUES (?, ?, ?)", songs)
    conn.commit()
    conn.close()

# Main GUI
class MusicRecommendationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Recommendation System")
        self.setGeometry(400, 200, 600, 600)
        self.initUI()
        self.setDarkMode()

    def setDarkMode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))  # Black background
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # White text
        self.setPalette(palette)

    def initUI(self):
        layout = QVBoxLayout()

        # Genre-based Recommendation
        self.genre_label = QLabel("Select your favorite genre:")
        layout.addWidget(self.genre_label)

        self.genre_dropdown = QComboBox()
        self.genre_dropdown.addItems(["Rap", "Rock", "Indie Rock", "Heavy Metal", "Alternative Rock", "Pop", "French Pop"])
        layout.addWidget(self.genre_dropdown)

        self.recommend_btn = QPushButton("Get Recommendation")
        self.recommend_btn.clicked.connect(self.get_recommendation)
        layout.addWidget(self.recommend_btn)

        self.recommendation_label = QLabel("")
        layout.addWidget(self.recommendation_label)

        # Song Rating System
        self.song_label = QLabel("Select a song to rate:")
        layout.addWidget(self.song_label)

        self.song_dropdown = QComboBox()
        self.load_songs()
        layout.addWidget(self.song_dropdown)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        layout.addWidget(self.name_input)

        self.age_input = QSpinBox()
        self.age_input.setRange(10, 100)
        self.age_input.setPrefix("Age: ")
        layout.addWidget(self.age_input)

        self.rating_input = QSpinBox()
        self.rating_input.setRange(1, 5)
        self.rating_input.setPrefix("Rating: ")
        layout.addWidget(self.rating_input)

        self.submit_rating_btn = QPushButton("Submit Rating")
        self.submit_rating_btn.clicked.connect(self.submit_rating)
        layout.addWidget(self.submit_rating_btn)

        # View & Manage Ratings
        self.view_ratings_btn = QPushButton("View & Manage Ratings")
        self.view_ratings_btn.clicked.connect(self.view_ratings)
        layout.addWidget(self.view_ratings_btn)

        self.ratings_table = QTableWidget()
        self.ratings_table.setColumnCount(4)
        self.ratings_table.setHorizontalHeaderLabels(["Name", "Age", "Song", "Rating"])
        layout.addWidget(self.ratings_table)

        self.delete_rating_btn = QPushButton("Delete Selected Rating")
        self.delete_rating_btn.clicked.connect(self.delete_rating)
        layout.addWidget(self.delete_rating_btn)

        self.setLayout(layout)

    def get_recommendation(self):
        genre = self.genre_dropdown.currentText()
        conn = sqlite3.connect("music_recommendation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT artist FROM songs WHERE genre = ? LIMIT 1", (genre,))
        result = cursor.fetchone()
        conn.close()

        if result:
            self.recommendation_label.setText(f"Recommended Artist: {result[0]}")
        else:
            self.recommendation_label.setText("No artist found for this genre.")

    def load_songs(self):
        conn = sqlite3.connect("music_recommendation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM songs")
        songs = cursor.fetchall()
        conn.close()

        self.song_dropdown.clear()
        for song in songs:
            self.song_dropdown.addItem(song[0])

    def submit_rating(self):
        name = self.name_input.text()
        age = self.age_input.value()
        song_name = self.song_dropdown.currentText()
        rating = self.rating_input.value()

        if not name:
            self.recommendation_label.setText("Please enter your name.")
            return

        conn = sqlite3.connect("music_recommendation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM songs WHERE name = ?", (song_name,))
        song_id = cursor.fetchone()

        if song_id:
            cursor.execute("INSERT INTO ratings (song_id, user_name, age, rating) VALUES (?, ?, ?, ?)",
                           (song_id[0], name, age, rating))
            conn.commit()
            self.recommendation_label.setText("Rating submitted successfully!")
        conn.close()
        self.view_ratings()

    def view_ratings(self):
        conn = sqlite3.connect("music_recommendation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT user_name, age, songs.name, rating FROM ratings JOIN songs ON ratings.song_id = songs.id")
        ratings = cursor.fetchall()
        conn.close()

        self.ratings_table.setRowCount(len(ratings))
        for row_idx, row_data in enumerate(ratings):
            for col_idx, col_data in enumerate(row_data):
                self.ratings_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def delete_rating(self):
        selected_row = self.ratings_table.currentRow()
        if selected_row == -1:
            return

        user_name = self.ratings_table.item(selected_row, 0).text()
        song_name = self.ratings_table.item(selected_row, 2).text()

        conn = sqlite3.connect("music_recommendation.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ratings WHERE user_name = ? AND song_id = (SELECT id FROM songs WHERE name = ?)",
                       (user_name, song_name))
        conn.commit()
        conn.close()
        self.view_ratings()

if __name__ == "__main__":
    initialize_db()
    app = QApplication(sys.argv)
    window = MusicRecommendationApp()
    window.show()
    sys.exit(app.exec_())
