from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import random

class ColorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.color = Color(1, 1, 1, 1)  # Blanco inicial
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def change_color(self, *args):
        r, g, b = random.random(), random.random(), random.random()
        self.color.rgb = (r, g, b)
        print(f"Cambio de color a: {self.color.rgb}")  # Mensaje de depuración

class ScrollApp(App):
    def build(self):
        self.sm = ScreenManager(transition=SlideTransition(direction='up', duration=0.5))
        self.screen_count = 1
        initial_screen = ColorScreen(name=f'color_screen_{self.screen_count}')
        self.sm.add_widget(initial_screen)
        initial_screen.bind(on_touch_move=self.on_touch_move)
        return self.sm

    def on_touch_move(self, screen, touch):
        if touch.dy > 5:
            self.screen_count += 1
            new_screen = ColorScreen(name=f'color_screen_{self.screen_count}')
            new_screen.change_color()
            new_screen.bind(on_touch_move=self.on_touch_move)  # Vincular el evento de deslizamiento
            self.sm.add_widget(new_screen)
            self.sm.current = new_screen.name
        return True

if __name__ == '__main__':
    ScrollApp().run()
