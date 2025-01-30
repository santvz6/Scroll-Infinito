import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import random

# Configurar base de datos
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.username_input = TextInput(hint_text="Username")
        self.password_input = TextInput(hint_text="Password", password=True)
        self.message_label = Label(text="")
        login_button = Button(text="Login", on_press=self.login)
        register_button = Button(text="Register", on_press=self.register)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.message_label)
        layout.add_widget(login_button)
        layout.add_widget(register_button)
        self.add_widget(layout)
    
    def login(self, instance):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                       (self.username_input.text, self.password_input.text))
        user = cursor.fetchone()
        conn.close()
        if user:
            self.manager.current = "main"
        else:
            self.message_label.text = "Invalid credentials"
    
    def register(self, instance):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                           (self.username_input.text, self.password_input.text))
            conn.commit()
            self.message_label.text = "User registered!"
        except sqlite3.IntegrityError:
            self.message_label.text = "Username already exists"
        conn.close()

class ColorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.color = Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)
        self.score_label = Label(text="0", font_size=50, color=(1, 1, 1, 1),
                                 pos_hint={"center_x": 0.95, "center_y": 0.95})
        self.add_widget(self.score_label)
        self.change_color()

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
    
    def change_color(self):
        r, g, b = random.random(), random.random(), random.random()
        self.color.rgb = (r, g, b)
        self.score_label.text = f"{((r + g + b) / 3 * 100):.0f}"

class ScrollApp(App):
    def build(self):
        """lógica"""

if __name__ == "__main__":
    ScrollApp().run()
