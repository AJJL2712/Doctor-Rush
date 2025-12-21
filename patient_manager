from character import Character
from constants import PATIENT_POSITIONS, PATIENT_ASSET_MAP
import pygame


# Helper: asegurar que haya suficientes animaciones; si faltan, se agregan placeholders
def ensure_animations(anim_list, needed, color):
    """
    Asegura que haya suficientes animaciones disponibles.
    Si hay menos animaciones que las necesarias, reutiliza las existentes.
    Si no hay ninguna, crea placeholders.

    Parámetros:
    - anim_list: Lista de animaciones disponibles
    - needed: Número mínimo de animaciones necesarias
    - color: Color para placeholders si no hay animaciones

    Retorna:
    - Lista con al menos 'needed' animaciones
    """
    result = list(anim_list)
    if len(result) == 0:
        # Crear al menos una animación placeholder del color indicado
        surf = pygame.Surface((27, 27))
        surf.fill(color)
        result.append([surf])
        print(f"Advertencia: No hay animaciones disponibles, creando placeholder de color {color}")
    # Si hay animaciones pero menos de las necesarias, reutilizar las existentes
    while len(result) < needed:
        result.append(result[len(result) % len(anim_list)] if len(anim_list) > 0 else result[-1])
    return result


# Función para crear pacientes según el nivel del escenario
def create_patients(scenario_level, animations_green, animations_yellow, animations_orange, player_animation):
    list_patients = []
    patient_levels = []
    desired = 6

    # Nivel 1 (scenario_level 0): 6 verdes
    if scenario_level == 0:
        pos_list = PATIENT_POSITIONS.get("green", [])
        asset_map = PATIENT_ASSET_MAP.get("level1_green", [])

        for idx in range(desired):
            anim_idx = asset_map[idx] if idx < len(asset_map) else idx
            anim = animations_green[anim_idx % len(animations_green)] if animations_green else player_animation

            if idx < len(pos_list):
                x, y = pos_list[idx]
            else:
                x, y = pos_list[-1] if pos_list else (100 + idx * 80, 150)

            list_patients.append(Character(x, y, anim, 100))
            patient_levels.append("green")

    # Nivel 2 (scenario_level 1): 6 amarillos
    elif scenario_level == 1:
        pos_list = PATIENT_POSITIONS.get("yellow", [])
        asset_map = PATIENT_ASSET_MAP.get("level2_yellow", [])

        for idx in range(desired):
            anim_idx = asset_map[idx] if idx < len(asset_map) else idx
            anim = animations_yellow[anim_idx % len(animations_yellow)] if animations_yellow else player_animation

            if idx < len(pos_list):
                x, y = pos_list[idx]
            else:
                x, y = pos_list[-1] if pos_list else (100 + idx * 80, 150)

            list_patients.append(Character(x, y, anim, 100))
            patient_levels.append("yellow")

    # Nivel 3 (scenario_level 2): 6 naranjas
    elif scenario_level == 2:
        pos_list = PATIENT_POSITIONS.get("orange", [])
        asset_map = PATIENT_ASSET_MAP.get("level3_orange", [])

        for idx in range(desired):
            anim_idx = asset_map[idx] if idx < len(asset_map) else idx
            anim = animations_orange[anim_idx % len(animations_orange)] if animations_orange else player_animation

            if idx < len(pos_list):
                x, y = pos_list[idx]
            else:
                x, y = pos_list[-1] if pos_list else (100 + idx * 80, 150)

            list_patients.append(Character(x, y, anim, 100))
            patient_levels.append("orange")

    # Fallback: si llega un nivel no contemplado
    else:
        for idx in range(desired):
            x, y = (100 + idx * 80, 150)
            list_patients.append(Character(x, y, player_animation, 100))
            patient_levels.append("green")

    return list_patients, patient_levels

