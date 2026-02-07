import pygame
import os
from constants import SCALE_CHARACTER, SCALE_PATIENT
from utils import scale_img, count_elements, name_folder


# Función para cargar animaciones de pacientes por nivel
def load_patient_animations(level):
    """
    Carga las imágenes de pacientes para un nivel específico.
    Ahora busca una sola imagen por carpeta (Patient1.png) ya que los pacientes no se mueven.

    Parámetros:
    - level: Nivel del paciente ("green", "yellow", "orange")

    Retorna:
    - Lista de listas de imágenes, donde cada sublista es una animación (con una sola imagen)
    """
    directory_patients = f"assets/image/character/patients_level/{level}"
    if not os.path.exists(directory_patients):
        print(f"Directorio no encontrado: {directory_patients}")
        return []

    type_patients = name_folder(directory_patients)
    print(f"Cargando pacientes de nivel '{level}': encontré {len(type_patients)} carpetas")
    animation_patients = []

    for eni in type_patients:
        list_temp = []
        route_temp = f"{directory_patients}/{eni}"

        # Buscar cualquier archivo .png en la carpeta (ya no son sprites, solo una imagen)
        image_loaded = False

        # Primero intentar nombres comunes
        possible_names = [
            "Patient1.png", "patient1.png", "Patient1.PNG", "PATIENT1.PNG",
            "Patient.png", "patient.png", "Patient.PNG", "PATIENT.PNG",
            "image.png", "Image.png", "IMAGE.PNG",
            "sprite.png", "Sprite.png", "SPRITE.PNG"
        ]

        for img_name in possible_names:
            img_path = f"{route_temp}/{img_name}"
            if os.path.exists(img_path):
                try:
                    img_patient = pygame.image.load(img_path).convert_alpha()
                    img_patient = scale_img(img_patient, SCALE_PATIENT)
                    list_temp.append(img_patient)
                    print(f"✓ Paciente cargado desde {img_path}")
                    image_loaded = True
                    break
                except Exception as e:
                    print(f"Error al cargar {img_path}: {e}")

        # Si no se encontró con nombres comunes, buscar cualquier archivo .png en la carpeta
        if not image_loaded:
            try:
                files_in_folder = os.listdir(route_temp)
                png_files = [f for f in files_in_folder if f.lower().endswith('.png')]

                if png_files:
                    # Usar el primer archivo .png encontrado
                    img_path = os.path.join(route_temp, png_files[0])
                    try:
                        img_patient = pygame.image.load(img_path).convert_alpha()
                        img_patient = scale_img(img_patient, SCALE_PATIENT)
                        list_temp.append(img_patient)
                        print(f"✓ Paciente cargado desde {img_path} (archivo encontrado: {png_files[0]})")
                        image_loaded = True
                    except Exception as e:
                        print(f"Error al cargar {img_path}: {e}")
                else:
                    print(f"⚠ No se encontraron archivos .png en {route_temp}")
                    print(f"  Archivos encontrados: {files_in_folder}")
            except Exception as e:
                print(f"Error al leer carpeta {route_temp}: {e}")

        # Si aún no se cargó ninguna imagen, crear un placeholder
        if not image_loaded:
            placeholder = pygame.Surface((27, 27))
            placeholder.fill((0, 255, 0) if level == "green" else (255, 255, 0) if level == "yellow" else (255, 165, 0))
            list_temp.append(placeholder)
            print(f"⚠ Placeholder creado para {route_temp} (no se encontró imagen)")

        if list_temp:  # Solo agregar si se cargó al menos una imagen o placeholder
            animation_patients.append(list_temp)

    return animation_patients


# Función para cargar animación del jugador
def load_player_animation():
    animation = []
    for i in range(6):
        img = pygame.image.load(f"assets/image/character/player/Player_{i}.png")
        img = scale_img(img, SCALE_CHARACTER)
        animation.append(img)
    return animation


# Función para cargar todas las animaciones
def load_all_animations():
    player_animation = load_player_animation()
    animations_green = load_patient_animations("green")
    animations_yellow = load_patient_animations("yellow")
    animations_orange = load_patient_animations("orange")

    return {
        "player": player_animation,
        "green": animations_green,
        "yellow": animations_yellow,
        "orange": animations_orange
    }
