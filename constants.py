# CONFIGURACIÓN DE VENTANA
BASE_WIDTH = 800
BASE_HEIGHT = 600

# Resolución actual de la ventana (puede cambiar si es redimensionable)
WIDTH_SCREEN = 800  # Mantener para compatibilidad, pero usar BASE_WIDTH para lógica
HEIGHT_SCREEN = 600  # Mantener para compatibilidad, pero usar BASE_HEIGHT para lógica

FPS = 60  # Frame Rate (cuadros por segundo)

# CONFIGURACIÓN DEL JUGADOR
HEIGHT_CHARACTER = 27
WIDTH_CHARACTER = 27
COLOR_CHARACTER = (255, 255, 0)  # Color amarillo
SPEED_CHARACTER = 5  # Velocidad de movimiento
SCALE_CHARACTER = 3  # Escala de la imagen del jugador

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
INITIAL_SCREEN = -1  # Pantalla inicial (input de nombre)
MENU = 0        # Menú principal
PLAYING = 1     # Jugando (moviendo al doctor y atendiendo pacientes)
QUESTION = 2    # Pantalla de pregunta
PAUSE = 3       # Menú de pausa
LEVEL_COMPLETE = 4  # Pantalla de nivel completado (al llegar al nivel 3)
GAME_OVER = 5   # Pantalla de fin de juego
CLINICAL_CASE = 6  # Modo Caso Clínico
CLINICAL_CASE_PAUSE = 7  # Pausa en modo Caso Clínico
CLINICAL_CASE_VICTORY = 8  # Pantalla de victoria en Caso Clínico
STATISTICS = 9  # Pantalla de estadísticas

# COLORES

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_DARK_GRAY = (169, 169, 169)
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
FILE_INITIAL_BG = "initial_bg.png"  # Fondo de pantalla inicial
FILE_MENU_BG = "menu_bg.png"
FILE_QUESTION_BG = "question_bg.png"
FILE_GAME_BG = "bg1.png"
FILE_CLINICAL_CASE_BG = "clinical_case_bg.png"  # Background para el modo Caso Clínico
FILE_STATISTICS_BG = "statistics_bg.png"  # Fondo de estadísticas

# Sonido de fondo global
SOUND_GLOBAL_BG = "global_bg.mp3"  # Sonido de fondo que se reproduce siempre

# CONFIGURACIÓN DE VOLÚMENES DE SONIDO
# Todos los volúmenes están en rango de 0.0 a 1.0
SOUND_VOLUME_GLOBAL_BG = 0.2  # Volumen del sonido de fondo global
SOUND_VOLUME_MENU_NAVIGATE = 0.7  # Volumen del sonido de navegación del menú
SOUND_VOLUME_MENU_SELECT = 0.7  # Volumen del sonido de selección del menú
SOUND_VOLUME_DOCTOR_RUSH_BG = 0.5  # Volumen de la música de fondo de Doctor Rush
SOUND_VOLUME_ANSWER_CORRECT = 0.7  # Volumen del sonido de respuesta correcta
SOUND_VOLUME_ANSWER_INCORRECT = 0.7  # Volumen del sonido de respuesta incorrecta
SOUND_VOLUME_LEVEL_COMPLETE = 0.7  # Volumen del sonido de nivel completado
SOUND_VOLUME_CLINICAL_CASE_BG = 0.5  # Volumen de la música de fondo de Caso Clínico
SOUND_VOLUME_CLINICAL_SELECT = 0.7  # Volumen del sonido de selección en caso clínico
SOUND_VOLUME_CLINICAL_CASE_COMPLETE = 0.7  # Volumen del sonido de caso completado
SOUND_VOLUME_DIAGNOSIS_CORRECT = 0.7  # Volumen del sonido de diagnóstico correcto
SOUND_VOLUME_DIAGNOSIS_INCORRECT = 0.7  # Volumen del sonido de diagnóstico incorrecto

# CONFIGURACIÓN DE FUENTES PARA CASO CLÍNICO
# Tamaños de fuente (puedes ajustarlos según necesites)
CLINICAL_CASE_FONT_TITLE = 32  # Tamaño de fuente para títulos
CLINICAL_CASE_FONT_NORMAL = 22  # Tamaño de fuente para texto normal
CLINICAL_CASE_FONT_SMALL = 18  # Tamaño de fuente para texto pequeño
CLINICAL_CASE_FONT_TINY = 14  # Tamaño de fuente para texto muy pequeño

# Colores de texto para Caso Clínico (puedes cambiarlos aquí)
CLINICAL_CASE_COLOR_TITLE = COLOR_WHITE  # Color para títulos
CLINICAL_CASE_COLOR_TEXT = COLOR_WHITE  # Color para texto normal
CLINICAL_CASE_COLOR_SELECTED = COLOR_GREEN  # Color para opción seleccionada
CLINICAL_CASE_COLOR_SECTION = COLOR_RED  # Color para secciones (Antecedentes, Síntomas, etc.)
CLINICAL_CASE_COLOR_INSTRUCTION = COLOR_WHITE  # Color para instrucciones

# Espaciado para Caso Clínico
CLINICAL_CASE_LINE_HEIGHT = 20  # Altura entre líneas de texto
CLINICAL_CASE_SECTION_SPACING = 30  # Espacio entre secciones
CLINICAL_CASE_OPTION_SPACING = 45  # Espacio entre opciones en menús

# Sistema de puntos para Caso Clínico
CLINICAL_CASE_POINTS_EASY = 2  # Puntos por caso fácil
CLINICAL_CASE_POINTS_MEDIUM = 3  # Puntos por caso intermedio
CLINICAL_CASE_POINTS_HARD = 5  # Puntos por caso difícil
CLINICAL_CASE_POINTS_TO_WIN = 15  # Puntos necesarios para ganar
