import pygame
from constants import (WIDTH_SCREEN, HEIGHT_SCREEN, COLOR_BACKGROUND, COLOR_WHITE, COLOR_BLACK,
                       COLOR_GREEN, COLOR_RED, COLOR_BLUE, COLOR_DARK_GRAY, COLOR_PURPLE, DISTANCE_INTERACTION,
                       LIVES_LOST_GREEN, LIVES_LOST_YELLOW, LIVES_LOST_ORANGE,
                       LIVES_GAINED_GREEN, LIVES_GAINED_YELLOW, LIVES_GAINED_ORANGE,
                       TIME_GREEN, TIME_YELLOW, TIME_ORANGE, INITIAL_LIVES)
from utils import calculate_distance, draw_text_centered
from questions import get_random_question


# FUNCIONES DEL MENÚ

def draw_menu(screen, font, font_small, menu_bg_image=None):
    # Dibujar fondo del menú
    if menu_bg_image:
        screen.blit(menu_bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)
    draw_text_centered(screen, "DOCTOR RUSH", font, COLOR_WHITE, 250)
    draw_text_centered(screen, "Presiona ESPACIO para jugar", font_small, COLOR_WHITE, 500)
    draw_text_centered(screen, "Presiona ESC para salir", font_small, COLOR_WHITE, 550)


def handle_menu_events(event, game_state, player, score, patients_cured, lives, current_scenario,
                       create_patients_func, animations_green, animations_yellow, animations_orange, player_animation):
    """
    Maneja los eventos del teclado en el menú.

    Retorna:
    - Tupla con (nuevo_estado, score, patients_cured, lives, scenario, pacientes, niveles, lista_curados)
    """
    from constants import PLAYING
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            game_state = PLAYING
            # Resetear posición del jugador
            player.shape.center = (50, 50)
            score = 0
            patients_cured = 0
            lives = 7  # INITIAL_LIVES
            current_scenario = 0
            # Recrear pacientes para el nivel 0
            list_patients, patient_levels = create_patients_func(0, animations_green, animations_yellow,
                                                                 animations_orange, player_animation)
            patients_cured_list = [False] * len(list_patients)
            return game_state, score, patients_cured, lives, current_scenario, list_patients, patient_levels, patients_cured_list
        elif event.key == pygame.K_ESCAPE:
            return "QUIT", score, patients_cured, lives, current_scenario, None, None, None
    return game_state, score, patients_cured, lives, current_scenario, None, None, None


# FUNCIONES DE DIBUJADO EN EL JUEGO

def draw_patients(screen, list_patients, patient_levels, patients_cured_list, player, font_small):
    """
    Dibuja los pacientes en la pantalla de juego con sus distintivos de nivel.
    También muestra el mensaje de interacción cuando el jugador está cerca.
    """
    for i, ene in enumerate(list_patients):
        if not patients_cured_list[i]:
            ene.draw(screen)

            # Dibujar distintivo visual (punto) sobre el paciente según su nivel
            if i < len(patient_levels):
                dot_color = COLOR_WHITE
                dot_size = 8
                if patient_levels[i] == "green":
                    dot_color = COLOR_GREEN
                elif patient_levels[i] == "yellow":
                    dot_color = (255, 255, 0)  # Amarillo
                elif patient_levels[i] == "orange":
                    dot_color = (255, 165, 0)  # Naranja

                # Dibujar punto encima del paciente
                dot_x = ene.shape.centerx
                dot_y = ene.shape.y - 15
                pygame.draw.circle(screen, dot_color, (dot_x, dot_y), dot_size)

            # Verificar si el jugador está cerca del paciente
            distance = calculate_distance(
                player.shape.centerx, player.shape.centery,
                ene.shape.centerx, ene.shape.centery
            )

            if distance < DISTANCE_INTERACTION:
                # Mostrar mensaje de interacción con el nivel del paciente
                level_name = ""
                level_color = COLOR_WHITE
                if i < len(patient_levels):
                    if patient_levels[i] == "green":
                        level_name = " (Verde - Bajo)"
                        level_color = COLOR_GREEN
                    elif patient_levels[i] == "yellow":
                        level_name = " (Amarillo - Medio)"
                        level_color = (255, 255, 0)  # Amarillo
                    elif patient_levels[i] == "orange":
                        level_name = " (Naranja - Alto)"
                        level_color = (255, 165, 0)  # Naranja
                text_interaction = font_small.render(f"Presiona E para atender{level_name}", True, level_color)
                screen.blit(text_interaction, (ene.shape.x, ene.shape.y - 50))


# FUNCIONES DE PREGUNTAS

def start_question(patient_level, patient_index, question_start_time):
    """
    Inicia una nueva pregunta para un paciente.

    Retorna:
    - Tupla con (pregunta, tiempo_limite)
    """
    current_question = get_random_question(patient_level)
    question_time_limit = 0
    if patient_level == "green":
        question_time_limit = TIME_GREEN
    elif patient_level == "yellow":
        question_time_limit = TIME_YELLOW
    elif patient_level == "orange":
        question_time_limit = TIME_ORANGE

    return current_question, question_time_limit


def check_answer(selected, correct_answer, patient_level, score, patients_cured, lives):
    """
    Verifica si la respuesta es correcta y actualiza vidas/puntuación.
    Retorna:
    - Tupla con (es_correcta, nuevo_score, nuevos_curados, nuevas_vidas)
    """
    if selected == correct_answer:
        # Respuesta correcta
        score += 10
        patients_cured += 1
        # Agregar vidas según el nivel del paciente
        if patient_level == "green":
            lives += LIVES_GAINED_GREEN
        elif patient_level == "yellow":
            lives += LIVES_GAINED_YELLOW
        elif patient_level == "orange":
            lives += LIVES_GAINED_ORANGE
        # No superar el máximo de vidas
        lives = min(lives, INITIAL_LIVES)
        return True, score, patients_cured, lives
    else:
        # Respuesta incorrecta
        # Restar vidas según el nivel del paciente
        if patient_level == "green":
            lives -= LIVES_LOST_GREEN
        elif patient_level == "yellow":
            lives -= LIVES_LOST_YELLOW
        elif patient_level == "orange":
            lives -= LIVES_LOST_ORANGE
        return False, score, patients_cured, lives


def check_time_up(question_start_time, question_time_limit, patient_level, lives):
    """
    Verifica si se agotó el tiempo para responder la pregunta.

    Retorna:
    - Tupla con (tiempo_agotado, nuevas_vidas)
    """
    elapsed_time = pygame.time.get_ticks() - question_start_time
    if elapsed_time >= question_time_limit:
        # Restar vidas según el nivel del paciente
        if patient_level == "green":
            lives -= LIVES_LOST_GREEN
        elif patient_level == "yellow":
            lives -= LIVES_LOST_YELLOW
        elif patient_level == "orange":
            lives -= LIVES_LOST_ORANGE
        return True, lives
    return False, lives


# Función para dibujar la pantalla de pregunta
def draw_question_screen(screen, font, font_small, current_question, patient_level,
                         question_start_time, question_time_limit, question_result, question_bg=None):
    """
    Dibuja la pantalla de pregunta con el fondo, cuadro centrado y todas las opciones.
    """
    from ui_config import (QUESTION_BOX_X, QUESTION_BOX_Y, QUESTION_BOX_WIDTH, QUESTION_BOX_HEIGHT,
                           QUESTION_BOX_COLOR, QUESTION_BOX_ALPHA, QUESTION_BOX_BORDER_OUTER,
                           QUESTION_BOX_BORDER_INNER, QUESTION_BOX_BORDER_WIDTH, QUESTION_BOX_BORDER_INNER_WIDTH,
                           QUESTION_BOX_MARGIN, QUESTION_TITLE_Y, QUESTION_TEXT_Y_OFFSET,
                           QUESTION_LINE_SPACING, QUESTION_OPTION_SPACING, QUESTION_TIME_Y_OFFSET,
                           QUESTION_INSTRUCTION_Y_OFFSET, TIME_COLOR_GREEN, TIME_COLOR_ORANGE, TIME_COLOR_RED,
                           TIME_WARNING_THRESHOLD, TIME_ORANGE_THRESHOLD_DIVISOR)

    # Dibujar fondo de la pantalla
    if question_bg:
        try:
            screen.blit(question_bg, (0, 0))
        except Exception as e:
            print(f"Error al dibujar fondo: {e}")
            screen.fill(COLOR_BACKGROUND)
    else:
        screen.fill(COLOR_BACKGROUND)

    if question_result is None:
        # Verificar si se agotó el tiempo
        elapsed_time = pygame.time.get_ticks() - question_start_time
        time_remaining = max(0, question_time_limit - elapsed_time)
        time_remaining_seconds = time_remaining / 1000.0

        # Mostrar pregunta con nivel del paciente
        level_text = ""
        if patient_level == "green":
            level_text = " (Nivel Verde - Bajo)"
        elif patient_level == "yellow":
            level_text = " (Nivel Amarillo - Medio)"
        elif patient_level == "orange":
            level_text = " (Nivel Naranja - Alto)"

        # Título centrado arriba
        draw_text_centered(screen, f"ATENDIENDO PACIENTE{level_text}", font, COLOR_WHITE, QUESTION_TITLE_Y)

        # Usar configuraciones del cuadro desde ui_config
        box_x = QUESTION_BOX_X
        box_y = QUESTION_BOX_Y
        box_width = QUESTION_BOX_WIDTH
        box_height = QUESTION_BOX_HEIGHT
        box_center_x = box_x + box_width // 2

        # Dibujar rectángulo de fondo (semi-transparente) con mejor diseño
        box_surface = pygame.Surface((box_width, box_height))
        box_surface.set_alpha(QUESTION_BOX_ALPHA)
        box_surface.fill(QUESTION_BOX_COLOR)
        screen.blit(box_surface, (box_x, box_y))

        # Borde del cuadro más visible
        pygame.draw.rect(screen, QUESTION_BOX_BORDER_OUTER, (box_x, box_y, box_width, box_height),
                         QUESTION_BOX_BORDER_WIDTH)
        # Borde interno más sutil
        pygame.draw.rect(screen, QUESTION_BOX_BORDER_INNER,
                         (box_x + 2, box_y + 2, box_width - 4, box_height - 4), QUESTION_BOX_BORDER_INNER_WIDTH)

        # Pregunta centrada dentro del cuadro (con ajuste a dos líneas si es necesario)
        pregunta_y = box_y + QUESTION_TEXT_Y_OFFSET
        max_width = box_width - QUESTION_BOX_MARGIN * 2  # Ancho máximo con márgenes

        # Dividir la pregunta en líneas si es muy larga
        pregunta_texto = current_question["pregunta"]
        palabras = pregunta_texto.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            test_linea = linea_actual + (" " if linea_actual else "") + palabra
            test_surface = font.render(test_linea, True, COLOR_WHITE)
            if test_surface.get_width() <= max_width:
                linea_actual = test_linea
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        # Si solo hay una línea, centrarla; si hay dos, mostrarlas
        if len(lineas) == 1:
            text_surface = font.render(lineas[0], True, COLOR_WHITE)
            text_rect = text_surface.get_rect(center=(box_center_x, pregunta_y))
            screen.blit(text_surface, text_rect)
            pregunta_final_y = pregunta_y + 40
        else:
            # Mostrar hasta 2 líneas
            for i, linea in enumerate(lineas[:2]):
                text_surface = font.render(linea, True, COLOR_WHITE)
                text_rect = text_surface.get_rect(center=(box_center_x, pregunta_y + i * QUESTION_LINE_SPACING))
                screen.blit(text_surface, text_rect)
            pregunta_final_y = pregunta_y + len(lineas[:2]) * QUESTION_LINE_SPACING + 10

        # Opciones centradas dentro del cuadro
        y_offset = pregunta_final_y + 20
        for i, opcion in enumerate(current_question["opciones"]):
            option_text = font_small.render(opcion, True, COLOR_WHITE)
            option_rect = option_text.get_rect(center=(box_center_x, y_offset + i * QUESTION_OPTION_SPACING))
            screen.blit(option_text, option_rect)

        # Tiempo restante abajo de las opciones, casi al final del cuadro
        time_color = TIME_COLOR_GREEN
        if time_remaining_seconds < TIME_WARNING_THRESHOLD:
            time_color = TIME_COLOR_RED
        elif time_remaining_seconds < question_time_limit / TIME_ORANGE_THRESHOLD_DIVISOR:
            time_color = TIME_COLOR_ORANGE

        tiempo_y = box_y + box_height - QUESTION_TIME_Y_OFFSET
        time_text = font_small.render(f"Tiempo restante: {time_remaining_seconds:.1f}s", True, time_color)
        time_rect = time_text.get_rect(center=(box_center_x, tiempo_y))
        screen.blit(time_text, time_rect)

        # Instrucción abajo del cuadro
        draw_text_centered(screen, "Presiona 1, 2 o 3 para responder", font_small, COLOR_GREEN,
                           box_y + box_height + QUESTION_INSTRUCTION_Y_OFFSET)
    else:
        # Dibujar fondo para el cuadro de resultado (centrado)
        from ui_config import RESULT_BOX_X, RESULT_BOX_Y, RESULT_BOX_WIDTH, RESULT_BOX_HEIGHT
        box_x = RESULT_BOX_X
        box_y = RESULT_BOX_Y
        box_width = RESULT_BOX_WIDTH
        box_height = RESULT_BOX_HEIGHT
        box_center_x = box_x + box_width // 2

        # Dibujar rectángulo de fondo (semi-transparente) con mejor diseño
        box_surface = pygame.Surface((box_width, box_height))
        box_surface.set_alpha(QUESTION_BOX_ALPHA)
        box_surface.fill(QUESTION_BOX_COLOR)
        screen.blit(box_surface, (box_x, box_y))

        # Borde del cuadro más visible
        pygame.draw.rect(screen, QUESTION_BOX_BORDER_OUTER, (box_x, box_y, box_width, box_height),
                         QUESTION_BOX_BORDER_WIDTH)
        pygame.draw.rect(screen, QUESTION_BOX_BORDER_INNER, (box_x + 2, box_y + 2, box_width - 4, box_height - 4),
                         QUESTION_BOX_BORDER_INNER_WIDTH)

        # Mostrar resultado centrado dentro del cuadro
        result_y = box_y + 40
        if question_result:
            result_text = font.render("¡CORRECTO!", True, COLOR_GREEN)
            result_rect = result_text.get_rect(center=(box_center_x, result_y))
            screen.blit(result_text, result_rect)

            points_y = result_y + 50
            points_text = font_small.render(f"+10 puntos", True, COLOR_GREEN)
            points_rect = points_text.get_rect(center=(box_center_x, points_y))
            screen.blit(points_text, points_rect)

            lives_gained = 0
            if patient_level == "green":
                lives_gained = LIVES_GAINED_GREEN
            elif patient_level == "yellow":
                lives_gained = LIVES_GAINED_YELLOW
            elif patient_level == "orange":
                lives_gained = LIVES_GAINED_ORANGE

            lives_y = points_y + 35
            lives_text = font_small.render(f"+{lives_gained} vidas", True, COLOR_GREEN)
            lives_rect = lives_text.get_rect(center=(box_center_x, lives_y))
            screen.blit(lives_text, lives_rect)
        else:
            # Verificar si fue por tiempo agotado o respuesta incorrecta
            elapsed_time = pygame.time.get_ticks() - question_start_time
            if elapsed_time >= question_time_limit:
                result_text = font.render("¡TIEMPO AGOTADO!", True, COLOR_RED)
            else:
                result_text = font.render("INCORRECTO", True, COLOR_RED)

            result_rect = result_text.get_rect(center=(box_center_x, result_y))
            screen.blit(result_text, result_rect)

            if elapsed_time < question_time_limit:
                answer_y = result_y + 50
                answer_text = font_small.render(
                    "La respuesta correcta era la opción " + str(current_question["correcta"] + 1), True, COLOR_WHITE)
                answer_rect = answer_text.get_rect(center=(box_center_x, answer_y))
                screen.blit(answer_text, answer_rect)

            lives_lost = 0
            if patient_level == "green":
                lives_lost = LIVES_LOST_GREEN
            elif patient_level == "yellow":
                lives_lost = LIVES_LOST_YELLOW
            elif patient_level == "orange":
                lives_lost = LIVES_LOST_ORANGE

            lives_y = result_y + 100 if elapsed_time < question_time_limit else result_y + 50
            lives_text = font_small.render(f"-{lives_lost} vidas", True, COLOR_RED)
            lives_rect = lives_text.get_rect(center=(box_center_x, lives_y))
            screen.blit(lives_text, lives_rect)

        # Instrucción abajo del cuadro
        draw_text_centered(screen, "Presiona ESPACIO para continuar", font_small, COLOR_WHITE, box_y + box_height + 30)


# FUNCIONES DE PAUSA Y FIN DE JUEGO
def draw_pause(screen, font, font_small):
    """
    Dibuja la pantalla de PAUSA.

    Muestra que el juego está en pausa y las opciones disponibles.
    """
    # Fondo semi-transparente sobre el juego
    overlay = pygame.Surface((WIDTH_SCREEN, HEIGHT_SCREEN))
    overlay.set_alpha(180)
    overlay.fill(COLOR_BACKGROUND)
    screen.blit(overlay, (0, 0))

    # Título de pausa
    draw_text_centered(screen, "PAUSA", font, COLOR_WHITE, 200)

    # Mensajes de ayuda
    draw_text_centered(screen, "Presiona ESPACIO para seguir jugando", font_small, COLOR_GREEN, 280)
    draw_text_centered(screen, "Presiona ESC para salir al menú", font_small, COLOR_WHITE, 320)


def draw_level_complete(screen, font, font_small, score, patients_cured):
    """
    Dibuja la pantalla cuando se completa el nivel 3.

    Pregunta al jugador si quiere continuar o terminar la partida.
    """
    screen.fill(COLOR_BACKGROUND)
    draw_text_centered(screen, "¡NIVEL 3 COMPLETADO!", font, COLOR_GREEN, 150)
    draw_text_centered(screen, f"Puntuación: {score}", font_small, COLOR_WHITE, 220)
    draw_text_centered(screen, f"Pacientes curados: {patients_cured}", font_small, COLOR_WHITE, 260)
    draw_text_centered(screen, "¿Qué deseas hacer?", font, COLOR_WHITE, 320)
    draw_text_centered(screen, "Presiona ESPACIO para seguir jugando", font_small, COLOR_GREEN, 380)
    draw_text_centered(screen, "Presiona ESC para terminar y volver al menú", font_small, COLOR_WHITE, 420)


# Función para dibujar la pantalla de Game Over
def draw_game_over(screen, font, font_small, score, patients_cured):
    """
    Dibuja la pantalla de Game Over cuando el jugador se queda sin vidas.
    """
    screen.fill(COLOR_BACKGROUND)
    draw_text_centered(screen, "GAME OVER", font, COLOR_RED, 200)
    draw_text_centered(screen, f"Puntuación final: {score}", font_small, COLOR_WHITE, 280)
    draw_text_centered(screen, f"Pacientes curados: {patients_cured}", font_small, COLOR_WHITE, 320)
    draw_text_centered(screen, "Presiona ESPACIO para volver al menú", font_small, COLOR_GREEN, 400)

