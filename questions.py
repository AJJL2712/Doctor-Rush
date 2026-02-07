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
        "opciones": ["A) Solución salina", "B) Agua fría", "C) Nada"],
        "correcta": 0
    },
    {
        "pregunta": "¿Cuándo deberías consultar a un médico por un resfriado?",
        "opciones": ["A) Si dura más de 10 días", "B) Nunca", "C) Solo si tienes fiebre"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué síntoma indica fiebre?",
        "opciones": ["A) 35°C", "B) 38°C", "C) 30°C"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué ayuda a aliviar la garganta irritada?",
        "opciones": ["A) Agua tibia y miel", "B) Café", "C) Refresco"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué causa los estornudos en alergias?",
        "opciones": ["A) Virus", "B) Polvo/polen", "C) Bacterias"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué es una gripe?",
        "opciones": ["A) Bacteria", "B) Virus", "C) Alergia"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué NO es común en resfriado leve?",
        "opciones": ["A) Tos leve", "B) Congestión", "C) Desmayo"],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué ayuda a recuperarse más rápido?",
        "opciones": ["A) Dormir bien", "B) No comer", "C) Hacer deporte fuerte"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué líquido NO ayuda al cuerpo?",
        "opciones": ["A) Agua", "B) Jugos naturales", "C) Bebidas alcohólicas"],
        "correcta": 2
    },
    {
        "pregunta": "Un síntoma típico de gripe es:",
        "opciones": ["A) Dolor muscular", "B) Dolor de pie", "C) Dolor de oído siempre"],
        "correcta": 0
    },
    {
        "pregunta": "Un síntoma leve NO peligroso es:",
        "opciones": ["A) Moco", "B) Dificultad para respirar", "C) Dolor intenso en el pecho"],
        "correcta": 0
    },
    {
        "pregunta": "Para evitar contagios es clave:",
        "opciones": ["A) Lavarse las manos", "B) No dormir", "C) No comer"],
        "correcta": 0
    },
    {
        "pregunta": "Las alergias suelen afectar:",
        "opciones": ["A) Nariz y ojos", "B) Huesos", "C) Corazón"],
        "correcta": 0
    },
    {
        "pregunta": "Un signo de resfriado inicial es:",
        "opciones": ["A) Estornudos", "B) Dolor de pierna", "C) Mareo severo"],
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
        "opciones": ["A) Seguir moviendo", "B) Reposo, hielo y elevación", "C) Calor inmediato"],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuál es un signo de infección leve?",
        "opciones": ["A) Ninguno", "B) Enrojecimiento e hinchazón", "C) Desmayo"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué ayuda a tratar la gastritis?",
        "opciones": ["A) Picante", "B) Comidas suaves", "C) Comer mucho"],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuánto tarda en sanar un esguince leve?",
        "opciones": ["A) 1 día", "B) 1-2 semanas", "C) 1 mes"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué indica infección grave?",
        "opciones": ["A) Fiebre persistente", "B) Picazón leve", "C) Nada"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué NO hacer ante esguince?",
        "opciones": ["A) Elevar", "B) Forzar", "C) Reposo"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué síntoma alerta en gastritis?",
        "opciones": ["A) Dolor leve", "B) Vómitos con sangre", "C) Solo náuseas"],
        "correcta": 1
    },
    {
        "pregunta": "Un síntoma común de infección es:",
        "opciones": ["A) Hinchazón", "B) Nada", "C) Frío"],
        "correcta": 0
    },
    {
        "pregunta": "Un esguince ocurre cuando:",
        "opciones": ["A) Se rompe el hueso", "B) Se estira el ligamento", "C) No pasa nada"],
        "correcta": 1
    },
    {
        "pregunta": "Gastritis aumenta con:",
        "opciones": ["A) Comida picante y estrés", "B) Agua", "C) Dormir"],
        "correcta": 0
    },
    {
        "pregunta": "Una infección puede mostrar:",
        "opciones": ["A) Pus", "B) Pelo", "C) Hueso roto"],
        "correcta": 0
    },
    {
        "pregunta": "Si una herida sangra mucho debes:",
        "opciones": ["A) Presionar y buscar ayuda", "B) Ignorar", "C) Soplar"],
        "correcta": 0
    },
    {
        "pregunta": "Un síntoma de deshidratación es:",
        "opciones": ["A) Boca seca", "B) Pelo seco", "C) Tos"],
        "correcta": 0
    },
    {
        "pregunta": "La fiebre moderada indica:",
        "opciones": ["A) Infección posible", "B) Frío", "C) Nada"],
        "correcta": 0
    },
    {
        "pregunta": "Dolor abdominal fuerte puede ser:",
        "opciones": ["A) Nada", "B) Algo importante", "C) Solo aire siempre"],
        "correcta": 1
    },
    {
        "pregunta": "Un esguince severo requiere:",
        "opciones": ["A) Médico", "B) Correr", "C) Ignorar"],
        "correcta": 0
    },
    {
        "pregunta": "Una infección mal cuidada puede:",
        "opciones": ["A) Empeorar", "B) Mejorar sola siempre", "C) No pasa nada"],
        "correcta": 0
    },
    {
        "pregunta": "La gastritis duele más en:",
        "opciones": ["A) Estómago", "B) Pierna", "C) Cabeza"],
        "correcta": 0
    },
    {
        "pregunta": "Un síntoma leve manejable es:",
        "opciones": ["A) Dolor suave", "B) Dificultad respiratoria", "C) Desmayo"],
        "correcta": 0
    }
]

# NIVEL NARANJA - Alto (Neumonía, fractura, apendicitis, etc)
questions_orange = [
    {
        "pregunta": "¿Cuál es un síntoma grave de neumonía?",
        "opciones": ["A) Estornudos", "B) Dificultad para respirar y fiebre alta", "C) Dolor leve"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué hacer ante una fractura?",
        "opciones": ["A) Inmovilizar y buscar ayuda", "B) Moverla", "C) Calor"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué indica apendicitis?",
        "opciones": ["A) Dolor suave", "B) Dolor en lado derecho", "C) Dolor en mano"],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué indica emergencia médica?",
        "opciones": ["A) Dolor normal", "B) Dificultad para respirar", "C) Tos"],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuándo buscar atención urgente?",
        "opciones": ["A) Síntomas graves", "B) Siempre", "C) Nunca"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué es peligroso en neumonía?",
        "opciones": ["A) Respiración comprometida", "B) Moco", "C) Estornudos"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué NO hacer en fractura?",
        "opciones": ["A) Inmovilizar", "B) Enderezar", "C) Buscar ayuda"],
        "correcta": 1
    },
    {
        "pregunta": "Apendicitis grave requiere:",
        "opciones": ["A) Cirugía", "B) Té", "C) Reposo"],
        "correcta": 0
    },
    {
        "pregunta": "Dolor en pecho puede indicar:",
        "opciones": ["A) Infarto", "B) Gripe", "C) Alergia siempre"],
        "correcta": 0
    },
    {
        "pregunta": "Dificultad respiratoria es:",
        "opciones": ["A) Emergencia", "B) Normal", "C) Nada"],
        "correcta": 0
    },
    {
        "pregunta": "Un golpe fuerte en cabeza + desmayo es:",
        "opciones": ["A) Peligroso", "B) Normal", "C) Nada"],
        "correcta": 0
    },
    {
        "pregunta": "Una fractura abierta se caracteriza por:",
        "opciones": ["A) Hueso expuesto", "B) Un rasguño", "C) Hinchazón leve"],
        "correcta": 0
    },
    {
        "pregunta": "Un paciente con fiebre muy alta:",
        "opciones": ["A) Requiere atención", "B) No pasa nada", "C) Solo dormir"],
        "correcta": 0
    },
    {
        "pregunta": "Un fuerte golpe en abdomen con dolor intenso puede ser:",
        "opciones": ["A) Internamente grave", "B) Nada", "C) Aire"],
        "correcta": 0
    },
    {
        "pregunta": "Si alguien no respira:",
        "opciones": ["A) Es emergencia", "B) Esperar", "C) Huir"],
        "correcta": 0
    },
    {
        "pregunta": "Una quemadura grave se reconoce por:",
        "opciones": ["A) Ampollas grandes", "B) Solo rojo", "C) Nada"],
        "correcta": 0
    },
    {
        "pregunta": "Neumonía mal tratada puede causar:",
        "opciones": ["A) Fallo respiratorio", "B) Estornudos", "C) Moco"],
        "correcta": 0
    },
    {
        "pregunta": "Un dolor abdominal súbito e intenso:",
        "opciones": ["A) Puede ser cirugía", "B) No importa", "C) Es aire siempre"],
        "correcta": 0
    },
    {
        "pregunta": "Una persona inconsciente necesita:",
        "opciones": ["A) Atención inmediata", "B) Dormir", "C) Ignorar"],
        "correcta": 0
    },
    {
        "pregunta": "Un dolor en el pecho con sudoración y mareo puede ser:",
        "opciones": ["A) Infarto", "B) Resfriado", "C) Hambre"],
        "correcta": 0
    }
]

# Variables globales para rastrear preguntas usadas por sala
_used_questions_by_scenario = {
    0: set(),  # Escenario 0 (green)
    1: set(),  # Escenario 1 (yellow)
    2: set()  # Escenario 2 (orange)
}


def reset_questions_for_scenario(scenario):
    """Resetea las preguntas usadas para un escenario específico."""
    if scenario in _used_questions_by_scenario:
        _used_questions_by_scenario[scenario] = set()


def get_random_question(level, scenario=0):
    """
    Obtiene una pregunta aleatoria del nivel especificado.
    Las opciones se mezclan aleatoriamente y la respuesta correcta se ajusta.
    No repite preguntas en el mismo escenario hasta que todas hayan salido.

    Parámetros:
    - level: Nivel del paciente ("green", "yellow", "orange")
    - scenario: Escenario actual (0, 1, 2) para rastrear preguntas usadas

    Retorna:
    - Diccionario con la pregunta, opciones y respuesta correcta (índice ajustado)
    """
    # Obtener lista de preguntas según el nivel
    if level == "green":
        question_list = questions_green
    elif level == "yellow":
        question_list = questions_yellow
    elif level == "orange":
        question_list = questions_orange
    else:
        question_list = questions_green

    # Obtener preguntas no usadas en este escenario
    used_indices = _used_questions_by_scenario.get(scenario, set())
    available_questions = [i for i in range(len(question_list)) if i not in used_indices]

    # Si todas las preguntas ya se usaron, resetear
    if len(available_questions) == 0:
        _used_questions_by_scenario[scenario] = set()
        available_questions = list(range(len(question_list)))

    # Seleccionar pregunta aleatoria de las disponibles
    question_index = random.choice(available_questions)
    question = question_list[question_index].copy()

    # Marcar como usada
    _used_questions_by_scenario[scenario].add(question_index)

    # Mezclar las opciones aleatoriamente
    original_options = question["opciones"].copy()
    original_correct = question["correcta"]

    # Crear lista de índices para mezclar
    indices = list(range(len(original_options)))
    random.shuffle(indices)

    # Crear nuevas opciones mezcladas
    new_options = [original_options[i] for i in indices]

    # Encontrar el nuevo índice de la respuesta correcta
    new_correct = indices.index(original_correct)

    # Actualizar pregunta
    question["opciones"] = new_options
    question["correcta"] = new_correct

    return question
