import pygame
import constants
import os
from constants import (WIDTH_SCREEN, HEIGHT_SCREEN, BASE_WIDTH, BASE_HEIGHT, SPEED_CHARACTER, INITIAL_SCREEN, MENU, PLAYING, QUESTION, PAUSE, LEVEL_COMPLETE,
                       GAME_OVER, CLINICAL_CASE, CLINICAL_CASE_PAUSE, CLINICAL_CASE_VICTORY, STATISTICS,
                       COLOR_WHITE, COLOR_BACKGROUND, COLOR_GREEN, SCENARIO_1, SCENARIO_2, SCENARIO_3,
                      WIDTH_CHARACTER, HEIGHT_CHARACTER, INITIAL_LIVES,
                       PATH_BACKGROUNDS, FILE_QUESTION_BG, FILE_MENU_BG, FILE_GAME_BG, FILE_CLINICAL_CASE_BG, FILE_INITIAL_BG, FPS,
                       CLINICAL_CASE_FONT_TITLE, CLINICAL_CASE_FONT_NORMAL, CLINICAL_CASE_FONT_SMALL, CLINICAL_CASE_FONT_TINY,
                       SOUND_VOLUME_DOCTOR_RUSH_BG, SOUND_VOLUME_CLINICAL_CASE_BG)
from character import Character
from assets_loader import load_all_animations
from patient_manager import create_patients
from game_states import (draw_menu, handle_menu_events, draw_patients, start_question,
                         check_answer, check_time_up, draw_question_screen, draw_game_over, draw_pause,
                         draw_level_complete,
                         draw_clinical_case_reading, draw_clinical_case_tests, draw_clinical_case_results,
                         draw_clinical_case_diagnosis, draw_clinical_case_treatment, draw_clinical_case_final,
                         draw_clinical_case_victory, handle_clinical_case_events,
                         draw_initial_screen, handle_initial_screen_events, draw_statistics, handle_statistics_events)
from user_manager import UserManager
from sound_manager import SoundManager
from ui_config import FONT_SIZE_LARGE, FONT_SIZE_SMALL
from clinical_cases import get_random_case, CASE_PHASE_READING, CASE_PHASE_TESTS, CASE_PHASE_RESULTS, \
    CASE_PHASE_DIAGNOSIS, CASE_PHASE_TREATMENT, CASE_PHASE_RESULT

# INICIALIZACIÓN DE PYGAME

pygame.init()

# Crear ventana redimensionable
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Doctor RUSH")

# Superficie virtual donde se renderiza todo el juego (resolución base)
virtual_screen = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

# Variables para el escalado
current_window_width = BASE_WIDTH
current_window_height = BASE_HEIGHT

# Crear fuentes usando las configuraciones de ui_config
font = pygame.font.Font(None, FONT_SIZE_LARGE)
font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

# Crear fuentes para el modo Caso Clínico (más pequeñas)
clinical_case_font_title = pygame.font.Font(None, CLINICAL_CASE_FONT_TITLE)
clinical_case_font_normal = pygame.font.Font(None, CLINICAL_CASE_FONT_NORMAL)
clinical_case_font_small = pygame.font.Font(None, CLINICAL_CASE_FONT_SMALL)
clinical_case_font_tiny = pygame.font.Font(None, CLINICAL_CASE_FONT_TINY)

# CARGA DE RECURSOS (IMÁGENES Y FONDOS)

# Imagen de fondo seleccionada por el usuario (opcional)
user_bg_image = None
user_bg_name = None


# Función para cargar fondo según el escenario (bg1, bg2, bg3) o el seleccionado por el usuario
def load_background(scenario_index):
    """
    Carga el fondo correspondiente al escenario actual.
    Escenario 0 -> bg1.png
    Escenario 1 -> bg2.png
    Escenario 2 -> bg3.png
    """
    global user_bg_image

    # Si el usuario eligió una imagen de fondo personalizada, usarla siempre
    if user_bg_image is not None:
        return user_bg_image

    bg_files = ["bg1.png", "bg2.png", "bg3.png"]
    if 0 <= scenario_index < len(bg_files):
        bg_file = bg_files[scenario_index]
        bg_path = os.path.join(PATH_BACKGROUNDS, bg_file)
        try:
            bg_img = pygame.image.load(bg_path).convert()
            bg_img = pygame.transform.scale(bg_img, (BASE_WIDTH, BASE_HEIGHT))
            return bg_img
        except Exception as e:
            return None
    return None


# Cargar fondo inicial (escenario 0)
bg_image = load_background(0)

# Cargar fondo del menú
try:
    menu_bg_path = os.path.join(PATH_BACKGROUNDS, FILE_MENU_BG)
    menu_bg_image = pygame.image.load(menu_bg_path).convert()
    menu_bg_image = pygame.transform.scale(menu_bg_image, (BASE_WIDTH, BASE_HEIGHT))
except Exception as e:
    menu_bg_image = None

# Cargar fondo de la pantalla de pregunta
try:
    question_bg_path = os.path.join(PATH_BACKGROUNDS, FILE_QUESTION_BG)
    if os.path.exists(question_bg_path):
        question_bg_image = pygame.image.load(question_bg_path).convert()
        question_bg_image = pygame.transform.scale(question_bg_image, (BASE_WIDTH, BASE_HEIGHT))
    else:
        question_bg_image = None
except Exception as e:
    question_bg_image = None

# Cargar fondo del modo Caso Clínico
try:
    clinical_case_bg_path = os.path.join(PATH_BACKGROUNDS, FILE_CLINICAL_CASE_BG)
    if os.path.exists(clinical_case_bg_path):
        clinical_case_bg_image = pygame.image.load(clinical_case_bg_path).convert()
        clinical_case_bg_image = pygame.transform.scale(clinical_case_bg_image, (BASE_WIDTH, BASE_HEIGHT))
    else:
        clinical_case_bg_image = None
except Exception as e:
    clinical_case_bg_image = None

# Cargar fondo de pantalla inicial
try:
    initial_bg_path = os.path.join(PATH_BACKGROUNDS, FILE_INITIAL_BG)
    if os.path.exists(initial_bg_path):
        initial_bg_image = pygame.image.load(initial_bg_path).convert()
        initial_bg_image = pygame.transform.scale(initial_bg_image, (BASE_WIDTH, BASE_HEIGHT))
    else:
        initial_bg_image = None
except Exception as e:
    initial_bg_image = None

# CARGA DE ANIMACIONES

# Cargar todas las animaciones (jugador y pacientes)
try:
    animations = load_all_animations()
    player_animation = animations["player"]
    animations_green = animations["green"]
    animations_yellow = animations["yellow"]
    animations_orange = animations["orange"]
except Exception as e:
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

game_state = INITIAL_SCREEN  # Estado actual: INITIAL_SCREEN, MENU, PLAYING, QUESTION, GAME_OVER
player_name = ""  # Nombre del jugador actual
current_scenario = 0  # Escenario actual (0, 1, 2)
scenarios = [SCENARIO_1, SCENARIO_2, SCENARIO_3]  # Colores de fondo por escenario
score = 0  # Puntuación del jugador
patients_cured = 0  # Contador de pacientes curados en el nivel actual
total_patients_cured_session = 0  # Acumulado de pacientes curados en la partida (todos los niveles + modo infinito)
lives = INITIAL_LIVES  # Vidas actuales del jugador
menu_selected_option = 0  # Opción seleccionada en el menú (0: Doctor Rush, 1: Caso Clínico, 2: Estadísticas, 3: Salir)
doctor_rush_infinite_mode = False  # Modo infinito de Doctor Rush (después de completar nivel 3)

# Variables relacionadas con el modo Caso Clínico
clinical_case_data = None  # Datos del caso clínico actual
clinical_case_phase = CASE_PHASE_READING  # Fase actual del caso clínico
clinical_case_selected_tests = []  # Pruebas seleccionadas
clinical_case_test_index = 0  # Índice de selección en pruebas
clinical_case_diagnosis_index = 0  # Índice de selección en diagnóstico
clinical_case_treatment_index = 0  # Índice de selección en tratamiento
clinical_case_start_time = 0  # Tiempo de inicio del caso
clinical_case_test_score = 0  # Puntuación de pruebas
clinical_case_test_feedback = ""  # Feedback de pruebas
clinical_case_diagnosis_correct = False  # Si el diagnóstico fue correcto
clinical_case_final_score = 0  # Puntuación final
clinical_case_outcome_type = "incorrect"  # Tipo de resultado
clinical_case_total_points = 0  # Puntos acumulados totales
clinical_case_infinite_mode = False  # Modo infinito (después de ganar)
clinical_case_points_earned = 0  # Puntos ganados en el caso actual

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
player = Character(BASE_WIDTH // 2, BASE_HEIGHT // 2, player_animation, 100)

# Crear pacientes iniciales para el nivel 0
list_patients, patient_levels = create_patients(0, animations_green, animations_yellow, animations_orange,
                                                player_animation)

# Asegurarse de que hay pacientes (crear uno de respaldo si no hay)
if len(list_patients) == 0:
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

# Inicializar sistemas de usuario y sonido
user_manager = UserManager()
sound_manager = SoundManager()
sound_manager.load_all_sounds()
# Iniciar sonido de fondo global
sound_manager.start_global_background()

# Variables de sesión
session_start_time = 0

# Variables para control de sesiones de juego (para guardar estadísticas al final)
current_mode_for_stats = None  # "doctor_rush" | "clinical_case" | None

# Función para escalar y mostrar la superficie virtual en la pantalla real
def render_to_screen():
    """Escala la superficie virtual a la ventana real con letterboxing."""
    global current_window_width, current_window_height
    
    # Calcular escala manteniendo relación de aspecto
    scale_x = current_window_width / BASE_WIDTH
    scale_y = current_window_height / BASE_HEIGHT
    scale = min(scale_x, scale_y)  # Usar la escala menor para mantener aspecto
    
    # Calcular tamaño escalado
    scaled_width = int(BASE_WIDTH * scale)
    scaled_height = int(BASE_HEIGHT * scale)
    
    # Escalar superficie virtual (sin smoothscale para mantener pixel art)
    scaled_surface = pygame.transform.scale(virtual_screen, (scaled_width, scaled_height))
    
    # Limpiar pantalla real
    screen.fill((0, 0, 0))
    
    # Calcular posición centrada (letterboxing)
    offset_x = (current_window_width - scaled_width) // 2
    offset_y = (current_window_height - scaled_height) // 2
    
    # Dibujar superficie escalada centrada
    screen.blit(scaled_surface, (offset_x, offset_y))
    
    pygame.display.flip()

# LOOP PRINCIPAL DEL JUEGO

run = True
while run:
    # Controlar la velocidad del juego (FPS)
    clock.tick(FPS)

    # Obtener todos los eventos
    events = pygame.event.get()
    
    # Manejar eventos de redimensionamiento
    for event in events:
        if event.type == pygame.VIDEORESIZE:
            current_window_width = event.w
            current_window_height = event.h
            screen = pygame.display.set_mode((current_window_width, current_window_height), pygame.RESIZABLE)

    # ESTADO: PANTALLA INICIAL (Input de nombre)
    
    if game_state == INITIAL_SCREEN:
        draw_initial_screen(virtual_screen, font, font_small, initial_bg_image, player_name)
        
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            else:
                action, new_name = handle_initial_screen_events(event, player_name)
                if action == "CONTINUE":
                    player_name = new_name
                    # Obtener o crear usuario: si el nombre ya existe en stats.json se carga
                    # su historial para que los puntos de Caso Clínico y Doctor Rush persistan.
                    user_manager.create_user(player_name)
                    session_start_time = pygame.time.get_ticks()
                    game_state = MENU
                    sound_manager.play_sound("menu_select")
                elif action == "BACKSPACE":
                    player_name = new_name
                elif action == "TEXT":
                    player_name = new_name
                elif action == "QUIT":
                    run = False

    # ESTADO: MENÚ PRINCIPAL

    elif game_state == MENU:
        # Mostrar en el menú el nombre del fondo seleccionado (si existe)
        draw_menu(virtual_screen, font, font_small, menu_bg_image, menu_selected_option)

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # Permitir al usuario cambiar la imagen de fondo usando las teclas de flecha izquierda/derecha
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    try:
                        bg_files = [f for f in os.listdir(PATH_BACKGROUNDS)
                                    if f.lower().endswith((".png", ".jpg", ".jpeg"))]
                    except Exception:
                        bg_files = []

                    if bg_files:
                        # Mantener índice seleccionado en un atributo global sencillo
                        if not hasattr(pygame, "_bg_index"):
                            pygame._bg_index = 0

                        if event.key == pygame.K_RIGHT:
                            pygame._bg_index = (pygame._bg_index + 1) % len(bg_files)
                        else:
                            pygame._bg_index = (pygame._bg_index - 1) % len(bg_files)

                        selected_file = bg_files[pygame._bg_index]
                        selected_path = os.path.join(PATH_BACKGROUNDS, selected_file)

                        try:
                            new_bg = pygame.image.load(selected_path).convert()
                            new_bg = pygame.transform.scale(new_bg, (BASE_WIDTH, BASE_HEIGHT))
                            # Actualizar fondo global seleccionado por el usuario
                            user_bg_image = new_bg
                            user_bg_name = selected_file
                            # Aplicar el nuevo fondo también a las pantallas de pregunta y caso clínico
                            question_bg_image = user_bg_image
                            clinical_case_bg_image = user_bg_image
                            menu_bg_image = user_bg_image
                        except Exception as e:
                            print(f"Error al cargar fondo personalizado '{selected_file}': {e}")
                    continue

                result = handle_menu_events(event, game_state, player, score, patients_cured, lives,
                                            current_scenario, create_patients, animations_green,
                                            animations_yellow, animations_orange, player_animation,
                                            menu_selected_option)
                # Reproducir sonido de navegación si cambió la opción seleccionada
                if result[8] != menu_selected_option and result[0] == game_state:
                    sound_manager.play_sound("menu_navigate")
                if result[0] == "QUIT":
                    run = False
                elif result[0] == PLAYING:
                    # Iniciar Doctor Rush
                    sound_manager.play_sound("menu_select")
                    sound_manager.play_music("doctor_rush_bg.mp3", loop=True, volume=SOUND_VOLUME_DOCTOR_RUSH_BG)
                    session_start_time = pygame.time.get_ticks()
                    current_mode_for_stats = "doctor_rush"
                    total_patients_cured_session = 0  # Reiniciar acumulado al iniciar nueva partida
                    game_state = result[0]
                    score = result[1]
                    patients_cured = result[2]
                    lives = result[3]
                    current_scenario = result[4]
                    list_patients = result[5]
                    patient_levels = result[6]
                    patients_cured_list = result[7]
                    menu_selected_option = result[8]
                    # Reposicionar jugador en el centro al iniciar nuevo juego
                    player.shape.center = (BASE_WIDTH // 2, BASE_HEIGHT // 2)
                elif result[0] == CLINICAL_CASE:
                    # Iniciar modo Caso Clínico
                    sound_manager.play_sound("menu_select")
                    sound_manager.play_music("clinical_case_bg.mp3", loop=True, volume=SOUND_VOLUME_CLINICAL_CASE_BG)
                    session_start_time = pygame.time.get_ticks()  # Guardamos el momento en que empieza la sesión de caso clínico
                    current_mode_for_stats = "clinical_case"      # Indicamos que el modo actual para estadísticas es caso clínico
                    game_state = result[0]
                    menu_selected_option = result[8]
                    # Resetear variables del caso clínico
                    from clinical_cases import reset_case_progression
                    reset_case_progression()  # Resetear progresión de casos
                    clinical_case_data = None                     # Sin caso cargado al inicio
                    clinical_case_phase = CASE_PHASE_READING      # Empezamos en fase de lectura
                    clinical_case_selected_tests = []             # Ninguna prueba seleccionada aún
                    clinical_case_test_index = 0                  # Índice de selección de pruebas en 0
                    clinical_case_diagnosis_index = 0             # Índice de diagnóstico en 0
                    clinical_case_treatment_index = 0             # Índice de tratamiento en 0
                    clinical_case_total_points = 0                # Reiniciamos puntos acumulados para esta partida de caso clínico
                    clinical_case_infinite_mode = False           # Modo infinito desactivado al iniciar una nueva partida
                elif result[0] == STATISTICS:
                    # Ir a estadísticas
                    sound_manager.play_sound("menu_select")
                    game_state = result[0]
                    menu_selected_option = result[8]
                else:
                    # Actualizar la opción seleccionada del menú
                    menu_selected_option = result[8]


    # ESTADO: JUGANDO (PANTALLA PRINCIPAL)

    elif game_state == PLAYING:
        # Cargar y dibujar fondo según el escenario actual
        bg_image = load_background(current_scenario)
        if bg_image:
            virtual_screen.blit(bg_image, (0, 0))
        else:
            virtual_screen.fill(scenarios[current_scenario])

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

        # Limitar movimiento dentro de la pantalla (usar resolución base)
        if player.shape.x < 0:
            player.shape.x = 0
        if player.shape.x > BASE_WIDTH - WIDTH_CHARACTER:
            player.shape.x = BASE_WIDTH - WIDTH_CHARACTER
        if player.shape.y < 0:
            player.shape.y = 0
        if player.shape.y > BASE_HEIGHT - HEIGHT_CHARACTER:
            player.shape.y = BASE_HEIGHT - HEIGHT_CHARACTER

        # Actualizar al jugador (los pacientes se quedan quietos, sin animación)
        player.update()
        # Los pacientes no se actualizan para que se queden quietos

        # Dibujar al jugador
        player.draw(virtual_screen)

        # Dibujar pacientes con distintivos
        draw_patients(virtual_screen, list_patients, patient_levels, patients_cured_list, player, font_small)

        # Mostrar puntuación y vidas (pacientes curados: acumulado de la partida + actual del nivel)
        total_cured_display = total_patients_cured_session + patients_cured
        text_score = font_small.render(
            f"Puntuación: {score} | Pacientes curados: {total_cured_display} ({patients_cured}/{len(list_patients)} nivel)", True, COLOR_WHITE)
        virtual_screen.blit(text_score, (10, 10))
        text_lives = font_small.render(f"Vidas: {lives}", True, (255, 0, 0))
        virtual_screen.blit(text_lives, (10, 35))
        
        # Mostrar nombre del jugador abajo de las vidas
        if player_name:
            text_player = font_small.render(f"Jugador: {player_name}", True, COLOR_WHITE)
            virtual_screen.blit(text_player, (10, 60))

        # Mostrar instrucciones
        text_instructions = font_small.render("WASD: Mover | E: Interactuar | ESC: Pausa", True, COLOR_WHITE)
        virtual_screen.blit(text_instructions, (10, BASE_HEIGHT - 30))

        # Verificar si se quedó sin vidas
        if lives <= 0:
            game_state = GAME_OVER

        # Verificar si todos
        # los pacientes están curados
        if patients_cured >= len(list_patients):
            total_patients_cured_session += patients_cured  # Acumular antes de resetear (6 por nivel; al terminar nivel 3 = 18)
            # Si llegamos al nivel 3 (escenario 2), mostrar mensaje de continuar/terminar
            if current_scenario == 2 and not doctor_rush_infinite_mode:
                # Mostrar pantalla de nivel completado (18 pacientes curados) y preguntar si continuar
                sound_manager.play_sound("level_complete")
                game_state = LEVEL_COMPLETE
            elif doctor_rush_infinite_mode:
                # Modo infinito: mantener escenario 3 y solo pacientes naranjas; el contador ya incluye los 18 + nuevos
                patients_cured = 0
                # Recrear solo pacientes naranjas en escenario 3
                list_patients, patient_levels = create_patients(2, animations_green,
                                                                animations_yellow, animations_orange, player_animation)
                patients_cured_list = [False] * len(list_patients)
                # Reposicionar jugador en el centro
                player.shape.center = (BASE_WIDTH // 2, BASE_HEIGHT // 2)
                # Resetear preguntas usadas para el escenario 3
                from questions import reset_questions_for_scenario
                reset_questions_for_scenario(2)
            else:
                # Cambiar de escenario
                sound_manager.play_sound("level_complete")
                current_scenario += 1
                patients_cured = 0
                # Recrear pacientes para el nuevo escenario
                list_patients, patient_levels = create_patients(current_scenario, animations_green,
                                                                animations_yellow, animations_orange, player_animation)
                patients_cured_list = [False] * len(list_patients)
                # Reposicionar jugador en el centro
                player.shape.center = (BASE_WIDTH // 2, BASE_HEIGHT // 2)
                # Resetear preguntas usadas para el nuevo escenario
                from questions import reset_questions_for_scenario
                reset_questions_for_scenario(current_scenario)

        for event in events:
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
                                                                                               pygame.time.get_ticks(),
                                                                                               current_scenario)
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
            draw_question_screen(virtual_screen, font, font_small, current_question, current_patient_level,
                                 question_start_time, question_time_limit, question_result, question_bg_image)

        if question_result is None and current_question is not None:
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        question_result, score, patients_cured, lives = check_answer(0, current_question["correcta"],
                                                                                     current_patient_level, score,
                                                                                     patients_cured, lives)
                        question_result_time = pygame.time.get_ticks()
                        if question_result:
                            sound_manager.play_sound("answer_correct")
                        else:
                            sound_manager.play_sound("answer_incorrect")
                    if event.key == pygame.K_2:
                        question_result, score, patients_cured, lives = check_answer(1, current_question["correcta"],
                                                                                     current_patient_level, score,
                                                                                     patients_cured, lives)
                        question_result_time = pygame.time.get_ticks()
                        if question_result:
                            sound_manager.play_sound("answer_correct")
                        else:
                            sound_manager.play_sound("answer_incorrect")
                    if event.key == pygame.K_3:
                        question_result, score, patients_cured, lives = check_answer(2, current_question["correcta"],
                                                                                     current_patient_level, score,
                                                                                     patients_cured, lives)
                        question_result_time = pygame.time.get_ticks()
                        if question_result:
                            sound_manager.play_sound("answer_correct")
                        else:
                            sound_manager.play_sound("answer_incorrect")
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

            for event in events:
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
        draw_pause(virtual_screen, font, font_small)

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # ESPACIO: continuar jugando donde estabas
                if event.key == pygame.K_SPACE:
                    game_state = PLAYING
                # ESC: salir al menú principal
                if event.key == pygame.K_ESCAPE:
                    # El jugador abandona la partida de Doctor Rush desde la pausa:
                    # guardar estadísticas acumuladas de esta sesión en un solo registro.
                    if current_mode_for_stats == "doctor_rush" and session_start_time > 0:
                        play_time = (pygame.time.get_ticks() - session_start_time) // 1000
                        user_manager.add_play_time(play_time)
                        user_manager.update_doctor_rush_score(score)
                        user_manager.add_game_result("doctor_rush", score, patients_cured=total_patients_cured_session)
                        user_manager.increment_games_played()
                        user_manager.save_stats()
                        current_mode_for_stats = None
                        session_start_time = 0

                    game_state = MENU
                    menu_selected_option = 0  # Resetear opción seleccionada al volver al menú

    # ESTADO: NIVEL COMPLETADO (al llegar al nivel 3)
    elif game_state == LEVEL_COMPLETE:
        # Dibujar pantalla de nivel completado (18 pacientes curados = 3 niveles x 6)
        draw_level_complete(virtual_screen, font, font_small, score, total_patients_cured_session)

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # ESPACIO: continuar jugando en modo infinito (escenario 3, solo pacientes naranjas)
                if event.key == pygame.K_SPACE:
                    # Activar modo infinito
                    doctor_rush_infinite_mode = True
                    # Mantener escenario 3 y solo pacientes naranjas
                    current_scenario = 2
                    patients_cured = 0
                    list_patients, patient_levels = create_patients(2, animations_green,
                                                                    animations_yellow, animations_orange,
                                                                    player_animation)
                    patients_cured_list = [False] * len(list_patients)
                    player.shape.center = (BASE_WIDTH // 2, BASE_HEIGHT // 2)
                    # Resetear preguntas usadas para el escenario 3
                    from questions import reset_questions_for_scenario
                    reset_questions_for_scenario(2)
                    game_state = PLAYING
                    session_start_time = pygame.time.get_ticks()
                # ESC: terminar partida y volver al menú
                if event.key == pygame.K_ESCAPE:
                    # Guardar estadísticas
                    if current_mode_for_stats == "doctor_rush" and session_start_time > 0:
                        play_time = (pygame.time.get_ticks() - session_start_time) // 1000
                        user_manager.add_play_time(play_time)
                        user_manager.update_doctor_rush_score(score)
                        user_manager.add_game_result("doctor_rush", score, patients_cured=total_patients_cured_session)
                        user_manager.increment_games_played()
                        user_manager.save_stats()
                        current_mode_for_stats = None
                        session_start_time = 0
                    
                    sound_manager.stop_music()
                    game_state = MENU
                    menu_selected_option = 0  # Resetear opción seleccionada al volver al menú

    # ESTADO: GAME OVER (JUEGO TERMINADO)
    elif game_state == GAME_OVER:
        draw_game_over(virtual_screen, font, font_small, score, total_patients_cured_session + patients_cured)

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Guardar estadísticas
                    if current_mode_for_stats == "doctor_rush" and session_start_time > 0:
                        play_time = (pygame.time.get_ticks() - session_start_time) // 1000
                        user_manager.add_play_time(play_time)
                        user_manager.update_doctor_rush_score(score)
                        user_manager.add_game_result("doctor_rush", score, patients_cured=total_patients_cured_session)
                        user_manager.increment_games_played()
                        user_manager.save_stats()
                        current_mode_for_stats = None
                        session_start_time = 0
                    
                    sound_manager.stop_music()
                    game_state = MENU
                    menu_selected_option = 0  # Resetear opción seleccionada al volver al menú
                if event.key == pygame.K_ESCAPE:
                    run = False

    # ESTADO: CASO CLÍNICO
    elif game_state == CLINICAL_CASE:
        # Inicializar caso si es necesario
        if clinical_case_data is None:
            clinical_case_data = get_random_case(clinical_case_infinite_mode)
            clinical_case_phase = CASE_PHASE_READING
            clinical_case_start_time = pygame.time.get_ticks()
            clinical_case_selected_tests = []
            clinical_case_test_index = 0
            clinical_case_diagnosis_index = 0
            clinical_case_treatment_index = 0

        # Marcador en pantalla: puntos acumulados (variable clinical_case_total_points, no se reinicia al cambiar de fase)
        if not clinical_case_infinite_mode:
            from clinical_cases import POINTS_TO_WIN
            points_text = clinical_case_font_normal.render(f"Puntos: {clinical_case_total_points}/{POINTS_TO_WIN}", True, COLOR_WHITE)
            virtual_screen.blit(points_text, (BASE_WIDTH - points_text.get_width() - 10, 10))
        
        # Dibujar según la fase actual
        if clinical_case_phase == CASE_PHASE_READING:
            draw_clinical_case_reading(virtual_screen, clinical_case_font_title, clinical_case_font_normal, clinical_case_data, clinical_case_bg_image, player_name)
        elif clinical_case_phase == CASE_PHASE_TESTS:
            draw_clinical_case_tests(virtual_screen, clinical_case_font_title, clinical_case_font_normal, clinical_case_selected_tests, clinical_case_test_index, clinical_case_bg_image, player_name)
        elif clinical_case_phase == CASE_PHASE_RESULTS:
            draw_clinical_case_results(virtual_screen, clinical_case_font_title, clinical_case_font_normal, clinical_case_data, clinical_case_selected_tests, clinical_case_bg_image, player_name)
        elif clinical_case_phase == CASE_PHASE_DIAGNOSIS:
            draw_clinical_case_diagnosis(virtual_screen, clinical_case_font_title, clinical_case_font_normal, clinical_case_data, clinical_case_diagnosis_index, clinical_case_bg_image, player_name)
        elif clinical_case_phase == CASE_PHASE_TREATMENT:
            draw_clinical_case_treatment(virtual_screen, clinical_case_font_title, clinical_case_font_normal, clinical_case_data, clinical_case_treatment_index, clinical_case_bg_image, player_name)
        elif clinical_case_phase == CASE_PHASE_RESULT:
            treatment_correct = False
            if clinical_case_data and "treatments" in clinical_case_data:
                if clinical_case_treatment_index < len(clinical_case_data["treatments"]):
                    treatment_correct = clinical_case_data["treatments"][clinical_case_treatment_index]["correct"]
            draw_clinical_case_final(virtual_screen, clinical_case_font_title, clinical_case_font_normal, clinical_case_data,
                                    clinical_case_test_score, clinical_case_test_feedback,
                                    clinical_case_diagnosis_correct,
                                    treatment_correct,
                                    clinical_case_final_score, clinical_case_outcome_type, clinical_case_bg_image,
                                    clinical_case_points_earned, clinical_case_total_points, clinical_case_infinite_mode, player_name)

        # Manejar eventos
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # ESC: Pausar el caso clínico
                if event.key == pygame.K_ESCAPE:
                    game_state = CLINICAL_CASE_PAUSE
                else:
                    result = handle_clinical_case_events(
                        event, clinical_case_phase, clinical_case_data,
                        clinical_case_selected_tests, clinical_case_test_index,
                        clinical_case_diagnosis_index, clinical_case_treatment_index,
                        clinical_case_start_time, clinical_case_test_score, clinical_case_diagnosis_correct
                    )

                    new_phase = result[0]
                    updated_data = result[1] if len(result) > 1 else {}

                    # Actualizar fase y datos
                    if new_phase == "MENU":
                        # Guardado persistente: al volver al menú se guardan los puntos del Caso Clínico
                        # en el historial del usuario (add_game_result) y en disco (save_stats).
                        if session_start_time > 0:
                            play_time = (pygame.time.get_ticks() - session_start_time) // 1000
                            user_manager.add_play_time(play_time)
                            user_manager.update_clinical_case_score(clinical_case_total_points)
                            user_manager.add_game_result("clinical_case", clinical_case_total_points)
                            user_manager.increment_games_played()
                            user_manager.save_stats()
                            if __debug__:
                                print(f"[Caso Clínico] Guardado al volver al menú: puntos={clinical_case_total_points}")
                            current_mode_for_stats = None
                            session_start_time = 0
                        
                        sound_manager.stop_music()
                        game_state = MENU
                        menu_selected_option = 0
                        # Resetear variables del caso clínico
                        clinical_case_data = None
                        clinical_case_phase = CASE_PHASE_READING
                        clinical_case_selected_tests = []
                        clinical_case_test_index = 0
                        clinical_case_diagnosis_index = 0
                        clinical_case_treatment_index = 0
                    else:
                        old_phase = clinical_case_phase
                        clinical_case_phase = new_phase
                        
                        # Sonidos para cambios de fase y selecciones
                        if new_phase == CASE_PHASE_TESTS and old_phase == CASE_PHASE_READING:
                            sound_manager.play_sound("clinical_select")
                        elif new_phase == CASE_PHASE_RESULTS and old_phase == CASE_PHASE_TESTS:
                            sound_manager.play_sound("clinical_select")
                        elif new_phase == CASE_PHASE_DIAGNOSIS and old_phase == CASE_PHASE_RESULTS:
                            sound_manager.play_sound("clinical_select")
                        elif new_phase == CASE_PHASE_TREATMENT and old_phase == CASE_PHASE_DIAGNOSIS:
                            # Sonido según si el diagnóstico fue correcto
                            if "diagnosis_correct" in updated_data:
                                if updated_data["diagnosis_correct"]:
                                    sound_manager.play_sound("diagnosis_correct")
                                else:
                                    sound_manager.play_sound("diagnosis_incorrect")
                        elif new_phase == CASE_PHASE_RESULT and old_phase == CASE_PHASE_TREATMENT:
                            sound_manager.play_sound("clinical_case_complete")
                        
                        # Sonido para navegación en selecciones
                        if "test_selection_index" in updated_data or "diagnosis_index" in updated_data or "treatment_index" in updated_data:
                            sound_manager.play_sound("clinical_select")
                        
                        # Actualizar datos según la fase
                        if "selected_tests" in updated_data:
                            clinical_case_selected_tests = updated_data["selected_tests"]
                        if "test_selection_index" in updated_data:
                            clinical_case_test_index = updated_data["test_selection_index"]
                        if "diagnosis_index" in updated_data:
                            clinical_case_diagnosis_index = updated_data["diagnosis_index"]
                        if "treatment_index" in updated_data:
                            clinical_case_treatment_index = updated_data["treatment_index"]
                        if "test_score" in updated_data:
                            clinical_case_test_score = updated_data["test_score"]
                        if "test_feedback" in updated_data:
                            clinical_case_test_feedback = updated_data["test_feedback"]
                        if "diagnosis_correct" in updated_data:
                            clinical_case_diagnosis_correct = updated_data["diagnosis_correct"]
                        if "final_score" in updated_data:
                            clinical_case_final_score = updated_data["final_score"]
                        if "outcome_type" in updated_data:
                            clinical_case_outcome_type = updated_data["outcome_type"]
                        # Incremento de puntos: cada acierto (diagnóstico + tratamiento) suma al total
                        if "points_earned" in updated_data:
                            clinical_case_points_earned = updated_data["points_earned"]
                            clinical_case_total_points += clinical_case_points_earned
                            if __debug__:
                                print(f"[Caso Clínico] Total acumulado: {clinical_case_total_points}/15 (sumados +{clinical_case_points_earned})")
                            if not clinical_case_infinite_mode:
                                from clinical_cases import POINTS_TO_WIN
                                if clinical_case_total_points >= POINTS_TO_WIN:
                                    game_state = CLINICAL_CASE_VICTORY
                        if new_phase == "NEXT_CASE":
                            # Siguiente caso: NO se reinicia clinical_case_total_points (se mantiene el acumulado)
                            if session_start_time > 0:
                                case_time = (pygame.time.get_ticks() - clinical_case_start_time) // 1000
                                user_manager.add_play_time(case_time)
                            clinical_case_data = get_random_case(clinical_case_infinite_mode)
                            clinical_case_phase = CASE_PHASE_READING
                            clinical_case_start_time = pygame.time.get_ticks()
                            clinical_case_selected_tests = []
                            clinical_case_test_index = 0
                            clinical_case_diagnosis_index = 0
                            clinical_case_treatment_index = 0
                            clinical_case_test_score = 0
                            clinical_case_test_feedback = ""
                            clinical_case_diagnosis_correct = False
                            clinical_case_final_score = 0
                            clinical_case_outcome_type = "incorrect"
                            clinical_case_points_earned = 0

    # ESTADO: PAUSA EN CASO CLÍNICO
    elif game_state == CLINICAL_CASE_PAUSE:
        # Pantalla completamente negra (sin mostrar fondo del caso clínico)
        virtual_screen.fill(COLOR_BACKGROUND)
        
        # Dibujar mensaje de pausa
        from utils import draw_text_centered
        draw_text_centered(virtual_screen, "PAUSA", clinical_case_font_title, COLOR_WHITE, 200)
        draw_text_centered(virtual_screen, "Presiona ESPACIO para continuar", clinical_case_font_normal, COLOR_GREEN, 280)
        draw_text_centered(virtual_screen, "Presiona ESC para volver al menú", clinical_case_font_normal, COLOR_WHITE, 320)

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # ESPACIO: continuar donde estabas
                if event.key == pygame.K_SPACE:
                    game_state = CLINICAL_CASE
                # ESC: salir al menú principal
                elif event.key == pygame.K_ESCAPE:
                    # Guardado persistente: al salir desde pausa se guardan los puntos en historial y disco
                    if session_start_time > 0:
                        play_time = (pygame.time.get_ticks() - session_start_time) // 1000
                        user_manager.add_play_time(play_time)
                        user_manager.update_clinical_case_score(clinical_case_total_points)
                        user_manager.add_game_result("clinical_case", clinical_case_total_points)
                        user_manager.increment_games_played()
                        user_manager.save_stats()
                        current_mode_for_stats = None
                        session_start_time = 0
                    
                    sound_manager.stop_music()
                    sound_manager.start_global_background()
                    game_state = MENU
                    menu_selected_option = 0
                    clinical_case_data = None
                    clinical_case_phase = CASE_PHASE_READING
                    clinical_case_selected_tests = []
                    clinical_case_test_index = 0
                    clinical_case_diagnosis_index = 0
                    clinical_case_treatment_index = 0
                    clinical_case_test_score = 0
                    clinical_case_test_feedback = ""
                    clinical_case_diagnosis_correct = False
                    clinical_case_final_score = 0
                    clinical_case_outcome_type = "incorrect"

    # ESTADO: VICTORIA EN CASO CLÍNICO
    elif game_state == CLINICAL_CASE_VICTORY:
        draw_clinical_case_victory(virtual_screen, clinical_case_font_title, clinical_case_font_normal, 
                                   clinical_case_total_points, clinical_case_bg_image, player_name)
        
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Continuar en modo infinito
                    clinical_case_infinite_mode = True
                    game_state = CLINICAL_CASE
                    # Iniciar nuevo caso (solo casos difíciles en modo infinito)
                    clinical_case_data = get_random_case(True)
                    clinical_case_phase = CASE_PHASE_READING
                    clinical_case_start_time = pygame.time.get_ticks()
                    clinical_case_selected_tests = []
                    clinical_case_test_index = 0
                    clinical_case_diagnosis_index = 0
                    clinical_case_treatment_index = 0
                    clinical_case_test_score = 0
                    clinical_case_test_feedback = ""
                    clinical_case_diagnosis_correct = False
                    clinical_case_final_score = 0
                    clinical_case_outcome_type = "incorrect"
                    clinical_case_points_earned = 0
                elif event.key == pygame.K_ESCAPE:
                    # Guardado persistente: al salir desde victoria se guardan los puntos en historial y disco
                    if session_start_time > 0:
                        play_time = (pygame.time.get_ticks() - session_start_time) // 1000
                        user_manager.add_play_time(play_time)
                        user_manager.update_clinical_case_score(clinical_case_total_points)
                        user_manager.add_game_result("clinical_case", clinical_case_total_points)
                        user_manager.increment_games_played()
                        user_manager.save_stats()
                        if __debug__:
                            print(f"[Caso Clínico] Guardado al salir desde victoria: puntos={clinical_case_total_points}")
                        current_mode_for_stats = None
                        session_start_time = 0
                    
                    sound_manager.stop_music()
                    sound_manager.start_global_background()
                    game_state = MENU
                    menu_selected_option = 0
                    clinical_case_data = None
                    clinical_case_phase = CASE_PHASE_READING
                    clinical_case_selected_tests = []
                    clinical_case_test_index = 0
                    clinical_case_diagnosis_index = 0
                    clinical_case_treatment_index = 0
                    clinical_case_total_points = 0
                    clinical_case_infinite_mode = False
                    clinical_case_points_earned = 0

    # ESTADO: ESTADÍSTICAS
    elif game_state == STATISTICS:
        # Cargar estadísticas del top 10
        top_stats = user_manager.get_top_stats(10)
        draw_statistics(virtual_screen, font, font_small, menu_bg_image, top_stats)
        
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                result = handle_statistics_events(event)
                if result == "MENU":
                    game_state = MENU
                    menu_selected_option = 0

    # Renderizar superficie virtual a la pantalla real
    render_to_screen()

# Guardar estadísticas finales antes de salir
if user_manager.current_user and session_start_time > 0:
    play_time = (pygame.time.get_ticks() - session_start_time) // 1000        # Calculamos los segundos de juego de la última sesión
    user_manager.add_play_time(play_time)                                     # Sumamos este tiempo al total del usuario
    # Guardar última sesión según el modo activo (si todavía está marcado)
    if current_mode_for_stats == "doctor_rush":                               # Si el último modo activo fue Doctor Rush
        user_manager.update_doctor_rush_score(score)                          # Actualizamos el mejor puntaje de Doctor Rush
        user_manager.add_game_result("doctor_rush", score, patients_cured=total_patients_cured_session)                    # Registramos una partida de Doctor Rush en el historial
    elif current_mode_for_stats == "clinical_case":                           # Si el último modo activo fue Caso Clínico
        user_manager.update_clinical_case_score(clinical_case_total_points)   # Actualizamos el mejor puntaje de Caso Clínico
        user_manager.add_game_result("clinical_case", clinical_case_total_points)  # Registramos una partida de Caso Clínico en el historial
    user_manager.save_stats()                                                 # Guardamos todas las estadísticas en disco

pygame.quit()
