import pygame
import constants
import os
from constants import (WIDTH_SCREEN, HEIGHT_SCREEN, SPEED_CHARACTER, MENU, PLAYING, QUESTION, PAUSE, LEVEL_COMPLETE, GAME_OVER,
                      COLOR_WHITE, SCENARIO_1, SCENARIO_2, SCENARIO_3,
                      WIDTH_CHARACTER, HEIGHT_CHARACTER, INITIAL_LIVES,
                      PATH_BACKGROUNDS, FILE_QUESTION_BG, FILE_MENU_BG, FILE_GAME_BG, FPS)
from character import Character
from assets_loader import load_all_animations
from patient_manager import create_patients
from game_states import (draw_menu, handle_menu_events, draw_patients, start_question,
                         check_answer, check_time_up, draw_question_screen, draw_game_over, draw_pause, draw_level_complete)
from ui_config import FONT_SIZE_LARGE, FONT_SIZE_SMALL


# INICIALIZACIÓN DE PYGAME

pygame.init()
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("DOCTOR RUSH")

# Crear fuentes usando las configuraciones de ui_config
font = pygame.font.Font(None, FONT_SIZE_LARGE)
font_small = pygame.font.Font(None, FONT_SIZE_SMALL)


# CARGA DE RECURSOS (IMÁGENES Y FONDOS)

# Función para cargar fondo según el escenario (bg1, bg2, bg3)
def load_background(scenario_index):
    """
    Carga el fondo correspondiente al escenario actual.
    Escenario 0 -> bg1.png
    Escenario 1 -> bg2.png
    Escenario 2 -> bg3.png
    """
    bg_files = ["bg1.png", "bg2.png", "bg3.png"]
    if 0 <= scenario_index < len(bg_files):
        bg_file = bg_files[scenario_index]
        bg_path = os.path.join(PATH_BACKGROUNDS, bg_file)
        try:
            bg_img = pygame.image.load(bg_path).convert()
            bg_img = pygame.transform.scale(bg_img, (WIDTH_SCREEN, HEIGHT_SCREEN))
            print(f"Fondo cargado: {bg_path}")
            return bg_img
        except Exception as e:
            print(f"Error al cargar fondo {bg_file}: {e}")
            return None
    return None

# Cargar fondo inicial (escenario 0)
bg_image = load_background(0)

# Cargar fondo del menú
try:
    menu_bg_path = os.path.join(PATH_BACKGROUNDS, FILE_MENU_BG)
    menu_bg_image = pygame.image.load(menu_bg_path).convert()
    menu_bg_image = pygame.transform.scale(menu_bg_image, (WIDTH_SCREEN, HEIGHT_SCREEN))
    #print(f"Fondo del menú cargado: {menu_bg_path}")
except Exception as e:
    #print(f"Fondo del menú no cargado: {e}")
    menu_bg_image = None

# Cargar fondo de la pantalla de pregunta
try:
    question_bg_path = os.path.join(PATH_BACKGROUNDS, FILE_QUESTION_BG)
    if os.path.exists(question_bg_path):
        question_bg_image = pygame.image.load(question_bg_path).convert()
        question_bg_image = pygame.transform.scale(question_bg_image, (WIDTH_SCREEN, HEIGHT_SCREEN))
        print(f"Fondo de pregunta cargado correctamente desde: {question_bg_path}")
    else:
        print(f"Archivo no encontrado: {question_bg_path}")
        question_bg_image = None
except Exception as e:
    print(f"Error al cargar fondo de pregunta: {e}")
    print(f"Ruta intentada: {os.path.join(PATH_BACKGROUNDS, FILE_QUESTION_BG)}")
    question_bg_image = None


# CARGA DE ANIMACIONES

# Cargar todas las animaciones (jugador y pacientes)
try:
    animations = load_all_animations()
    player_animation = animations["player"]
    animations_green = animations["green"]
    animations_yellow = animations["yellow"]
    animations_orange = animations["orange"]
    print("Animaciones cargadas correctamente")
except Exception as e:
    print(f"Error al cargar animaciones: {e}")
    # Usar animación básica del jugador como respaldo
    player_animation = []
    for i in range(6):
        try:
            from utils import scale_img
            from constants import SCALE_CHARACTER

            img = pygame.image.load(f"assets/image/character/player/Player_{i}.png")
            img = scale_img(img, SCALE_CHARACTER)
            player_animation.append(img)
        except:
            # Si no se puede cargar, crear una imagen básica
            img = pygame.Surface((27, 27))
            img.fill((255, 255, 0))
            player_animation.append(img)
    animations_green = []
    animations_yellow = []
    animations_orange = []


# VARIABLES DE ESTADO DEL JUEGO

game_state = MENU  # Estado actual: MENU, PLAYING, QUESTION, GAME_OVER
current_scenario = 0  # Escenario actual (0, 1, 2)
scenarios = [SCENARIO_1, SCENARIO_2, SCENARIO_3]  # Colores de fondo por escenario
score = 0  # Puntuación del jugador
patients_cured = 0  # Contador de pacientes curados
lives = INITIAL_LIVES  # Vidas actuales del jugador

# Variables relacionadas con las preguntas
current_question = None  # Pregunta actual que se está mostrando
current_patient_index = -1  # Índice del paciente que se está atendiendo
current_patient_level = None  # Nivel del paciente actual ("green", "yellow", "orange")
question_result = None  # Resultado de la pregunta (None, True, False)
question_result_time = 0  # Tiempo en que se mostró el resultado
question_start_time = 0  # Tiempo en que inició la pregunta
question_time_limit = 0  # Tiempo límite para responder (en milisegundos)


# CREACIÓN DE PERSONAJES

# Crear jugador (doctor) - Posición inicial en el centro de la pantalla
player = Character(WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2, player_animation, 100)

# Crear pacientes iniciales para el nivel 0
list_patients, patient_levels = create_patients(0, animations_green, animations_yellow, animations_orange,
                                                player_animation)

# Asegurarse de que hay pacientes (crear uno de respaldo si no hay)
if len(list_patients) == 0:
    print("Advertencia: No se encontraron pacientes, creando uno de respaldo")
    list_patients = [Character(100, 100, player_animation, 100)]
    patient_levels = ["green"]

# Lista para rastrear qué pacientes están curados
patients_cured_list = [False] * len(list_patients)


# VARIABLES DE CONTROL

# Variables de movimiento del jugador (teclas presionadas)
move_up = False
move_down = False
move_left = False
move_right = False

# Controlador del frame rate
clock = pygame.time.Clock()


# LOOP PRINCIPAL DEL JUEGO

run = True
while run:
    # Controlar la velocidad del juego (FPS)
    clock.tick(FPS)


    # ESTADO: MENÚ INICIAL

    if game_state == MENU:
        draw_menu(screen, font, font_small, menu_bg_image)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                result = handle_menu_events(event, game_state, player, score, patients_cured, lives,
                                            current_scenario, create_patients, animations_green,
                                            animations_yellow, animations_orange, player_animation)
                if result[0] == "QUIT":
                    run = False
                elif result[0] == PLAYING:
                    game_state = result[0]
                    score = result[1]
                    patients_cured = result[2]
                    lives = result[3]
                    current_scenario = result[4]
                    list_patients = result[5]
                    patient_levels = result[6]
                    patients_cured_list = result[7]
                    # Reposicionar jugador en el centro al iniciar nuevo juego
                    player.shape.center = (WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2)


    # ESTADO: JUGANDO (PANTALLA PRINCIPAL)

    elif game_state == PLAYING:
        # Cargar y dibujar fondo según el escenario actual
        bg_image = load_background(current_scenario)
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill(scenarios[current_scenario])

        # Calcular el movimiento del jugador
        delta_x = 0
        delta_y = 0

        if move_right:
            delta_x = SPEED_CHARACTER
        if move_left:
            delta_x = -SPEED_CHARACTER
        if move_down:
            delta_y = SPEED_CHARACTER
        if move_up:
            delta_y = -SPEED_CHARACTER

        # Mover jugador
        player.move(delta_x, delta_y)

        # Limitar movimiento dentro de la pantalla
        if player.shape.x < 0:
            player.shape.x = 0
        if player.shape.x > WIDTH_SCREEN - WIDTH_CHARACTER:
            player.shape.x = WIDTH_SCREEN - WIDTH_CHARACTER
        if player.shape.y < 0:
            player.shape.y = 0
        if player.shape.y > HEIGHT_SCREEN - HEIGHT_CHARACTER:
            player.shape.y = HEIGHT_SCREEN - HEIGHT_CHARACTER

        # Actualizar al jugador (los pacientes se quedan quietos, sin animación)
        player.update()
        # Los pacientes no se actualizan para que se queden quietos

        # Dibujar al jugador
        player.draw(screen)

        # Dibujar pacientes con distintivos
        draw_patients(screen, list_patients, patient_levels, patients_cured_list, player, font_small)

        # Mostrar puntuación y vidas
        text_score = font_small.render(
            f"Puntuación: {score} | Pacientes curados: {patients_cured}/{len(list_patients)}", True, COLOR_WHITE)
        screen.blit(text_score, (10, 10))
        text_lives = font_small.render(f"Vidas: {lives}", True, (255, 0, 0))
        screen.blit(text_lives, (10, 35))

        # Mostrar instrucciones
        text_instructions = font_small.render("WASD: Mover | E: Interactuar | ESC: Pausa", True, COLOR_WHITE)
        screen.blit(text_instructions, (10, HEIGHT_SCREEN - 30))

        # Verificar si se quedó sin vidas
        if lives <= 0:
            game_state = GAME_OVER

        # Verificar si todos los pacientes están curados
        if patients_cured >= len(list_patients):
            # Si llegamos al nivel 3 (escenario 2), mostrar mensaje de continuar/terminar
            if current_scenario == 2:
                # Mostrar pantalla de nivel completado y preguntar si continuar
                game_state = LEVEL_COMPLETE
            else:
                # Cambiar de escenario
                current_scenario += 1
                patients_cured = 0
                # Recrear pacientes para el nuevo escenario
                list_patients, patient_levels = create_patients(current_scenario, animations_green,
                                                                animations_yellow, animations_orange, player_animation)
                patients_cured_list = [False] * len(list_patients)
                # Reposicionar jugador en el centro
                player.shape.center = (WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                if event.key == pygame.K_d:
                    move_right = True
                if event.key == pygame.K_w:
                    move_up = True
                if event.key == pygame.K_s:
                    move_down = True
                if event.key == pygame.K_e:
                    # Verificar interacción con pacientes
                    for i, ene in enumerate(list_patients):
                        if not patients_cured_list[i]:
                            from utils import calculate_distance

                            distance = calculate_distance(
                                player.shape.centerx, player.shape.centery,
                                ene.shape.centerx, ene.shape.centery
                            )
                            if distance < 50:  # DISTANCE_INTERACTION
                                # Iniciar pregunta
                                if i < len(patient_levels):
                                    current_patient_level = patient_levels[i]
                                    try:
                                        current_question, question_time_limit = start_question(current_patient_level, i,
                                                                                               pygame.time.get_ticks())
                                        current_patient_index = i
                                        question_start_time = pygame.time.get_ticks()
                                        game_state = QUESTION
                                        question_result = None
                                        break
                                    except Exception as e:
                                        print(f"Error al iniciar pregunta: {e}")
                                        # Continuar sin iniciar pregunta si hay error
                                break
                if event.key == pygame.K_ESCAPE:
                    # Ir al menú de pausa en lugar de regresar al menú principal
                    game_state = PAUSE
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_w:
                    move_up = False
                if event.key == pygame.K_s:
                    move_down = False


    # ESTADO: PREGUNTA (ATENDIENDO PACIENTE)

    elif game_state == QUESTION:
        # Verificar que hay una pregunta válida
        if current_question is None:
            # Si no hay pregunta, volver al juego
            game_state = PLAYING
        else:
            # Verificar si se agotó el tiempo (solo si aún no hay resultado)
            if question_result is None:
                elapsed_time = pygame.time.get_ticks() - question_start_time
                if elapsed_time >= question_time_limit:
                    question_result = False
                    # Restar vidas según el nivel del paciente (solo una vez)
                    from constants import LIVES_LOST_GREEN, LIVES_LOST_YELLOW, LIVES_LOST_ORANGE

                    if current_patient_level == "green":
                        lives -= LIVES_LOST_GREEN
                    elif current_patient_level == "yellow":
                        lives -= LIVES_LOST_YELLOW
                    elif current_patient_level == "orange":
                        lives -= LIVES_LOST_ORANGE
                    question_result_time = pygame.time.get_ticks()

            # Dibujar pantalla de pregunta (sin imagen del paciente, solo el fondo)
            draw_question_screen(screen, font, font_small, current_question, current_patient_level,
                                 question_start_time, question_time_limit, question_result, question_bg_image)

        if question_result is None and current_question is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        question_result, score, patients_cured, lives = check_answer(0, current_question["correcta"],
                                                                                     current_patient_level, score,
                                                                                     patients_cured, lives)
                        question_result_time = pygame.time.get_ticks()
                    if event.key == pygame.K_2:
                        question_result, score, patients_cured, lives = check_answer(1, current_question["correcta"],
                                                                                     current_patient_level, score,
                                                                                     patients_cured, lives)
                        question_result_time = pygame.time.get_ticks()
                    if event.key == pygame.K_3:
                        question_result, score, patients_cured, lives = check_answer(2, current_question["correcta"],
                                                                                     current_patient_level, score,
                                                                                     patients_cured, lives)
                        question_result_time = pygame.time.get_ticks()
        else:
            # Volver al juego después de 2 segundos o al presionar espacio
            if pygame.time.get_ticks() - question_result_time > 2000:
                game_state = PLAYING
                # Marcar paciente como curado si la respuesta fue correcta
                if question_result and current_patient_index >= 0:
                    patients_cured_list[current_patient_index] = True
                question_result = None
                current_patient_index = -1
                current_patient_level = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = PLAYING
                        # Marcar paciente como curado si la respuesta fue correcta
                        if question_result and current_patient_index >= 0:
                            patients_cured_list[current_patient_index] = True
                        question_result = None
                        current_patient_index = -1
                        current_patient_level = None


    # ESTADO: PAUSA
    elif game_state == PAUSE:
        # Dibujar pantalla de pausa (el juego se congela, no se actualiza nada)
        draw_pause(screen, font, font_small)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # ESPACIO: continuar jugando donde estabas
                if event.key == pygame.K_SPACE:
                    game_state = PLAYING
                # ESC: salir al menú principal
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU

    # ESTADO: NIVEL COMPLETADO (al llegar al nivel 3)
    elif game_state == LEVEL_COMPLETE:
        # Dibujar pantalla de nivel completado
        draw_level_complete(screen, font, font_small, score, patients_cured)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # ESPACIO: continuar jugando desde el nivel 1
                if event.key == pygame.K_SPACE:
                    current_scenario = 0
                    patients_cured = 0
                    list_patients, patient_levels = create_patients(0, animations_green,
                                                                    animations_yellow, animations_orange, player_animation)
                    patients_cured_list = [False] * len(list_patients)
                    player.shape.center = (WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2)
                    game_state = PLAYING
                # ESC: terminar partida y volver al menú
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU

    # ESTADO: GAME OVER (JUEGO TERMINADO)
    elif game_state == GAME_OVER:
        draw_game_over(screen, font, font_small, score, patients_cured)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = MENU
                if event.key == pygame.K_ESCAPE:
                    run = False

    pygame.display.update()

pygame.quit()
