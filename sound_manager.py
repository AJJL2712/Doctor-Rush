"""
Sistema de gestión de sonidos y música.
Maneja la carga y reproducción de efectos de sonido y música de fondo.
"""

import pygame
import os
from typing import Dict
from constants import (
    SOUND_VOLUME_GLOBAL_BG, SOUND_VOLUME_MENU_NAVIGATE, SOUND_VOLUME_MENU_SELECT,
    SOUND_VOLUME_DOCTOR_RUSH_BG, SOUND_VOLUME_ANSWER_CORRECT, SOUND_VOLUME_ANSWER_INCORRECT,
    SOUND_VOLUME_LEVEL_COMPLETE, SOUND_VOLUME_CLINICAL_CASE_BG, SOUND_VOLUME_CLINICAL_SELECT,
    SOUND_VOLUME_CLINICAL_CASE_COMPLETE, SOUND_VOLUME_DIAGNOSIS_CORRECT, SOUND_VOLUME_DIAGNOSIS_INCORRECT
)

# Ruta base para sonidos
PATH_SOUNDS = "assets/sounds"

# Nombres de archivos de sonido
SOUND_MENU_NAVIGATE = "menu_navigate.wav"
SOUND_MENU_SELECT = "menu_select.wav"
SOUND_DOCTOR_RUSH_BG = "doctor_rush_bg.mp3"
SOUND_ANSWER_CORRECT = "answer_correct.wav"
SOUND_ANSWER_INCORRECT = "answer_incorrect.wav"
SOUND_LEVEL_COMPLETE = "level_complete.wav"
SOUND_CLINICAL_CASE_BG = "clinical_case_bg.mp3"
SOUND_CLINICAL_SELECT = "clinical_select.wav"
SOUND_CLINICAL_CASE_COMPLETE = "clinical_case_complete.wav"
SOUND_DIAGNOSIS_CORRECT = "diagnosis_correct.wav"
SOUND_DIAGNOSIS_INCORRECT = "diagnosis_incorrect.wav"
SOUND_GLOBAL_BG = "global_bg.mp3"  # Sonido de fondo global


class SoundManager:
    """Gestor de sonidos y música."""
    
    def __init__(self):
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_playing = None
        self.music_volume = 0.5
        self.sound_volume = 0.7
        self.enabled = True
        
        # Inicializar mixer de pygame
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except Exception as e:
            print(f"Error al inicializar mixer: {e}")
            self.enabled = False
    
    def load_sound(self, filename: str, sound_name: str, volume: float = None) -> bool:
        """Carga un sonido desde archivo con volumen específico."""
        if not self.enabled:
            return False
        
        try:
            sound_path = os.path.join(PATH_SOUNDS, filename)
            if os.path.exists(sound_path):
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                # Usar volumen específico si se proporciona, sino usar el volumen por defecto
                if volume is not None:
                    self.sounds[sound_name].set_volume(volume)
                else:
                    self.sounds[sound_name].set_volume(self.sound_volume)
                return True
            else:
                print(f"Archivo de sonido no encontrado: {sound_path}")
                return False
        except Exception as e:
            print(f"Error al cargar sonido {filename}: {e}")
            return False
    
    def play_sound(self, sound_name: str):
        """Reproduce un efecto de sonido."""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        try:
            self.sounds[sound_name].play()
        except Exception as e:
            print(f"Error al reproducir sonido {sound_name}: {e}")
    
    def play_music(self, filename: str, loop: bool = True, volume: float = None):
        """Reproduce música de fondo con volumen específico."""
        if not self.enabled:
            return
        
        try:
            music_path = os.path.join(PATH_SOUNDS, filename)
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                # Usar volumen específico si se proporciona, sino usar el volumen por defecto
                if volume is not None:
                    pygame.mixer.music.set_volume(volume)
                else:
                    pygame.mixer.music.set_volume(self.music_volume)
                if loop:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.play()
                self.music_playing = filename
            else:
                print(f"Archivo de música no encontrado: {music_path}")
        except Exception as e:
            print(f"Error al reproducir música {filename}: {e}")
    
    def stop_music(self):
        """Detiene la música de fondo."""
        if self.enabled:
            try:
                pygame.mixer.music.stop()
                self.music_playing = None
            except Exception as e:
                print(f"Error al detener música: {e}")
    
    def set_music_volume(self, volume: float):
        """Establece el volumen de la música (0.0 a 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.enabled:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except:
                pass
    
    def set_sound_volume(self, volume: float):
        """Establece el volumen de los efectos (0.0 a 1.0)."""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def load_all_sounds(self):
        """Carga todos los sonidos del juego con sus volúmenes específicos."""
        self.load_sound(SOUND_MENU_NAVIGATE, "menu_navigate", SOUND_VOLUME_MENU_NAVIGATE)
        self.load_sound(SOUND_MENU_SELECT, "menu_select", SOUND_VOLUME_MENU_SELECT)
        self.load_sound(SOUND_ANSWER_CORRECT, "answer_correct", SOUND_VOLUME_ANSWER_CORRECT)
        self.load_sound(SOUND_ANSWER_INCORRECT, "answer_incorrect", SOUND_VOLUME_ANSWER_INCORRECT)
        self.load_sound(SOUND_LEVEL_COMPLETE, "level_complete", SOUND_VOLUME_LEVEL_COMPLETE)
        self.load_sound(SOUND_CLINICAL_SELECT, "clinical_select", SOUND_VOLUME_CLINICAL_SELECT)
        self.load_sound(SOUND_CLINICAL_CASE_COMPLETE, "clinical_case_complete", SOUND_VOLUME_CLINICAL_CASE_COMPLETE)
        self.load_sound(SOUND_DIAGNOSIS_CORRECT, "diagnosis_correct", SOUND_VOLUME_DIAGNOSIS_CORRECT)
        self.load_sound(SOUND_DIAGNOSIS_INCORRECT, "diagnosis_incorrect", SOUND_VOLUME_DIAGNOSIS_INCORRECT)

    def start_global_background(self):
        """Inicia el sonido de fondo global que se reproduce siempre."""
        if self.enabled:
            try:
                music_path = os.path.join(PATH_SOUNDS, SOUND_GLOBAL_BG)
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(SOUND_VOLUME_GLOBAL_BG)  # Usar volumen configurado
                    pygame.mixer.music.play(-1)  # Loop infinito
                else:
                    print(f"Archivo de música global no encontrado: {music_path}")
            except Exception as e:
                print(f"Error al reproducir música global {SOUND_GLOBAL_BG}: {e}")
