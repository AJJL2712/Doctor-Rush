"""
Sistema de gestión de usuarios y estadísticas.
Maneja la persistencia de datos de usuarios en formato JSON.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

# Archivo donde se guardan las estadísticas
STATS_FILE = "stats.json"


class User:
    """Clase que representa un usuario y sus estadísticas."""
    
    def __init__(self, name: str):
        self.name = name
        self.doctor_rush_score = 0
        self.clinical_case_score = 0
        self.total_play_time = 0  # En segundos
        self.last_played = datetime.now().isoformat()
        self.games_played = 0
        # Historial de puntajes con fecha y juego
        self.score_history: List[Dict] = []  # Lista de {"game": "doctor_rush"|"clinical_case", "score": int, "date": str}
    
    def to_dict(self) -> Dict:
        """Convierte el usuario a diccionario para guardar."""
        return {
            "name": self.name,
            "doctor_rush_score": self.doctor_rush_score,
            "clinical_case_score": self.clinical_case_score,
            "total_play_time": self.total_play_time,
            "last_played": self.last_played,
            "games_played": self.games_played,
            "score_history": self.score_history
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Crea un usuario desde un diccionario."""
        user = cls(data.get("name", "Unknown"))
        user.doctor_rush_score = data.get("doctor_rush_score", 0)
        user.clinical_case_score = data.get("clinical_case_score", 0)
        user.total_play_time = data.get("total_play_time", 0)
        user.last_played = data.get("last_played", datetime.now().isoformat())
        user.games_played = data.get("games_played", 0)
        user.score_history = data.get("score_history", [])
        return user


class UserManager:
    """Gestor de usuarios y estadísticas."""
    
    def __init__(self):
        self.current_user: Optional[User] = None
        self.stats: List[Dict] = []
        self.load_stats()
    
    def create_user(self, name: str) -> User:
        """
        Obtiene o crea el usuario por nombre.
        Si el nombre ya existe en stats (cargados desde stats.json), se restaura ese usuario
        para no perder historial ni puntajes. Así los puntos de Caso Clínico y Doctor Rush
        se persisten correctamente al cerrar y volver a abrir el juego.
        """
        name_clean = name.strip() if name else ""
        for stat in self.stats:
            if stat.get("name", "").strip() == name_clean:
                self.current_user = User.from_dict(stat)
                return self.current_user
        self.current_user = User(name_clean or name)
        return self.current_user
    
    def set_current_user(self, user: User):
        """Establece el usuario actual."""
        self.current_user = user
    
    def update_doctor_rush_score(self, score: int):
        """
        Actualiza la mejor puntuación acumulada de Doctor Rush del usuario actual.
        
        Nota:
            Esta función **no** agrega entradas al historial de partidas.
            Para registrar una partida completada en el historial, usa
            `add_game_result("doctor_rush", score)` al finalizar la partida.
        """
        if self.current_user:
            if score > self.current_user.doctor_rush_score:
                self.current_user.doctor_rush_score = score
    
    def update_clinical_case_score(self, score: int):
        """
        Actualiza la mejor puntuación acumulada de Caso Clínico del usuario actual.
        
        Nota:
            Esta función **no** agrega entradas al historial de partidas.
            Para registrar una partida completada en el historial, usa
            `add_game_result("clinical_case", score)` al finalizar la partida.
        """
        if self.current_user:
            if score > self.current_user.clinical_case_score:
                self.current_user.clinical_case_score = score

    def add_game_result(self, game: str, score: int, patients_cured: Optional[int] = None):
        """
        Registra el resultado de UNA partida en el historial del usuario actual.
        Se registra siempre que haya usuario (incluyendo partidas con 0 puntos).
        Debe llamarse al salir de una partida (menú, pausa, victoria) para que
        los puntos de Caso Clínico y Doctor Rush aparezcan en Estadísticas.
        Persistencia: hay que llamar save_stats() después para escribir en disco.
        
        Args:
            game: "doctor_rush" o "clinical_case"
            score: Puntuación final de la partida (ej. 2, 3 o 5 por caso clínico acertado).
            patients_cured: Opcional; pacientes curados (solo Doctor Rush).
        """
        if self.current_user:
            entry = {
                "game": game,
                "score": score,
                "date": datetime.now().isoformat()
            }
            if patients_cured is not None:
                entry["patients_cured"] = patients_cured
            self.current_user.score_history.append(entry)
            if __debug__ and game == "clinical_case":
                print(f"[Estadísticas] add_game_result clinical_case score={score} (historial tiene {len(self.current_user.score_history)} entradas)")
    
    def add_play_time(self, seconds: int):
        """Añade tiempo de juego al usuario actual."""
        if self.current_user:
            self.current_user.total_play_time += seconds
    
    def increment_games_played(self):
        """Incrementa el contador de partidas jugadas."""
        if self.current_user:
            self.current_user.games_played += 1
            self.current_user.last_played = datetime.now().isoformat()
    
    def save_stats(self):
        """
        Guarda las estadísticas en stats.json (persistencia en disco).
        Actualiza la entrada del usuario actual en self.stats y escribe todo
        el listado en el archivo. Necesario después de add_game_result para
        que los puntos de Caso Clínico se reflejen en Estadísticas al reabrir.
        """
        if not self.current_user:
            return
        
        user_dict = self.current_user.to_dict()
        found = False
        for i, stat in enumerate(self.stats):
            if stat.get("name") == self.current_user.name:
                self.stats[i] = user_dict
                found = True
                break
        if not found:
            self.stats.append(user_dict)
        
        try:
            with open(STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
            if __debug__:
                n_clinical = sum(1 for e in self.current_user.score_history if e.get("game") == "clinical_case")
                print(f"[Estadísticas] save_stats OK: usuario '{self.current_user.name}', partidas Caso Clínico en historial: {n_clinical}")
        except Exception as e:
            print(f"Error al guardar estadísticas: {e}")
    
    def load_stats(self):
        """
        Carga las estadísticas desde stats.json al iniciar o al abrir Estadísticas.
        Si el archivo no existe, deja self.stats vacío. create_user usa estos
        datos para restaurar usuarios existentes y no perder historial.
        """
        if not os.path.exists(STATS_FILE):
            self.stats = []
            return
        
        try:
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                self.stats = json.load(f)
        except Exception as e:
            print(f"Error al cargar estadísticas: {e}")
            self.stats = []
    
    def get_all_stats(self) -> List[Dict]:
        """Retorna todas las estadísticas."""
        return self.stats.copy()
    
    def clear_all_stats(self):
        """Borra todas las estadísticas."""
        self.stats = []
        self.current_user = None
        try:
            if os.path.exists(STATS_FILE):
                os.remove(STATS_FILE)
        except Exception as e:
            print(f"Error al borrar estadísticas: {e}")
    
    def get_combined_stats(self) -> List[Dict]:
        """Retorna estadísticas combinadas de ambos modos de juego."""
        combined = []
        for stat in self.stats:
            combined.append({
                "name": stat.get("name", "Unknown"),
                "score": stat.get("doctor_rush_score", 0) + stat.get("clinical_case_score", 0),
                "time": stat.get("total_play_time", 0),
                "date": stat.get("last_played", ""),
                "doctor_rush_score": stat.get("doctor_rush_score", 0),
                "clinical_case_score": stat.get("clinical_case_score", 0),
                "total_play_time": stat.get("total_play_time", 0),
                "games_played": stat.get("games_played", 0)
            })
        # Ordenar por puntuación descendente
        combined.sort(key=lambda x: x["score"], reverse=True)
        return combined
    
    def get_top_stats(self, limit=10) -> List[Dict]:
        """Retorna las top N estadísticas ordenadas por puntuación total."""
        stats = []
        for stat in self.stats:
            total_score = stat.get("doctor_rush_score", 0) + stat.get("clinical_case_score", 0)
            stats.append({
                "name": stat.get("name", "Unknown"),
                "doctor_rush_score": stat.get("doctor_rush_score", 0),
                "clinical_case_score": stat.get("clinical_case_score", 0),
                "total_play_time": stat.get("total_play_time", 0),
                "games_played": stat.get("games_played", 0),
                "last_played": stat.get("last_played", ""),
                "score_history": stat.get("score_history", [])
            })
        # Ordenar por puntuación total descendente
        stats.sort(key=lambda x: x["doctor_rush_score"] + x["clinical_case_score"], reverse=True)
        return stats[:limit]
    
    def get_score_history(self, limit=20) -> List[Dict]:
        """Retorna el historial de puntajes de todos los usuarios, ordenado por fecha descendente."""
        all_history = []
        for stat in self.stats:
            name = stat.get("name", "Unknown")
            history = stat.get("score_history", [])
            for entry in history:
                all_history.append({
                    "name": name,
                    "game": entry.get("game", "unknown"),
                    "score": entry.get("score", 0),
                    "date": entry.get("date", ""),
                    "patients_cured": entry.get("patients_cured")
                })
        # Ordenar por fecha descendente (más reciente primero)
        all_history.sort(key=lambda x: x.get("date", ""), reverse=True)
        return all_history[:limit]
