from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
import random


class ColorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.color = Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Etiquetas
        self.score_label = Label(
            text="0",
            font_size=50,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.95, "center_y": 0.95},
        )
        self.count_label = Label(
            text=self.name,
            font_size=100,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.add_widget(self.score_label)
        self.add_widget(self.count_label)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def change_color(self):
        # Generar un color aleatorio
        r, g, b = random.random(), random.random(), random.random()
        self.color.rgb = (r, g, b)
        self.rect.size = self.size
        self.rect.pos = self.pos

        # Actualizar etiquetas
        self.score_label.text = f"{((r + g + b) / 3 * 100):.0f}"
        self.count_label.text = self.name

        # Cambiar el color del texto según la luminosidad
        luminosidad = 0.299 * r + 0.587 * g + 0.114 * b
        text_color = (1, 1, 1, 1) if luminosidad < 0.5 else (0, 0, 0, 1)
        self.score_label.color = text_color
        self.count_label.color = text_color


class ScrollApp(App):
    def build(self):
        self.sm = ScreenManager(transition=SlideTransition(direction="up", duration=0.5))
        self.history = []  # Historial de pantallas
        self.current_index = -1  # Índice actual en el historial

        # Primera pantalla
        self.add_new_screen()

        return self.sm

    def add_new_screen(self):
        """Crea y añade una nueva pantalla al ScreenManager."""
        self.current_index += 1  # Mover el índice hacia adelante
        # Eliminar pantallas futuras si se navega hacia adelante desde un punto intermedio
        self.history = self.history[: self.current_index]

        # Crear una nueva pantalla
        screen_count = len(self.history) + 1
        new_screen = ColorScreen(name=f"{screen_count}")
        new_screen.change_color()
        new_screen.bind(on_touch_move=self.on_touch_move)

        # Añadir la pantalla al administrador y al historial
        self.sm.add_widget(new_screen)
        self.history.append(new_screen.name)
        self.sm.current = new_screen.name

    def navigate_to_screen(self, index):
        """Navega a una pantalla existente en el historial."""
        if index < self.current_index:  # Retroceder
            self.sm.transition.direction = "down"
        else:  # Avanzar
            self.sm.transition.direction = "up"
        
        self.current_index = index
        self.sm.current = self.history[self.current_index]

    def on_touch_move(self, screen, touch):
        if touch.dy > 25:  # Deslizar hacia arriba
            if self.current_index == len(self.history) - 1:
                self.add_new_screen()  # Añadir una nueva pantalla si estamos en la última
            else:
                self.navigate_to_screen(self.current_index + 1)  # Navegar hacia adelante

        elif touch.dy < -25:  # Deslizar hacia abajo
            if self.current_index > 0:  # Si no estamos en la primera pantalla
                self.navigate_to_screen(self.current_index - 1)  # Navegar hacia atrás

        return True


if __name__ == "__main__":
    ScrollApp().run()
