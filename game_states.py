import pygame
from constants import (WIDTH_SCREEN, HEIGHT_SCREEN, BASE_WIDTH, BASE_HEIGHT, COLOR_BACKGROUND, COLOR_WHITE, COLOR_BLACK,
                       COLOR_GREEN, COLOR_RED, COLOR_BLUE, COLOR_DARK_GRAY, DISTANCE_INTERACTION,
                       LIVES_LOST_GREEN, LIVES_LOST_YELLOW, LIVES_LOST_ORANGE,
                       LIVES_GAINED_GREEN, LIVES_GAINED_YELLOW, LIVES_GAINED_ORANGE,
                       TIME_GREEN, TIME_YELLOW, TIME_ORANGE, INITIAL_LIVES, INITIAL_SCREEN)
from utils import calculate_distance, draw_text_centered
from questions import get_random_question


# FUNCIONES DEL MENÚ

def draw_menu(screen, font, font_small, menu_bg_image=None, selected_option=0):
    """
    Dibuja el menú principal con las opciones disponibles.

    Args:
        selected_option: Índice de la opción seleccionada (0, 1, 2)
    """
    # Dibujar fondo del menú
    if menu_bg_image:
        screen.blit(menu_bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)

    # Título del juego
    draw_text_centered(screen, "DOCTOR RUSH", font, COLOR_WHITE, 200)

    # Opciones del menú
    menu_options = [
        "1. Doctor Rush",
        "2. Caso Clínico",
        "3. Estadísticas",
        "4. Salir"
    ]

    # Posiciones Y para cada opción
    start_y = 320
    option_spacing = 55

    for i, option in enumerate(menu_options):
        y_pos = start_y + i * option_spacing

        # Color según si está seleccionada o no
        if i == selected_option:
            # Opción seleccionada: color verde y con indicador ">"
            option_text = f"> {option} <"
            color = COLOR_GREEN
        else:
            # Opción no seleccionada: color blanco
            option_text = option
            color = COLOR_WHITE

        draw_text_centered(screen, option_text, font_small, color, y_pos)

    # Instrucciones de navegación
    draw_text_centered(screen, "W: Subir | S: Bajar | ESPACIO: Seleccionar", font_small, COLOR_WHITE, 550)


def handle_menu_events(event, game_state, player, score, patients_cured, lives, current_scenario,
                       create_patients_func, animations_green, animations_yellow, animations_orange, player_animation,
                       selected_option=0):
    """
    Maneja los eventos del teclado en el menú.

    Args:
        selected_option: Índice de la opción seleccionada actualmente

    Retorna:
    - Tupla con (nuevo_estado, score, patients_cured, lives, scenario, pacientes, niveles, lista_curados, nueva_opcion_seleccionada)
    """
    from constants import PLAYING, STATISTICS

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            # Subir en el menú
            selected_option = (selected_option - 1) % 4
            return game_state, score, patients_cured, lives, current_scenario, None, None, None, selected_option
        elif event.key == pygame.K_s:
            # Bajar en el menú
            selected_option = (selected_option + 1) % 4
            return game_state, score, patients_cured, lives, current_scenario, None, None, None, selected_option
        elif event.key == pygame.K_SPACE:
            # Seleccionar opción
            if selected_option == 0:
                # Doctor Rush - Iniciar juego normal
                game_state = PLAYING
                # Resetear posición del jugador
                player.shape.center = (BASE_WIDTH // 2, BASE_HEIGHT // 2)
                score = 0
                patients_cured = 0
                lives = INITIAL_LIVES
                current_scenario = 0
                # Recrear pacientes para el nivel 0
                list_patients, patient_levels = create_patients_func(0, animations_green, animations_yellow,
                                                                     animations_orange, player_animation)
                patients_cured_list = [False] * len(list_patients)
                return game_state, score, patients_cured, lives, current_scenario, list_patients, patient_levels, patients_cured_list, selected_option
            elif selected_option == 1:
                # Caso Clínico - Iniciar modo de casos clínicos
                from constants import CLINICAL_CASE
                from clinical_cases import reset_case_progression
                reset_case_progression()  # Resetear progresión de casos
                game_state = CLINICAL_CASE
                return game_state, score, patients_cured, lives, current_scenario, None, None, None, selected_option
            elif selected_option == 2:
                # Estadísticas
                game_state = STATISTICS
                return game_state, score, patients_cured, lives, current_scenario, None, None, None, selected_option
            elif selected_option == 3:
                # Salir
                return "QUIT", score, patients_cured, lives, current_scenario, None, None, None, selected_option

    return game_state, score, patients_cured, lives, current_scenario, None, None, None, selected_option


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

def start_question(patient_level, patient_index, question_start_time, current_scenario=0):
    """
    Inicia una nueva pregunta para un paciente.

    Retorna:
    - Tupla con (pregunta, tiempo_limite)
    """
    current_question = get_random_question(patient_level, current_scenario)
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
    overlay = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
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


def draw_clinical_case_victory(screen, font_title, font_normal, total_points, bg_image=None, player_name=""):
    """Dibuja la pantalla de victoria cuando se alcanzan 15 puntos."""
    from constants import (CLINICAL_CASE_COLOR_TITLE, CLINICAL_CASE_COLOR_TEXT, CLINICAL_CASE_COLOR_INSTRUCTION,
                           COLOR_GREEN, COLOR_WHITE, CLINICAL_CASE_LINE_HEIGHT, COLOR_BACKGROUND)

    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)

    # Mostrar nombre del jugador arriba a la izquierda
    if player_name:
        player_text = font_normal.render(f"Jugador: {player_name}", True, COLOR_WHITE)
        screen.blit(player_text, (10, 10))

    # Título de victoria
    draw_text_centered(screen, "¡FELICIDADES!", font_title, COLOR_GREEN, 150)
    draw_text_centered(screen, "Has alcanzado 15 puntos", font_normal, COLOR_WHITE, 220)
    draw_text_centered(screen, f"Puntos totales: {total_points}", font_normal, COLOR_GREEN, 260)

    draw_text_centered(screen, "¿Qué deseas hacer?", font_normal, CLINICAL_CASE_COLOR_TEXT, 320)
    draw_text_centered(screen, "ESPACIO: Continuar en modo infinito", font_normal, COLOR_GREEN, 380)
    draw_text_centered(screen, "ESC: Volver al menú", font_normal, CLINICAL_CASE_COLOR_INSTRUCTION, 420)


# FUNCIONES DEL MODO CASO CLÍNICO

def draw_clinical_case_reading(screen, font_title, font_normal, case_data, bg_image=None, player_name=""):
    """Dibuja la pantalla de lectura del caso clínico dentro de un único cuadro con fondo."""
    from constants import (CLINICAL_CASE_COLOR_TITLE, CLINICAL_CASE_COLOR_TEXT, CLINICAL_CASE_COLOR_SECTION,
                           CLINICAL_CASE_COLOR_INSTRUCTION, CLINICAL_CASE_LINE_HEIGHT, CLINICAL_CASE_SECTION_SPACING,
                           COLOR_WHITE, COLOR_BACKGROUND)
    from ui_config import (QUESTION_BOX_X, QUESTION_BOX_Y, QUESTION_BOX_WIDTH, QUESTION_BOX_HEIGHT,
                           QUESTION_BOX_COLOR, QUESTION_BOX_ALPHA, QUESTION_BOX_BORDER_OUTER,
                           QUESTION_BOX_BORDER_INNER, QUESTION_BOX_BORDER_WIDTH, QUESTION_BOX_BORDER_INNER_WIDTH,
                           QUESTION_BOX_MARGIN)
    
    # Fondo con imagen (si existe) o color por defecto
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)
    
    # Mostrar nombre del jugador arriba a la izquierda (fuera del cuadro principal)
    if player_name:
        player_text = font_normal.render(f"Jugador: {player_name}", True, COLOR_WHITE)
        screen.blit(player_text, (10, 10))
    
    # Crear cuadro centrado para todo el contenido del caso (altura dinámica para exploración física)
    box_x = QUESTION_BOX_X              # Posición X del cuadro (centrado usando configuración de ui_config)
    box_y = 40                          # Posición Y más alta para ganar espacio vertical dentro del cuadro
    box_width = QUESTION_BOX_WIDTH      # Ancho del cuadro (constante reutilizada del sistema de preguntas)
    box_height = 580                    # Alto del cuadro para que quepan anamnesis, síntomas y exploración física
    box_center_x = box_x + box_width // 2
    
    # Dibujar rectángulo de fondo (semi-transparente)
    box_surface = pygame.Surface((box_width, box_height))  # Creamos una superficie con el tamaño del cuadro
    box_surface.set_alpha(QUESTION_BOX_ALPHA)              # Aplicamos transparencia configurada
    box_surface.fill(QUESTION_BOX_COLOR)                   # Rellenamos la superficie con el color del cuadro
    screen.blit(box_surface, (box_x, box_y))               # Dibujamos el cuadro sobre la pantalla principal
    
    # Bordes del cuadro
    pygame.draw.rect(screen, QUESTION_BOX_BORDER_OUTER, (box_x, box_y, box_width, box_height),
                     QUESTION_BOX_BORDER_WIDTH)             # Borde exterior más grueso
    pygame.draw.rect(screen, QUESTION_BOX_BORDER_INNER,
                     (box_x + 2, box_y + 2, box_width - 4, box_height - 4), QUESTION_BOX_BORDER_INNER_WIDTH)  # Borde interior decorativo
    
    # Contenido dentro del cuadro
    scroll_y = box_y + 20                          # Posición vertical inicial interna del contenido
    line_height = CLINICAL_CASE_LINE_HEIGHT        # Altura de cada línea de texto (definida en constants)
    max_width = box_width - QUESTION_BOX_MARGIN * 2  # Ancho máximo para el texto, dejando márgenes a ambos lados

    # Título del caso dentro del cuadro
    title_surface = font_title.render(case_data["title"], True, COLOR_WHITE)  # Renderizamos el título del caso
    title_rect = title_surface.get_rect(center=(box_center_x, scroll_y))      # Centramos el título dentro del cuadro
    screen.blit(title_surface, title_rect)                                    # Dibujamos el título dentro del cuadro
    scroll_y += CLINICAL_CASE_SECTION_SPACING                                 # Avanzamos la posición vertical para la siguiente sección

    # Datos del paciente (dentro del cuadro)
    section_title = font_normal.render("DATOS DEL PACIENTE", True, COLOR_WHITE)  # Título de sección: datos del paciente
    section_rect = section_title.get_rect(center=(box_center_x, scroll_y))       # Centramos el título de sección
    screen.blit(section_title, section_rect)                                     # Dibujamos el título de sección
    scroll_y += CLINICAL_CASE_SECTION_SPACING                                    # Bajamos para empezar el texto de la sección
    
    pd = case_data["patient_data"]
    text_x = box_x + QUESTION_BOX_MARGIN
    
    # Función auxiliar para renderizar texto con ajuste de línea
    def render_wrapped_text(text, y_pos, color=COLOR_WHITE):
        """
        Dibuja un texto largo dividéndolo en varias líneas dentro del ancho máximo del cuadro.
        """
        nonlocal scroll_y                                # Usamos la variable scroll_y definida en el ámbito exterior
        words = text.split()                             # Separamos el texto en palabras
        line = ""                                        # Línea actual que se está construyendo
        for word in words:
            test_line = line + (" " if line else "") + word             # Probamos a añadir una palabra más
            test_surface = font_normal.render(test_line, True, color)   # Renderizamos la línea de prueba
            if test_surface.get_width() > max_width:                    # Si se pasa del ancho permitido
                if line:                                                # Si la línea anterior tiene contenido
                    text_surface = font_normal.render(line, True, color)  # Renderizamos la línea válida
                    screen.blit(text_surface, (text_x, scroll_y))         # La dibujamos en pantalla
                    scroll_y += line_height                               # Bajamos a la siguiente línea verticalmente
                line = word                                              # Empezamos una nueva línea con la palabra actual
            else:
                line = test_line                                         # Actualizamos la línea actual con la palabra añadida
        if line:                                                         # Si queda texto pendiente al final del bucle
            text_surface = font_normal.render(line, True, color)        # Renderizamos la última línea
            screen.blit(text_surface, (text_x, scroll_y))               # La dibujamos en pantalla
            scroll_y += line_height                                     # Bajamos la posición vertical para lo siguiente
    
    render_wrapped_text(f"Nombre: {pd['name']}", scroll_y)
    render_wrapped_text(f"Edad: {pd['age']} años", scroll_y)
    render_wrapped_text(f"Sexo: {pd['sex']}", scroll_y)
    render_wrapped_text(f"Ocupación: {pd['occupation']}", scroll_y)
    render_wrapped_text(f"Motivo: {pd['chief_complaint']}", scroll_y)
    scroll_y += 10

    # Antecedentes
    section_title = font_normal.render("ANTECEDENTES", True, COLOR_WHITE)
    section_rect = section_title.get_rect(center=(box_center_x, scroll_y))
    screen.blit(section_title, section_rect)
    scroll_y += CLINICAL_CASE_SECTION_SPACING
    
    h = case_data["history"]
    render_wrapped_text(f"Personales: {h['personal']}", scroll_y)
    render_wrapped_text(f"Familiares: {h['family']}", scroll_y)
    render_wrapped_text(f"Hábitos: {h['habits']}", scroll_y)
    render_wrapped_text(f"Medicación: {h['medication']}", scroll_y)
    scroll_y += 10

    # Síntomas
    section_title = font_normal.render("SÍNTOMAS Y EVOLUCIÓN", True, COLOR_WHITE)
    section_rect = section_title.get_rect(center=(box_center_x, scroll_y))
    screen.blit(section_title, section_rect)
    scroll_y += CLINICAL_CASE_SECTION_SPACING
    
    s = case_data["symptoms"]
    render_wrapped_text(f"Inicio: {s['onset']}", scroll_y)
    render_wrapped_text(f"Duración: {s['duration']}", scroll_y)
    render_wrapped_text(f"Intensidad: {s['intensity']}", scroll_y)
    render_wrapped_text(f"Empeora: {s['worsening']}", scroll_y)
    render_wrapped_text(f"Mejora: {s['improving']}", scroll_y)
    scroll_y += 10

    # Exploración física
    section_title = font_normal.render("EXPLORACIÓN FÍSICA", True, COLOR_WHITE)
    section_rect = section_title.get_rect(center=(box_center_x, scroll_y))
    screen.blit(section_title, section_rect)
    scroll_y += CLINICAL_CASE_SECTION_SPACING
    
    pe = case_data["physical_exam"]
    render_wrapped_text(f"Signos vitales: {pe['vital_signs']}", scroll_y)
    render_wrapped_text(f"Hallazgos: {pe['findings']}", scroll_y)

    # Instrucción dentro del cuadro, al final
    #instruction_text = font_normal.render("ESPACIO: Continuar | ESC: Pausa", True, COLOR_WHITE)
    #instruction_rect = instruction_text.get_rect(center=(box_center_x, box_y + box_height - 25))
    #screen.blit(instruction_text, instruction_rect)


def draw_clinical_case_tests(screen, font_title, font_normal, selected_tests, test_selection_index, bg_image=None,
                             player_name=""):
    """Dibuja la pantalla de selección de pruebas dentro de un único cuadro."""
    from constants import (CLINICAL_CASE_COLOR_TITLE, CLINICAL_CASE_COLOR_TEXT, CLINICAL_CASE_COLOR_SELECTED,
                           CLINICAL_CASE_COLOR_INSTRUCTION, CLINICAL_CASE_OPTION_SPACING, COLOR_WHITE, COLOR_BACKGROUND)

    # Fondo con imagen (si existe) o color por defecto
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)

    # Mostrar nombre del jugador arriba a la izquierda (fuera del cuadro)
    if player_name:
        player_text = font_normal.render(f"Jugador: {player_name}", True, COLOR_WHITE)
        screen.blit(player_text, (10, 10))

    # Crear cuadro centrado
    from ui_config import (QUESTION_BOX_X, QUESTION_BOX_Y, QUESTION_BOX_WIDTH, QUESTION_BOX_HEIGHT,
                           QUESTION_BOX_COLOR, QUESTION_BOX_ALPHA, QUESTION_BOX_BORDER_OUTER,
                           QUESTION_BOX_BORDER_INNER, QUESTION_BOX_BORDER_WIDTH, QUESTION_BOX_BORDER_INNER_WIDTH,
                           QUESTION_BOX_MARGIN)
    
    box_x = QUESTION_BOX_X
    box_y = 70
    box_width = QUESTION_BOX_WIDTH
    box_height = 450
    box_center_x = box_x + box_width // 2

    # Dibujar cuadro
    box_surface = pygame.Surface((box_width, box_height))
    box_surface.set_alpha(QUESTION_BOX_ALPHA)
    box_surface.fill(QUESTION_BOX_COLOR)
    screen.blit(box_surface, (box_x, box_y))

    pygame.draw.rect(screen, QUESTION_BOX_BORDER_OUTER, (box_x, box_y, box_width, box_height),
                     QUESTION_BOX_BORDER_WIDTH)
    pygame.draw.rect(screen, QUESTION_BOX_BORDER_INNER,
                     (box_x + 2, box_y + 2, box_width - 4, box_height - 4), QUESTION_BOX_BORDER_INNER_WIDTH)

    from clinical_cases import TEST_TYPES

    # Título dentro del cuadro
    title_surface = font_title.render("SELECCIONA LAS PRUEBAS A SOLICITAR", True, COLOR_WHITE)
    title_rect = title_surface.get_rect(center=(box_center_x, box_y + 25))
    screen.blit(title_surface, title_rect)

    test_list = list(TEST_TYPES.keys())
    start_y = box_y + 60
    spacing = CLINICAL_CASE_OPTION_SPACING
    text_x = box_x + QUESTION_BOX_MARGIN

    for i, test_key in enumerate(test_list):
        y_pos = start_y + i * spacing
        test_name = TEST_TYPES[test_key]

        # Marcar si está seleccionada
        prefix = "[X] " if test_key in selected_tests else "[ ] "
        if i == test_selection_index:
            color = COLOR_WHITE
            prefix = "> " + prefix
        else:
            color = COLOR_WHITE
            prefix = "  " + prefix

        screen.blit(font_normal.render(f"{prefix}{test_name}", True, color), (text_x, y_pos))

    # Instrucciones dentro del cuadro
    instructions = "W/S: Navegar | ESPACIO: Seleccionar | ENTER: Continuar | ESC: Pausa"
    instr_surface = font_normal.render(instructions, True, COLOR_WHITE)
    instr_rect = instr_surface.get_rect(center=(box_center_x, box_y + box_height - 25))
    screen.blit(instr_surface, instr_rect)


def draw_clinical_case_results(screen, font_title, font_normal, case_data, selected_tests, bg_image=None,
                               player_name=""):
    """Dibuja los resultados de las pruebas dentro de un único cuadro."""
    from constants import (CLINICAL_CASE_COLOR_TITLE, CLINICAL_CASE_COLOR_TEXT, CLINICAL_CASE_COLOR_SECTION,
                           CLINICAL_CASE_COLOR_INSTRUCTION, CLINICAL_CASE_LINE_HEIGHT, COLOR_WHITE, COLOR_BACKGROUND)

    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)

    # Mostrar nombre del jugador arriba a la izquierda (fuera del cuadro)
    if player_name:
        player_text = font_normal.render(f"Jugador: {player_name}", True, COLOR_WHITE)
        screen.blit(player_text, (10, 10))

    # Crear cuadro centrado
    from ui_config import (QUESTION_BOX_X, QUESTION_BOX_Y, QUESTION_BOX_WIDTH, QUESTION_BOX_HEIGHT,
                           QUESTION_BOX_COLOR, QUESTION_BOX_ALPHA, QUESTION_BOX_BORDER_OUTER,
                           QUESTION_BOX_BORDER_INNER, QUESTION_BOX_BORDER_WIDTH, QUESTION_BOX_BORDER_INNER_WIDTH)

    box_x = QUESTION_BOX_X                         # Coordenada X del cuadro de resultados
    box_y = 40                                     # Coordenada Y algo más alta para ganar espacio
    box_width = QUESTION_BOX_WIDTH                 # Ancho del cuadro igual al de preguntas
    box_height = 520                               # Alto del cuadro aumentado para mostrar todo el contenido
    box_center_x = box_x + box_width // 2         # Centro horizontal del cuadro

    box_surface = pygame.Surface((box_width, box_height))  # Creamos superficie para el cuadro
    box_surface.set_alpha(QUESTION_BOX_ALPHA)              # Aplicamos transparencia
    box_surface.fill(QUESTION_BOX_COLOR)                   # Rellenamos con color del cuadro
    screen.blit(box_surface, (box_x, box_y))               # Dibujamos el cuadro en pantalla

    pygame.draw.rect(screen, QUESTION_BOX_BORDER_OUTER, (box_x, box_y, box_width, box_height),
                     QUESTION_BOX_BORDER_WIDTH)            # Borde exterior del cuadro
    pygame.draw.rect(screen, QUESTION_BOX_BORDER_INNER,
                     (box_x + 2, box_y + 2, box_width - 4, box_height - 4), QUESTION_BOX_BORDER_INNER_WIDTH)  # Borde interior

    # Título dentro del cuadro
    draw_text_centered(screen, "RESULTADOS DE PRUEBAS", font_title, CLINICAL_CASE_COLOR_TITLE, box_y + 25)

    from clinical_cases import TEST_TYPES

    y_pos = box_y + 60                               # Posición inicial para listar resultados dentro del cuadro
    results = case_data["test_results"]
    line_height = CLINICAL_CASE_LINE_HEIGHT

    for test_key in selected_tests:
        test_name = TEST_TYPES[test_key]
        result_text = results.get(test_key, "Resultado no disponible")

        # Título de la prueba
        screen.blit(font_normal.render(f"{test_name}:", True, CLINICAL_CASE_COLOR_SECTION),
                    (box_x + 20, y_pos))           # Dibujamos el nombre de la prueba dentro del cuadro (con margen)
        y_pos += line_height

        # Resultado (puede ser largo, dividir en líneas)
        words = result_text.split()                 # Separamos el texto del resultado en palabras
        line = ""                                   # Línea actual que estamos construyendo
        max_width = box_width - 60                  # Ancho máximo dentro del cuadro para el texto de resultado
        for word in words:
            test_line = line + (" " if line else "") + word                        # Probamos a añadir una palabra más
            test_surface = font_normal.render(test_line, True, CLINICAL_CASE_COLOR_TEXT)  # Renderizamos la línea de prueba
            if test_surface.get_width() > max_width:                               # Si se pasa del ancho máximo permitido
                if line:                                                           # Si teníamos una línea válida antes
                    screen.blit(font_normal.render(line, True, CLINICAL_CASE_COLOR_TEXT),
                                (box_x + 40, y_pos))                               # Dibujamos la línea actual dentro del cuadro
                    y_pos += line_height                                           # Bajamos a la siguiente línea
                line = word                                                        # Empezamos nueva línea con la palabra actual
            else:
                line = test_line                                                   # Mantenemos la línea con la palabra añadida
        if line:                                                                   # Si queda texto pendiente
            screen.blit(font_normal.render(line, True, CLINICAL_CASE_COLOR_TEXT),
                        (box_x + 40, y_pos))                                       # Dibujamos la última línea
            y_pos += line_height + 5                                               # Dejamos un pequeño espacio extra entre resultados
    
    # Instrucciones dentro del cuadro
    instruction_text = font_normal.render("ESPACIO: Continuar | ESC: Pausa", True, CLINICAL_CASE_COLOR_INSTRUCTION)
    instruction_rect = instruction_text.get_rect(center=(box_center_x, box_y + box_height - 25))
    screen.blit(instruction_text, instruction_rect)


def draw_clinical_case_diagnosis(screen, font_title, font_normal, case_data, selected_index, bg_image=None,
                                 player_name=""):
    """Dibuja la pantalla de selección de diagnóstico dentro de un único cuadro."""
    from constants import (CLINICAL_CASE_COLOR_TITLE, CLINICAL_CASE_COLOR_TEXT, CLINICAL_CASE_COLOR_SELECTED,
                           CLINICAL_CASE_COLOR_INSTRUCTION, CLINICAL_CASE_OPTION_SPACING, COLOR_WHITE, COLOR_BACKGROUND)

    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)

    # Mostrar nombre del jugador arriba a la izquierda (fuera del cuadro)
    if player_name:
        player_text = font_normal.render(f"Jugador: {player_name}", True, COLOR_WHITE)
        screen.blit(player_text, (10, 10))

    from ui_config import (QUESTION_BOX_X, QUESTION_BOX_Y, QUESTION_BOX_WIDTH, QUESTION_BOX_HEIGHT,
                           QUESTION_BOX_COLOR, QUESTION_BOX_ALPHA, QUESTION_BOX_BORDER_OUTER,
                           QUESTION_BOX_BORDER_INNER, QUESTION_BOX_BORDER_WIDTH, QUESTION_BOX_BORDER_INNER_WIDTH,
                           QUESTION_BOX_MARGIN)
    from constants import CLINICAL_CASE_LINE_HEIGHT

    box_x = QUESTION_BOX_X
    box_y = 70
    box_width = QUESTION_BOX_WIDTH
    box_height = 450
    box_center_x = box_x + box_width // 2
    max_option_width = box_width - QUESTION_BOX_MARGIN * 2

    box_surface = pygame.Surface((box_width, box_height))
    box_surface.set_alpha(QUESTION_BOX_ALPHA)
    box_surface.fill(QUESTION_BOX_COLOR)
    screen.blit(box_surface, (box_x, box_y))

    pygame.draw.rect(screen, QUESTION_BOX_BORDER_OUTER, (box_x, box_y, box_width, box_height),
                     QUESTION_BOX_BORDER_WIDTH)
    pygame.draw.rect(screen, QUESTION_BOX_BORDER_INNER,
                     (box_x + 2, box_y + 2, box_width - 4, box_height - 4), QUESTION_BOX_BORDER_INNER_WIDTH)

    # Título dentro del cuadro
    draw_text_centered(screen, "SELECCIONA EL DIAGNÓSTICO", font_title, CLINICAL_CASE_COLOR_TITLE, box_y + 30)

    diagnoses = case_data["diagnoses"]
    start_y = box_y + 80
    spacing = CLINICAL_CASE_OPTION_SPACING

    for i, diag in enumerate(diagnoses):
        y_pos = start_y + i * spacing
        if i == selected_index:
            color = CLINICAL_CASE_COLOR_SELECTED
            prefix = "> "
        else:
            color = CLINICAL_CASE_COLOR_TEXT
            prefix = "  "

        # Dividir texto largo en líneas (word wrap dentro del cuadro)
        text = f"{i + 1}. {diag['text']}"
        words = text.split()
        line = ""
        lines = []
        for word in words:
            test_line = line + (" " if line else "") + word
            test_surface = font_normal.render(test_line, True, color)
            if test_surface.get_width() > max_option_width:
                if line:
                    lines.append(line)
                line = word
            else:
                line = test_line
        if line:
            lines.append(line)

        for j, line_text in enumerate(lines):
            opt_surface = font_normal.render(f"{prefix if j == 0 else '  '}{line_text}", True, color)
            opt_rect = opt_surface.get_rect(center=(box_center_x, y_pos + j * CLINICAL_CASE_LINE_HEIGHT))
            screen.blit(opt_surface, opt_rect)
    
    # Instrucciones dentro del cuadro
    instruction = "W/S: Navegar | ESPACIO: Seleccionar | ESC: Pausa"
    instr_surface = font_normal.render(instruction, True, CLINICAL_CASE_COLOR_INSTRUCTION)
    instr_rect = instr_surface.get_rect(center=(box_center_x, box_y + box_height - 25))
    screen.blit(instr_surface, instr_rect)


def draw_clinical_case_treatment(screen, font_title, font_normal, case_data, selected_index, bg_image=None,
                                 player_name=""):
    """Dibuja la pantalla de selección de tratamiento dentro de un único cuadro."""
    from constants import (CLINICAL_CASE_COLOR_TITLE, CLINICAL_CASE_COLOR_TEXT, CLINICAL_CASE_COLOR_SELECTED,
                           CLINICAL_CASE_COLOR_INSTRUCTION, CLINICAL_CASE_OPTION_SPACING, CLINICAL_CASE_LINE_HEIGHT,
                           COLOR_WHITE, COLOR_BACKGROUND)

    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)

    # Mostrar nombre del jugador arriba a la izquierda (fuera del cuadro)
    if player_name:
        player_text = font_normal.render(f"Jugador: {player_name}", True, COLOR_WHITE)
        screen.blit(player_text, (10, 10))

    from ui_config import (QUESTION_BOX_X, QUESTION_BOX_Y, QUESTION_BOX_WIDTH, QUESTION_BOX_HEIGHT,
                           QUESTION_BOX_COLOR, QUESTION_BOX_ALPHA, QUESTION_BOX_BORDER_OUTER,
                           QUESTION_BOX_BORDER_INNER, QUESTION_BOX_BORDER_WIDTH, QUESTION_BOX_BORDER_INNER_WIDTH,
                           QUESTION_BOX_MARGIN)

    box_x = QUESTION_BOX_X
    box_y = 70
    box_width = QUESTION_BOX_WIDTH
    box_height = 450
    box_center_x = box_x + box_width // 2
    max_option_width = box_width - QUESTION_BOX_MARGIN * 2

    box_surface = pygame.Surface((box_width, box_height))
    box_surface.set_alpha(QUESTION_BOX_ALPHA)
    box_surface.fill(QUESTION_BOX_COLOR)
    screen.blit(box_surface, (box_x, box_y))

    pygame.draw.rect(screen, QUESTION_BOX_BORDER_OUTER, (box_x, box_y, box_width, box_height),
                     QUESTION_BOX_BORDER_WIDTH)
    pygame.draw.rect(screen, QUESTION_BOX_BORDER_INNER,
                     (box_x + 2, box_y + 2, box_width - 4, box_height - 4), QUESTION_BOX_BORDER_INNER_WIDTH)

    # Título dentro del cuadro
    draw_text_centered(screen, "SELECCIONA EL TRATAMIENTO", font_title, CLINICAL_CASE_COLOR_TITLE, box_y + 30)

    treatments = case_data["treatments"]
    start_y = box_y + 80
    spacing = CLINICAL_CASE_OPTION_SPACING

    for i, treat in enumerate(treatments):
        y_pos = start_y + i * spacing
        if i == selected_index:
            color = CLINICAL_CASE_COLOR_SELECTED
            prefix = "> "
        else:
            color = CLINICAL_CASE_COLOR_TEXT
            prefix = "  "

        # Dividir texto largo en líneas (word wrap dentro del cuadro)
        text = treat["text"]
        words = text.split()
        line = ""
        lines = []
        for word in words:
            test_line = line + (" " if line else "") + word
            test_surface = font_normal.render(test_line, True, color)
            if test_surface.get_width() > max_option_width:
                if line:
                    lines.append(line)
                line = word
            else:
                line = test_line
        if line:
            lines.append(line)

        for j, line_text in enumerate(lines):
            opt_surface = font_normal.render(f"{prefix if j == 0 else '  '}{line_text}", True, color)
            opt_rect = opt_surface.get_rect(center=(box_center_x, y_pos + j * CLINICAL_CASE_LINE_HEIGHT))
            screen.blit(opt_surface, opt_rect)
    
    # Instrucciones dentro del cuadro
    instruction = "W/S: Navegar | ESPACIO: Seleccionar | ESC: Pausa"
    instr_surface = font_normal.render(instruction, True, CLINICAL_CASE_COLOR_INSTRUCTION)
    instr_rect = instr_surface.get_rect(center=(box_center_x, box_y + box_height - 25))
    screen.blit(instr_surface, instr_rect)


def draw_clinical_case_final(screen, font_title, font_normal, case_data, test_score, test_feedback,
                             diagnosis_correct, treatment_correct, final_score, outcome_type, bg_image=None,
                             points_earned=0, total_points=0, infinite_mode=False, player_name=""):
    """Dibuja la pantalla de resultado final del caso dentro de un único cuadro."""
    from constants import (CLINICAL_CASE_COLOR_TITLE, CLINICAL_CASE_COLOR_TEXT, CLINICAL_CASE_COLOR_SECTION,
                           CLINICAL_CASE_COLOR_INSTRUCTION, CLINICAL_CASE_LINE_HEIGHT, COLOR_GREEN, COLOR_RED,
                           COLOR_WHITE, COLOR_BACKGROUND)

    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)

    # Mostrar nombre del jugador arriba a la izquierda (fuera del cuadro)
    if player_name:
        player_text = font_normal.render(f"Jugador: {player_name}", True, COLOR_WHITE)
        screen.blit(player_text, (10, 10))

    # Crear cuadro centrado
    from ui_config import (QUESTION_BOX_X, QUESTION_BOX_Y, QUESTION_BOX_WIDTH, QUESTION_BOX_HEIGHT,
                           QUESTION_BOX_COLOR, QUESTION_BOX_ALPHA, QUESTION_BOX_BORDER_OUTER,
                           QUESTION_BOX_BORDER_INNER, QUESTION_BOX_BORDER_WIDTH, QUESTION_BOX_BORDER_INNER_WIDTH)

    from ui_config import QUESTION_BOX_MARGIN
    box_x = QUESTION_BOX_X
    box_y = 50
    box_width = QUESTION_BOX_WIDTH
    box_height = 540
    box_center_x = box_x + box_width // 2
    max_text_width = box_width - QUESTION_BOX_MARGIN * 2
    text_left = box_x + QUESTION_BOX_MARGIN

    box_surface = pygame.Surface((box_width, box_height))
    box_surface.set_alpha(QUESTION_BOX_ALPHA)
    box_surface.fill(QUESTION_BOX_COLOR)
    screen.blit(box_surface, (box_x, box_y))

    pygame.draw.rect(screen, QUESTION_BOX_BORDER_OUTER, (box_x, box_y, box_width, box_height),
                     QUESTION_BOX_BORDER_WIDTH)
    pygame.draw.rect(screen, QUESTION_BOX_BORDER_INNER,
                     (box_x + 2, box_y + 2, box_width - 4, box_height - 4), QUESTION_BOX_BORDER_INNER_WIDTH)

    # Título dentro del cuadro
    draw_text_centered(screen, "RESULTADO DEL CASO", font_title, CLINICAL_CASE_COLOR_TITLE, box_y + 25)
    
    y_pos = box_y + 55
    line_height = CLINICAL_CASE_LINE_HEIGHT

    # Puntuación del caso
    screen.blit(font_normal.render(f"Puntuación del caso: {final_score}", True, COLOR_GREEN), (text_left, y_pos))
    y_pos += line_height + 5

    # Puntos ganados y total (solo si no es modo infinito)
    if not infinite_mode:
        if points_earned > 0:
            screen.blit(font_normal.render(f"Puntos ganados: +{points_earned}", True, COLOR_GREEN), (text_left, y_pos))
            y_pos += line_height + 5
        screen.blit(font_normal.render(f"Puntos totales: {total_points}/15", True, CLINICAL_CASE_COLOR_TEXT),
                    (text_left, y_pos))
        y_pos += line_height + 10
    else:
        screen.blit(font_normal.render("Modo Infinito - Sin límite de puntos", True, COLOR_GREEN), (text_left, y_pos))
        y_pos += line_height + 10

    # Feedback de pruebas (word wrap dentro del cuadro)
    screen.blit(font_normal.render("Evaluación de pruebas:", True, CLINICAL_CASE_COLOR_TEXT), (text_left, y_pos))
    y_pos += line_height
    screen.blit(font_normal.render(f"Puntos: {test_score}", True, CLINICAL_CASE_COLOR_TEXT), (text_left + 20, y_pos))
    y_pos += line_height
    words = test_feedback.split()
    line = ""
    for word in words:
        test_line = line + (" " if line else "") + word
        test_surface = font_normal.render(test_line, True, CLINICAL_CASE_COLOR_TEXT)
        if test_surface.get_width() > max_text_width:
            if line:
                screen.blit(font_normal.render(line, True, CLINICAL_CASE_COLOR_TEXT), (text_left + 20, y_pos))
                y_pos += line_height
            line = word
        else:
            line = test_line
    if line:
        screen.blit(font_normal.render(line, True, CLINICAL_CASE_COLOR_TEXT), (text_left + 20, y_pos))
        y_pos += line_height + 5

    # Diagnóstico
    diag_text = "✓ Correcto" if diagnosis_correct else "✗ Incorrecto"
    diag_color = COLOR_GREEN if diagnosis_correct else COLOR_RED
    screen.blit(font_normal.render(f"Diagnóstico: {diag_text}", True, diag_color), (text_left, y_pos))
    y_pos += line_height + 5

    # Tratamiento
    treat_text = "✓ Correcto" if treatment_correct else "✗ Incorrecto"
    treat_color = COLOR_GREEN if treatment_correct else COLOR_RED
    screen.blit(font_normal.render(f"Tratamiento: {treat_text}", True, treat_color), (text_left, y_pos))
    y_pos += line_height + 10

    # Resultado del paciente (word wrap dentro del cuadro)
    outcomes = case_data["outcomes"]
    outcome_text = outcomes.get(outcome_type, outcomes["incorrect"])
    screen.blit(font_normal.render("Resultado del paciente:", True, CLINICAL_CASE_COLOR_TEXT), (text_left, y_pos))
    y_pos += line_height
    words = outcome_text.split()
    line = ""
    for word in words:
        test_line = line + (" " if line else "") + word
        test_surface = font_normal.render(test_line, True, CLINICAL_CASE_COLOR_TEXT)
        if test_surface.get_width() > max_text_width:
            if line:
                screen.blit(font_normal.render(line, True, CLINICAL_CASE_COLOR_TEXT), (text_left, y_pos))
                y_pos += line_height
            line = word
        else:
            line = test_line
    if line:
        screen.blit(font_normal.render(line, True, CLINICAL_CASE_COLOR_TEXT), (text_left, y_pos))
        y_pos += line_height + 10

    # Explicación educativa (word wrap dentro del cuadro)
    screen.blit(font_normal.render("Explicación:", True, CLINICAL_CASE_COLOR_SECTION), (text_left, y_pos))
    y_pos += line_height
    explanation = case_data["explanation"]
    words = explanation.split()
    line = ""
    for word in words:
        test_line = line + (" " if line else "") + word
        test_surface = font_normal.render(test_line, True, CLINICAL_CASE_COLOR_TEXT)
        if test_surface.get_width() > max_text_width:
            if line:
                screen.blit(font_normal.render(line, True, CLINICAL_CASE_COLOR_TEXT), (text_left, y_pos))
                y_pos += line_height
            line = word
        else:
            line = test_line
    if line:
        screen.blit(font_normal.render(line, True, CLINICAL_CASE_COLOR_TEXT), (text_left, y_pos))

    # Instrucciones dentro del cuadro
    instruction = "ESPACIO: Siguiente caso | ESC: Pausa"
    instr_surface = font_normal.render(instruction, True, CLINICAL_CASE_COLOR_INSTRUCTION)
    instr_rect = instr_surface.get_rect(center=(box_center_x, box_y + box_height - 25))
    screen.blit(instr_surface, instr_rect)


def handle_clinical_case_events(event, case_phase, case_data, selected_tests, test_selection_index,
                                diagnosis_index, treatment_index, case_start_time, test_score=0,
                                diagnosis_correct=False):
    """
    Maneja los eventos del teclado en el modo de caso clínico.

    Returns:
        (new_phase, updated_data) - Nueva fase y datos actualizados
    """
    from clinical_cases import (CASE_PHASE_READING, CASE_PHASE_TESTS, CASE_PHASE_RESULTS,
                                CASE_PHASE_DIAGNOSIS, CASE_PHASE_TREATMENT, CASE_PHASE_RESULT,
                                TEST_TYPES, calculate_test_score, calculate_final_score)
    from constants import CLINICAL_CASE

    if event.type == pygame.KEYDOWN:
        if case_phase == CASE_PHASE_READING:
            if event.key == pygame.K_SPACE:
                return CASE_PHASE_TESTS, {"selected_tests": [], "test_selection_index": 0}

        elif case_phase == CASE_PHASE_TESTS:
            test_list = list(TEST_TYPES.keys())
            if event.key == pygame.K_w:
                new_index = (test_selection_index - 1) % len(test_list)
                return CASE_PHASE_TESTS, {"test_selection_index": new_index}
            elif event.key == pygame.K_s:
                new_index = (test_selection_index + 1) % len(test_list)
                return CASE_PHASE_TESTS, {"test_selection_index": new_index}
            elif event.key == pygame.K_SPACE:
                # Toggle selección de prueba
                test_key = test_list[test_selection_index]
                new_tests = selected_tests.copy()
                if test_key in new_tests:
                    new_tests.remove(test_key)
                else:
                    new_tests.append(test_key)
                return CASE_PHASE_TESTS, {"selected_tests": new_tests}
            elif event.key == pygame.K_RETURN:
                # Continuar a ver resultados
                return CASE_PHASE_RESULTS, {}

        elif case_phase == CASE_PHASE_RESULTS:
            if event.key == pygame.K_SPACE:
                return CASE_PHASE_DIAGNOSIS, {"diagnosis_index": 0}

        elif case_phase == CASE_PHASE_DIAGNOSIS:
            diagnoses = case_data["diagnoses"]
            if event.key == pygame.K_w:
                new_index = (diagnosis_index - 1) % len(diagnoses)
                return CASE_PHASE_DIAGNOSIS, {"diagnosis_index": new_index}
            elif event.key == pygame.K_s:
                new_index = (diagnosis_index + 1) % len(diagnoses)
                return CASE_PHASE_DIAGNOSIS, {"diagnosis_index": new_index}
            elif event.key == pygame.K_SPACE:
                # Calcular puntuación de pruebas
                calc_test_score, test_feedback = calculate_test_score(
                    selected_tests,
                    case_data["correct_tests"],
                    case_data["optional_tests"],
                    case_data["unnecessary_tests"]
                )
                # Verificar si el diagnóstico es correcto
                diag_correct = diagnoses[diagnosis_index]["correct"]
                # Continuar a tratamiento
                return CASE_PHASE_TREATMENT, {
                    "test_score": calc_test_score,
                    "test_feedback": test_feedback,
                    "diagnosis_correct": diag_correct,
                    "treatment_index": 0
                }

        elif case_phase == CASE_PHASE_TREATMENT:
            treatments = case_data["treatments"]
            if event.key == pygame.K_w:
                new_index = (treatment_index - 1) % len(treatments)
                return CASE_PHASE_TREATMENT, {"treatment_index": new_index}
            elif event.key == pygame.K_s:
                new_index = (treatment_index + 1) % len(treatments)
                return CASE_PHASE_TREATMENT, {"treatment_index": new_index}
            elif event.key == pygame.K_SPACE:
                # Calcular resultado final
                treatment_correct = treatments[treatment_index]["correct"]
                time_taken = pygame.time.get_ticks() - case_start_time
                max_time = 300000  # 5 minutos máximo

                # Determinar tipo de resultado
                if diagnosis_correct and treatment_correct:
                    outcome_type = "correct"
                elif diagnosis_correct or treatment_correct:
                    outcome_type = "partial"
                else:
                    outcome_type = "incorrect"

                final_score = calculate_final_score(
                    test_score, diagnosis_correct, treatment_correct, time_taken, max_time,
                    case_data.get("difficulty", "medium")
                )

                # Suma de puntos: se otorgan cuando el jugador acierta diagnóstico Y tratamiento
                # (las pruebas afectan solo la puntuación de pruebas y el feedback, no el marcador 0/15)
                from clinical_cases import get_points_for_difficulty
                points_earned = 0
                if diagnosis_correct and treatment_correct:
                    points_earned = get_points_for_difficulty(case_data.get("difficulty", "medium"))
                    # Validación: confirmar que los puntos se calculan (útil para depuración)
                    if __debug__:
                        print(f"[Caso Clínico] Puntos ganados en este caso: {points_earned} (diagnóstico y tratamiento correctos)")

                return CASE_PHASE_RESULT, {
                    "final_score": final_score,
                    "outcome_type": outcome_type,
                    "points_earned": points_earned
                }

        elif case_phase == CASE_PHASE_RESULT:
            if event.key == pygame.K_SPACE:
                return "NEXT_CASE", {}

    return case_phase, {}


# FUNCIONES DE PANTALLA INICIAL

def draw_initial_screen(screen, font, font_small, bg_image=None, player_name=""):
    """Dibuja la pantalla inicial con input de nombre."""
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)

    # Título
    draw_text_centered(screen, "DOCTOR RUSH", font, COLOR_WHITE, 150)

    # Instrucción
    draw_text_centered(screen, "Ingresa tu nombre:", font_small, COLOR_WHITE, 280)

    # Mostrar nombre actual
    if player_name:
        name_text = font.render(player_name, True, COLOR_GREEN)
        name_rect = name_text.get_rect(center=(BASE_WIDTH // 2, 340))
        screen.blit(name_text, name_rect)
    else:
        draw_text_centered(screen, "_", font, COLOR_GREEN, 340)

    # Instrucciones
    draw_text_centered(screen, "Escribe tu nombre y presiona ENTER para continuar", font_small, COLOR_WHITE, 420)
    draw_text_centered(screen, "ESC: Salir", font_small, COLOR_WHITE, 480)


def handle_initial_screen_events(event, player_name):
    """Maneja eventos de la pantalla inicial."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if player_name.strip():
                return "CONTINUE", player_name.strip()
        elif event.key == pygame.K_BACKSPACE:
            return "BACKSPACE", player_name[:-1] if player_name else ""
        elif event.key == pygame.K_ESCAPE:
            return "QUIT", player_name
        elif event.unicode.isprintable() and len(player_name) < 20:
            return "TEXT", player_name + event.unicode

    return None, player_name


# FUNCIONES DE ESTADÍSTICAS

def draw_statistics(screen, font, font_small, bg_image=None, stats_data=None, confirm_delete=False):
    """
    Dibuja la pantalla de estadísticas: historial de puntajes (Doctor Rush y Caso Clínico),
    con columnas #, Jugador, Juego, Puntos y Fecha. Los datos se leen desde stats.json
    para reflejar el guardado persistente al volver al menú o reabrir el juego.
    """
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOR_BACKGROUND)
    
    # Título
    draw_text_centered(screen, "ESTADÍSTICAS", font, COLOR_WHITE, 30)
    
    if not stats_data or len(stats_data) == 0:
        draw_text_centered(screen, "No hay estadísticas disponibles", font_small, COLOR_WHITE, BASE_HEIGHT // 2)
        draw_text_centered(screen, "ESC: Volver al menú", font_small, COLOR_WHITE, BASE_HEIGHT - 50)
        return
    
    # Encabezados de tabla: #, Jugador, Juego, Puntos, Fecha (sin columna Pacientes)
    header_y = 80
    headers = ["#", "Jugador", "Juego", "Puntos", "Fecha"]
    header_widths = [30, 150, 150, 100, 250]
    header_x = 50
    
    for i, header in enumerate(headers):
        header_text = font_small.render(header, True, COLOR_GREEN)
        screen.blit(header_text, (header_x, header_y))
        header_x += header_widths[i]
    
    # Línea separadora
    pygame.draw.line(screen, COLOR_WHITE, (50, header_y + 25), (BASE_WIDTH - 50, header_y + 25), 2)
    
    # Lectura en estadísticas: se carga desde stats.json para mostrar Doctor Rush y Caso Clínico
    from user_manager import UserManager
    user_manager = UserManager()
    user_manager.load_stats()
    history = user_manager.get_score_history(20)  # Últimas 20 partidas (incluye clinical_case)
    if __debug__ and history:
        clinical_entries = [e for e in history if e.get("game") == "clinical_case"]
        if clinical_entries:
            print(f"[Estadísticas] Mostrando {len(clinical_entries)} partida(s) Caso Clínico en historial (puntos: {[e.get('score') for e in clinical_entries[:5]]})")
    
    # Datos de la tabla
    start_y = header_y + 40
    row_height = 28
    max_rows = min(15, len(history))  # Mostrar hasta 15 entradas
    
    for i, entry in enumerate(history[:max_rows]):
        y_pos = start_y + i * row_height
        
        # Posición/Ranking
        rank_text = font_small.render(f"{i+1}.", True, COLOR_GREEN)
        screen.blit(rank_text, (50, y_pos))
        
        # Nombre del jugador
        name_text = font_small.render(entry.get("name", "Unknown")[:18], True, COLOR_WHITE)
        screen.blit(name_text, (80, y_pos))
        
        # Juego (Doctor Rush o Caso Clínico)
        game_name = entry.get("game", "unknown")
        if game_name == "doctor_rush":
            game_display = "Doctor Rush"
        elif game_name == "clinical_case":
            game_display = "Caso Clínico"
        else:
            game_display = "Desconocido"
        game_text = font_small.render(game_display[:18], True, COLOR_WHITE)
        screen.blit(game_text, (230, y_pos))
        
        # Puntos (Doctor Rush o Caso Clínico según la partida)
        score = entry.get("score", 0)
        score_text = font_small.render(str(score), True, COLOR_WHITE)
        screen.blit(score_text, (380, y_pos))
        
        # Fecha (formateada)
        date_str = entry.get("date", "")
        if date_str:
            try:
                from datetime import datetime
                try:
                    dt = datetime.fromisoformat(date_str)
                except:
                    try:
                        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    except:
                        dt = None
                if dt:
                    date_str = dt.strftime("%d/%m/%Y %H:%M")
                elif len(date_str) > 16:
                    date_str = date_str[:16]
            except:
                if len(date_str) > 16:
                    date_str = date_str[:16]
        date_text = font_small.render(date_str[:18], True, COLOR_WHITE)
        screen.blit(date_text, (480, y_pos))
    
    # Instrucciones
    draw_text_centered(screen, "ESC: Volver al menú", font_small, COLOR_WHITE, BASE_HEIGHT - 50)


def handle_statistics_events(event):
    """Maneja eventos de la pantalla de estadísticas."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "MENU"
    
    return None
