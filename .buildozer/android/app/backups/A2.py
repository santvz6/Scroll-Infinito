from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import random

class ColorBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        with self.canvas:
            self.color = Color(random.random(), random.random(), random.random(), 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)
        self.bind(pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class ScrollApp(App):
    def build(self):
        root = ScrollView()
        layout = GridLayout(cols=1, size_hint_y=None, height=2 * Window.height)
        layout.bind(minimum_height=layout.setter('height'))

        for _ in range(2):  # Creamos dos cuadros de color
            color_box = ColorBox(size_hint_y=None, height=Window.height)
            layout.add_widget(color_box)

        root.add_widget(layout)
        return root

if __name__ == '__main__':
    ScrollApp().run()
