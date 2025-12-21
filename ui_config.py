from constants import WIDTH_SCREEN, HEIGHT_SCREEN


# CONFIGURACIÓN DE FUENTES

FONT_SIZE_LARGE = 40  # Tamaño de fuente grande (títulos)
FONT_SIZE_SMALL = 30  # Tamaño de fuente pequeña (texto normal)
FONT_SIZE_TINY = 20   # Tamaño de fuente muy pequeña (texto secundario)


# CONFIGURACIÓN DEL CUADRO DE PREGUNTA

# Dimensiones del cuadro de pregunta (centrado)
QUESTION_BOX_WIDTH = 600
QUESTION_BOX_HEIGHT = 400
QUESTION_BOX_X = (WIDTH_SCREEN - QUESTION_BOX_WIDTH) // 2  # Centrado horizontal
QUESTION_BOX_Y = 100  # Posición vertical desde arriba

# Colores del cuadro de pregunta
QUESTION_BOX_COLOR = (20, 20, 30)  # Color de fondo (azul oscuro)
QUESTION_BOX_ALPHA = 220  # Transparencia (0-255, más alto = más opaco)
QUESTION_BOX_BORDER_OUTER = (150, 150, 150)  # Color del borde exterior
QUESTION_BOX_BORDER_INNER = (60, 60, 80)  # Color del borde interior
QUESTION_BOX_BORDER_WIDTH = 4  # Grosor del borde exterior
QUESTION_BOX_BORDER_INNER_WIDTH = 2  # Grosor del borde interior

# Márgenes dentro del cuadro
QUESTION_BOX_MARGIN = 40  # Márgenes laterales para el texto


# POSICIONES DE ELEMENTOS EN PANTALLA DE PREGUNTA

# Posición del título "ATENDIENDO PACIENTE"
QUESTION_TITLE_Y = 40

# Posición inicial de la pregunta dentro del cuadro
QUESTION_TEXT_Y_OFFSET = 30  # Desde el borde superior del cuadro

# Espaciado entre líneas de la pregunta
QUESTION_LINE_SPACING = 35

# Espaciado entre opciones de respuesta
QUESTION_OPTION_SPACING = 50

# Posición del tiempo restante (desde el fondo del cuadro)
QUESTION_TIME_Y_OFFSET = 40  # Casi al final del cuadro

# Posición de la instrucción (debajo del cuadro)
QUESTION_INSTRUCTION_Y_OFFSET = 30


# CONFIGURACIÓN DEL CUADRO DE RESULTADO

RESULT_BOX_WIDTH = 500
RESULT_BOX_HEIGHT = 200
RESULT_BOX_X = (WIDTH_SCREEN - RESULT_BOX_WIDTH) // 2
RESULT_BOX_Y = 200


# CONFIGURACIÓN DE DISTINTIVOS DE PACIENTES

PATIENT_DOT_SIZE = 8  # Tamaño del punto que indica el nivel
PATIENT_DOT_Y_OFFSET = 15  # Distancia desde el paciente hacia arriba

# Colores de los distintivos según nivel
PATIENT_DOT_COLOR_GREEN = (0, 255, 0)
PATIENT_DOT_COLOR_YELLOW = (255, 255, 0)
PATIENT_DOT_COLOR_ORANGE = (255, 165, 0)


# CONFIGURACIÓN DE MENSAJES DE INTERACCIÓN

INTERACTION_MESSAGE_Y_OFFSET = 50  # Distancia desde el paciente hacia arriba


# CONFIGURACIÓN DE COLORES DE TIEMPO

# Colores del temporizador según el tiempo restante
TIME_COLOR_GREEN = (0, 255, 0)  # Verde cuando hay tiempo suficiente
TIME_COLOR_ORANGE = (255, 165, 0)  # Naranja cuando queda poco tiempo
TIME_COLOR_RED = (255, 0, 0)  # Rojo cuando queda muy poco tiempo
TIME_WARNING_THRESHOLD = 3  # Segundos para cambiar a rojo
TIME_ORANGE_THRESHOLD_DIVISOR = 2000  # Divisor para calcular umbral naranja

