import random

# Preguntas médicas básicas para el juego organizadas por nivel

# NIVEL VERDE - Bajo (Resfriado, dolor de cabeza, alergia, etc)
questions_green = [
    {
        "pregunta": "¿Cuál es el síntoma más común de un resfriado?",
        "opciones": ["A) Fiebre alta", "B) Congestión nasal", "C) Dolor de pecho"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué ayuda a aliviar un dolor de cabeza leve?",
        "opciones": ["A) Descansar y tomar agua", "B) Beber alcohol", "C) Hacer ejercicio intenso"],
        "correcta": 0
    },
    {
        "pregunta": "¿Cuál es un síntoma común de alergia?",
        "opciones": ["A) Estornudos y picazón", "B) Fiebre", "C) Dolor de huesos"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué se recomienda para un resfriado común?",
        "opciones": ["A) Antibióticos siempre", "B) Descanso y líquidos", "C) No hacer nada"],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuántos días suele durar un resfriado común?",
        "opciones": ["A) 1-2 días", "B) 7-10 días", "C) 1 mes"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué vitamina ayuda a prevenir resfriados?",
        "opciones": ["A) Vitamina A", "B) Vitamina K", "C) Vitamina C"],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué es mejor para aliviar la congestión nasal?",
        "opciones": ["A) Agua salada o solución salina", "B) Agua fría", "C) No hacer nada"],
        "correcta": 0
    },
    {
        "pregunta": "¿Cuándo deberías consultar a un médico por un resfriado?",
        "opciones": ["A) Si dura más de 10 días", "B) Nunca", "C) Solo si tienes fiebre"],
        "correcta": 0
    }
]

# NIVEL AMARILLO - Medio (Gastritis, infección leve, esguince, etc)
questions_yellow = [
    {
        "pregunta": "¿Cuál es un síntoma común de gastritis?",
        "opciones": ["A) Dolor abdominal y náuseas", "B) Dolor de cabeza", "C) Dolor de espalda"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué se debe hacer ante un esguince leve?",
        "opciones": ["A) Seguir moviendo la articulación", "B) Reposo, hielo y elevación",
                     "C) Aplicar calor inmediato"],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuál es un signo de infección leve?",
        "opciones": ["A) Sin síntomas", "B) Enrojecimiento e hinchazón local", "C) Pérdida de conciencia"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué ayuda a tratar la gastritis?",
        "opciones": ["A) Comidas picantes", "B) Comidas suaves y evitar irritantes", "C) Comer mucho"],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuánto tiempo tarda en sanar un esguince leve?",
        "opciones": ["A) 1 día", "B) 1-2 semanas", "C) 1 mes"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué indica una infección que requiere atención médica?",
        "opciones": ["A) Fiebre persistente o empeoramiento", "B) Cualquier síntoma", "C) Solo si duele mucho"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué NO debes hacer con un esguince?",
        "opciones": ["A) Aplicar hielo", "B) Mover la articulación forzadamente", "C) Elevar la extremidad"],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuál es un síntoma de gastritis que requiere atención?",
        "opciones": ["A) Dolor leve ocasional", "B) Dolor intenso o vómitos con sangre", "C) Solo náuseas"],
        "correcta": 1
    }
]

# NIVEL NARANJA - Alto (Neumonía, fractura, apendicitis, etc)
questions_orange = [
    {
        "pregunta": "¿Cuál es un síntoma grave de neumonía?",
        "opciones": ["A) Estornudos", "B) Dificultad para respirar y fiebre alta", "C) Dolor de cabeza leve"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué se debe hacer ante una fractura?",
        "opciones": ["A) Inmovilizar y buscar atención médica", "B) Mover la extremidad", "C) Aplicar calor"],
        "correcta": 0
    },
    {
        "pregunta": "¿Cuál es un síntoma de apendicitis?",
        "opciones": ["A) Dolor leve en el estómago", "B) Dolor intenso en el lado derecho del abdomen",
                     "C) Dolor de cabeza"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué indica una emergencia médica?",
        "opciones": ["A) Cualquier dolor", "B) Dificultad para respirar o dolor intenso", "C) Solo si hay sangre"],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuándo se debe buscar atención médica urgente?",
        "opciones": ["A) En síntomas graves o que empeoran", "B) Nunca", "C) Solo por la noche"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué es peligroso en una neumonía no tratada?",
        "opciones": ["A) Complicaciones respiratorias graves", "B) Nada", "C) Solo tos"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué NO debes hacer con una fractura?",
        "opciones": ["A) Inmovilizar", "B) Intentar enderezar el hueso", "C) Buscar ayuda médica"],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuál es un signo de apendicitis que requiere cirugía urgente?",
        "opciones": ["A) Dolor leve", "B) Dolor intenso con fiebre y náuseas", "C) Solo náuseas"],
        "correcta": 1
    }
]


# Función para obtener una pregunta aleatoria de un nivel específico
def get_random_question(level):
    """
    Obtiene una pregunta aleatoria del nivel especificado.
    Las opciones siempre se mantienen en orden A, B, C.

    Parámetros:
    - level: Nivel del paciente ("green", "yellow", "orange")

    Retorna:
    - Diccionario con la pregunta, opciones y respuesta correcta
    """
    if level == "green":
        question = random.choice(questions_green)
    elif level == "yellow":
        question = random.choice(questions_yellow)
    elif level == "orange":
        question = random.choice(questions_orange)
    else:
        question = random.choice(questions_green)

    # Retornar la pregunta sin mezclar las opciones
    # Las opciones siempre aparecerán en orden A, B, C
    return question.copy()
