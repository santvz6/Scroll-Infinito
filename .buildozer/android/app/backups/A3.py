from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
import random
from colorsys import rgb_to_hsv, hsv_to_rgb  # Para trabajar con HSV


class ColorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.color = Color(0, 0, 0, 1)
            self.puntuacion = 0
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Etiqueta para mostrar la puntuación
        self.score_label = Label(
            text=f"{self.puntuacion:.0f}",
            font_size=20,
            color=(1, 1, 1, 1),  # Color inicial (blanco)
            pos_hint={"center_x": 0.95, "center_y": 0.95},
        )
        self.count_label = Label(
            text=self.name,
            font_size=50,
            color=(1, 1, 1, 1),  # Color inicial (blanco)
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.add_widget(self.score_label)
        self.add_widget(self.count_label)

        self.last_touch_time = 0  # Para rastrear el tiempo del último toque

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def change_color(self, *args):
        # Generar un color aleatorio
        r, g, b = random.random(), random.random(), random.random()
        self.color.rgb = (r, g, b)
        
        # Calcular puntuación
        self.puntuacion = (r + g + b) / 3 * 100  # Puntuación basada en la media de RGB
        self.score_label.text = f"{self.puntuacion:.0f}"  # Actualizar el texto de la etiqueta
        self.count_label.text = self.name

        # Convertir RGB a HSV
        h, s, v = rgb_to_hsv(r, g, b)
        
        # Calcular el color complementario desplazando el tono (hue) 180 grados
        h_complementario = (h + 0.5) % 1  # +180° y mantenerlo en rango [0, 1]
        r_complementario, g_complementario, b_complementario = hsv_to_rgb(h_complementario, s, v)

        # Aplicar el color complementario al texto
        self.score_label.color = (r_complementario, g_complementario, b_complementario, 1)
        self.count_label.color = (r_complementario, g_complementario, b_complementario, 1)
        
        print(f"Fondo RGB: {self.color.rgb}, Texto Complementario RGB: {(r_complementario, g_complementario, b_complementario)}")

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            current_time = Clock.get_time()
            # Si el tiempo entre dos toques es menor a 0.3 segundos, se considera un doble toque
            if current_time - self.last_touch_time < 0.3:
                self.show_heart(touch)
            self.last_touch_time = current_time
        return super().on_touch_down(touch)

    def show_heart(self, touch):
        # Ajustar tamaño del corazón según la puntuación
        heart_size = 250 * (self.puntuacion / 100)
        # Crear un nuevo corazón en la posición del toque
        heart = Image(
            source="assets/heart.png",
            size_hint=(None, None),
            size=(heart_size, heart_size),
            pos=(touch.x - heart_size / 2, touch.y - heart_size / 2),  # Centrar el corazón en el toque
            opacity=0
        )
        self.add_widget(heart)

        # Animación para hacer aparecer y desaparecer el corazón
        anim = Animation(opacity=1, duration=0.2) + Animation(opacity=0, duration=1.0)
        anim.bind(on_complete=lambda *args: self.remove_widget(heart))  # Eliminar el corazón después de la animación
        anim.start(heart)


class ScrollApp(App):
    def build(self):
        self.sm = ScreenManager(transition=SlideTransition(direction='up', duration=0.5))
        self.screen_count = 1
        initial_screen = ColorScreen(name=f'{self.screen_count}')
        self.sm.add_widget(initial_screen)
        initial_screen.bind(on_touch_move=self.on_touch_move)
        return self.sm

    def on_touch_move(self, screen, touch):
        if touch.dy > 25:
            self.screen_count += 1
            new_screen = ColorScreen(name=f'{self.screen_count}')
            new_screen.change_color()
            new_screen.bind(on_touch_move=self.on_touch_move)  # Vincular el evento de deslizamiento
            self.sm.add_widget(new_screen)
            self.sm.current = new_screen.name
        return True


if __name__ == '__main__':
    ScrollApp().run()
