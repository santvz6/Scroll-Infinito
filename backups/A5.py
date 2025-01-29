from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock
import random

class ColorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.likes = 0  # Contador de likes
        
        # Fondo de pantalla con color dinámico
        with self.canvas:
            self.color = Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Contenedor principal
        self.layout = BoxLayout(orientation='horizontal')
        self.add_widget(self.layout)
        
        # Espacio vacío a la izquierda
        self.left_space = BoxLayout()
        self.layout.add_widget(self.left_space)
        
        # Etiqueta de la pantalla
        self.count_label = Label(
            text=self.name,
            font_size=100,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        self.layout.add_widget(self.count_label)
        
        # Contenedor de la interfaz de likes
        self.right_layout = BoxLayout(orientation='vertical', size_hint=(None, 1), width=100)
        self.layout.add_widget(self.right_layout)
        
        # Botón de like (corazón)
        self.like_button = Button(
            background_normal='assets/heart.png',
            background_down='assets/heart_filled.png',
            size_hint=(None, None),
            size=(80, 80),
            on_press=self.increment_likes
        )
        self.right_layout.add_widget(self.like_button)
        
        # Etiqueta del contador de likes
        self.like_label = Label(
            text=str(self.likes),
            font_size=40,
            color=(1, 1, 1, 1)
        )
        self.right_layout.add_widget(self.like_label)
        
        self.last_touch_time = 0  # Para rastrear el tiempo del último toque

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def change_color(self):
        r, g, b = random.random(), random.random(), random.random()
        self.color.rgb = (r, g, b)
        luminosidad = 0.299 * r + 0.587 * g + 0.114 * b
        text_color = (1, 1, 1, 1) if luminosidad < 0.5 else (0, 0, 0, 1)
        self.count_label.color = text_color
        self.like_label.color = text_color
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            current_time = Clock.get_time()
            if current_time - self.last_touch_time < 0.3:
                self.increment_likes()
                self.show_heart(touch)
            self.last_touch_time = current_time
        return super().on_touch_down(touch)

    def increment_likes(self, *args):
        self.likes += 1
        self.like_label.text = str(self.likes)
    
    def show_heart(self, touch):
        heart_size = 100
        heart = Image(
            source='assets/heart.png',
            size_hint=(None, None),
            size=(heart_size, heart_size),
            pos=(touch.x - heart_size / 2, touch.y - heart_size / 2),
            opacity=0
        )
        self.add_widget(heart)
        anim = Animation(opacity=1, duration=0.2) + Animation(opacity=0, duration=1.0)
        anim.bind(on_complete=lambda *args: self.remove_widget(heart))
        anim.start(heart)

class ScrollApp(App):
    def build(self):
        self.sm = ScreenManager(transition=SlideTransition(direction='up', duration=0.5))
        self.history = []
        self.current_index = -1
        self.add_new_screen()
        return self.sm

    def add_new_screen(self):
        self.current_index += 1
        self.history = self.history[:self.current_index]
        screen_count = len(self.history) + 1
        new_screen = ColorScreen(name=f"{screen_count}")
        new_screen.change_color()
        new_screen.bind(on_touch_move=self.on_touch_move)
        self.sm.add_widget(new_screen)
        self.history.append(new_screen.name)
        self.sm.current = new_screen.name

    def navigate_to_screen(self, index):
        self.sm.transition.direction = 'down' if index < self.current_index else 'up'
        self.current_index = index
        self.sm.current = self.history[self.current_index]

    def on_touch_move(self, screen, touch):
        if touch.dy > 25:
            if self.current_index == len(self.history) - 1:
                self.add_new_screen()
            else:
                self.navigate_to_screen(self.current_index + 1)
        elif touch.dy < -25:
            if self.current_index > 0:
                self.navigate_to_screen(self.current_index - 1)
        return True

if __name__ == "__main__":
    ScrollApp().run()