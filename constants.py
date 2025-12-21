# CONFIGURACIÓN DE VENTANA
WIDTH_SCREEN = 800
HEIGHT_SCREEN = 600
FPS = 60  # Frame Rate (cuadros por segundo)

# CONFIGURACIÓN DEL JUGADOR
HEIGHT_CHARACTER = 27
WIDTH_CHARACTER = 27
COLOR_CHARACTER = (255, 255, 0)  # Color amarillo
SPEED_CHARACTER = 5  # Velocidad de movimiento
SCALE_CHARACTER = 2.5  # Escala de la imagen del jugador

# CONFIGURACIÓN DE PACIENTES
SCALE_PATIENT = 0.1  # Escala de las imágenes de pacientes
# Posiciones configurables por tipo de paciente (x, y)
# Puedes modificar estas coordenadas para mover a cada paciente
PATIENT_POSITIONS = {
    "green": [
        (150, 150),  # Paciente 1 verde
        (150, 375),  # Paciente 2 verde
        (550, 150),  # Paciente 3 verde
        (550, 250),  # Paciente 4 verde
        (550, 375),  # Paciente 5 verde
        (150, 250),  # Paciente 6 verde
    ],
    "yellow": [
        (110, 70),  # Paciente 1 amarillo
        (60, 230),  # Paciente 2 amarillo
        (575, 70),  # Paciente 3 amarillo
        (110, 400),  # Paciente 4 amarillo
        (625, 230),  # Paciente 5 amarillo
        (550, 400),  # Paciente 6 amarillo
    ],
    "orange": [
        (100, 150),  # Paciente 1 naranja
        (100, 375),  # Paciente 2 naranja
        (600, 150),  # Paciente 3 naranja
        (600, 275),  # Paciente 4 naranja
        (600, 375),  # Paciente 5 naranja
        (100, 275),  # Paciente 6 naranja
    ],
}

# Asignación de assets a cada slot de paciente (índices de carpeta/animación)
# Los índices corresponden a las carpetas de pacientes (patient1, patient2, etc.)
# Si hay menos carpetas que pacientes, se reutilizan los índices disponibles
PATIENT_ASSET_MAP = {
    # Nivel 1: 6 verdes (usa las 6 carpetas disponibles: 0, 1, 2, 3, 4, 5)
    "level1_green": [0, 1, 2, 3, 4, 5],
    # Nivel 2: 6 6 amarillos (usa las 6 carpetas disponibles: 0, 1, 2, 3, 4, 5)
    "level2_yellow": [0, 1, 2, 3, 4, 5],
    # Nivel 3: 6 naranjas (usa las 6 carpetas disponibles: 0, 1, 2, 3, 4, 5)
    "level3_orange": [0, 1, 2, 3, 4, 5],
}

# ESTADOS DEL JUEGO

# Estos valores se usan para saber en qué pantalla está el juego.
# Si agregas un nuevo estado, hazlo aquí y úsalo en main.py
MENU = 0        # Menú inicial
PLAYING = 1     # Jugando (moviendo al doctor y atendiendo pacientes)
QUESTION = 2    # Pantalla de pregunta
PAUSE = 3       # Menú de pausa
LEVEL_COMPLETE = 4  # Pantalla de nivel completado (al llegar al nivel 3)
GAME_OVER = 5   # Pantalla de fin de juego

# COLORES

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_DARK_GRAY = (169, 169, 169)
COLOR_PURPLE = (128, 8, 128)
COLOR_BACKGROUND = (0, 0, 0)  # Color de fondo por defecto

# ESCENARIOS/NIVELES

SCENARIO_1 = (0, 0, 0)  # Fondo negro
SCENARIO_2 = (20, 20, 40)  # Fondo azul oscuro
SCENARIO_3 = (40, 20, 20)  # Fondo rojo oscuro

# SISTEMA DE INTERACCIÓN

DISTANCE_INTERACTION = 50  # Distancia en píxeles para interactuar con pacientes

# SISTEMA DE VIDAS

INITIAL_LIVES = 7  # Vidas iniciales del jugador
MAX_LIVES = 7  # Máximo de vidas (no puede superar este valor)

# Vidas que se pierden al responder incorrectamente según el nivel
LIVES_LOST_GREEN = 1
LIVES_LOST_YELLOW = 2
LIVES_LOST_ORANGE = 3

# Vidas que se ganan al responder correctamente según el nivel
LIVES_GAINED_GREEN = 1
LIVES_GAINED_YELLOW = 2
LIVES_GAINED_ORANGE = 3

# SISTEMA DE TIEMPO PARA PREGUNTAS

# Tiempos en milisegundos para responder preguntas según el nivel
TIME_GREEN = 10000  # 10 segundos
TIME_YELLOW = 15000  # 15 segundos
TIME_ORANGE = 20000  # 20 segundos

# RUTAS DE ARCHIVOS

# Rutas relativas a los assets del juego
PATH_BACKGROUNDS = "assets/image/backgrounds"
PATH_PLAYER = "assets/image/character/player"
PATH_PATIENTS_GREEN = "assets/image/character/patients_level/green"
PATH_PATIENTS_YELLOW = "assets/image/character/patients_level/yellow"
PATH_PATIENTS_ORANGE = "assets/image/character/patients_level/orange"

# Nombres de archivos de fondos
FILE_MENU_BG = "menu_bg.png"
FILE_QUESTION_BG = "question_bg.png"
FILE_GAME_BG = "bg1.png"
