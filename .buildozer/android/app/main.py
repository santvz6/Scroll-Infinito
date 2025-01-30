# Aplicación móvil - Funcionalidad
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
# Extra
import random
# Hasheo de Contraseñas - Seguridad
import bcrypt
# Base de datos - Almacenamiento
import firebase_admin
from firebase_admin import credentials, firestore


# Inicializamos la app de Firebase con las credenciales
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)
# Obtención del cliente por firebase_credentials.json
db = firestore.client()

# Función para hashear la contraseña
def hash_password(password):
    # Generación del salt (antes de hashear)
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Función para verificar la contraseña
def check_password(stored_hash, password):
    # checkpw() 
    # * Extrae el salt del hash almacenado.
    # * Combina ese salt con la contraseña ingresada.
    # * Realiza las rondas de hashing para generar un nuevo hash.
    # * Compara el nuevo hash con el hash almacenado para verificar si coinciden.
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)


# Pantalla Gestión de Usuario
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 🔹 FONDO MÁS ESTÉTICO
        with self.canvas.before:
            Color(52/255, 152/255, 219/255, 1)  # Azul moderno
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # 📌 Ajusta el fondo dinámicamente
        self.bind(size=self.update_rect, pos=self.update_rect)

        # 🔹 DISEÑO GENERAL
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        # 🔹 ESTILO DE LOS CAMPOS DE TEXTO
        self.username_input = TextInput(
            hint_text="Usuario",
            background_color=(1, 1, 1, 0.2),  # Blanco translúcido
            foreground_color=(1, 1, 1, 1),  # Texto blanco
            size_hint=(1, None), height=50,
            padding=(10, 10),
        )
        
        self.password_input = TextInput(
            hint_text="Contraseña",
            password=True,
            background_color=(1, 1, 1, 0.2),
            foreground_color=(1, 1, 1, 1),
            size_hint=(1, None), height=50,
            padding=(10, 10),
        )

        # 🔹 MENSAJE DE ERROR / INFO
        self.message_label = Label(
            text="",
            color=(1, 0, 0, 1),  # Rojo
            size_hint=(1, None),
            height=30
        )

        # 🔹 BOTONES ESTILIZADOS
        login_button = Button(
            text="Iniciar Sesión",
            background_color=(0.2, 0.6, 1, 1),  # Azul brillante
            color=(1, 1, 1, 1),  # Texto blanco
            size_hint=(1, None),
            height=50,
            on_press = self.login
        )

        register_button = Button(
            text="Registrarse",
            background_color=(0.1, 0.4, 0.9, 1),  # Azul oscuro
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
            on_press = self.register
        )

        # 🔹 AGREGA LOS WIDGETS
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.message_label)
        layout.add_widget(login_button)
        layout.add_widget(register_button)
        
        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def login(self, instance):
        # Obtener los datos del formulario
        username = self.username_input.text
        password = self.password_input.text

        # Obtenemos la referencia a la colección de usuarios 
        users_ref = db.collection('users')
        
        # Obtenemos el documento del usuario
        user_doc = users_ref.document(username).get()
        
        if user_doc.exists:
            # Obtener el hash de la contraseña almacenado
            stored_hash = user_doc.to_dict()['password']
            
            # Verificar la contraseña
            if check_password(stored_hash.encode('utf-8'), password):
                # Llamamos al método para generar una pantalla nueva de scroll
                # App.get_runninf_app() para obtener la instancia de ScrollApp
                App.get_running_app().add_new_screen()
            else:
                self.message_label.text = "Información Incorrecta"
        else:
            self.message_label.text = "Usuario no registrado"
    
    def register(self, instance):
        # Obtener los datos de usuario
        username = self.username_input.text
        password = self.password_input.text

        
        users_ref = db.collection('users')
        
        user_doc = users_ref.document(username).get()
        
        if user_doc.exists:
            self.message_label.text = "El usuario ya existe"
        else:
            hashed_password = hash_password(password)
            
            # Creamos un nuevo documento en Firestore
            users_ref.document(username).set({
                'username': username,
                'password': hashed_password.decode('utf-8')  # Guardamos el hash como string
            })
            self.message_label.text = "User registered!"

# Pantalla Juego Scroll
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

        self.last_touch_time = 0  # Rastrea el tiempo del último toque

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def change_color(self):
        
        r, g, b = random.random(), random.random(), random.random()
        self.color.rgb = (r, g, b)

        # Actualización de etiquetas
        self.score_label.text = f"{((r + g + b) / 3 * 100):.0f}"
        self.count_label.text = self.name

        # Ajuste del color del texto según la luminosidad
        luminosidad = 0.299 * r + 0.587 * g + 0.114 * b
        text_color = (1, 1, 1, 1) if luminosidad < 0.5 else (0, 0, 0, 1)
        self.score_label.color = text_color
        self.count_label.color = text_color

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
        heart_size = 300 * (float(self.score_label.text) / 100)
        # Crear un nuevo corazón en la posición del toque
        heart = Image(
            source="assets/heart.png",
            size_hint=(None, None),
            size=(heart_size, heart_size),
            pos=(touch.x - heart_size / 2, touch.y - heart_size / 2),  # Centrar el corazón en el toque
            opacity=0,
        )
        self.add_widget(heart)

        # Animación para hacer aparecer y desaparecer el corazón
        anim = Animation(opacity=1, duration=0.2) + Animation(opacity=0, duration=1.0)
        anim.bind(on_complete=lambda *args: self.remove_widget(heart))  # Eliminar el corazón después de la animación
        anim.start(heart)

# Aplicación
class ScrollApp(App):
    def build(self):
        # Crear ScreenManager
        self.sm = ScreenManager(transition=SlideTransition())

        self.history = []  # Historial de pantallas
        self.current_index = -1  # Índice actual en el historial

        # Añadimos las pantalla del Login
        self.sm.add_widget(LoginScreen(name="login"))
        
        return self.sm

    def add_new_screen(self):
        """Crea y añade una nueva pantalla al ScreenManager."""
        self.current_index += 1  # Mover el índice hacia adelante
        # Eliminar pantallas futuras si se navega hacia adelante desde un punto intermedio
        self.history = self.history[:self.current_index]

        # Crear una nueva pantalla
        screen_count = len(self.history) + 1
        new_screen = ColorScreen(name=f"{screen_count}")
        new_screen.change_color()
        new_screen.bind(on_touch_move=self.on_touch_move)

        # Configuración de la transición para la primera pantalla después del login
        if self.current_index == 1:  
            self.sm.transition.direction = 'up' 

        # Añadimos la pantalla al manager y al historial
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
