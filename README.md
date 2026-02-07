# 🩺 Doctor Rush

**Doctor Rush** es un juego educativo médico desarrollado en **Python con Pygame**, que combina acción y aprendizaje a través de dos modos de juego: un modo arcade dinámico y un modo educativo basado en **casos clínicos reales**.

El proyecto está orientado a estudiantes de medicina y profesionales de la salud, integrando entretenimiento con el refuerzo de conceptos médicos fundamentales.

---

## 🎮 Modos de Juego

### 🏃 Doctor Rush (Modo Acción)
- Movimiento del personaje con **WASD**
- Atención de pacientes según nivel de urgencia
- Sistema de preguntas médicas cronometradas
- Sistema de vidas y puntuación
- 3 niveles progresivos + modo infinito

**Niveles de urgencia**
- 🟢 Verde
- 🟡 Amarillo
- 🟠 Naranja

---

### 🧠 Caso Clínico (Modo Educativo)
- Lectura completa del caso clínico
- Selección de pruebas médicas
- Diagnóstico
- Tratamiento
- Evaluación basada en decisiones clínicas

Incluye **13 casos clínicos** inspirados en escenarios médicos reales.

---

## ⭐ Características Principales

- Juego educativo con enfoque médico  
- Sistema de progresión por niveles  
- Música de fondo y efectos de sonido  
- Guardado automático de estadísticas en formato JSON  
- Interfaz redimensionable  
- Más de **60 preguntas médicas**  

---

## 🏗️ Estructura del Proyecto

doctor_rush/
│
├── main.py # Punto de entrada del juego
│
├── core/ # Lógica principal del juego
│ ├── game_states.py # Control de estados y pantallas
│ ├── character.py # Clases de jugador y pacientes
│ ├── patient_manager.py # Gestión de pacientes
│
├── systems/ # Sistemas del juego
│ ├── questions.py # Preguntas médicas
│ ├── clinical_cases.py # Casos clínicos
│ ├── sound_manager.py # Gestión de audio
│ ├── user_manager.py # Usuarios y estadísticas
│
├── config/ # Configuración general
│ ├── constants.py # Constantes globales
│ ├── ui_config.py # Configuración de interfaz
│
├── utils.py # Funciones auxiliares
├── stats.json # Datos persistentes de jugadores
│
└── assets/ # Recursos del juego
├── sounds/ # Archivos de audio
└── image/
├── backgrounds/ # Fondos
└── character/
├── player/ # Sprites del jugador
└── patients_level/
├── green/
├── yellow/
└── orange/



---

## 🔊 Sistema de Audio

**Música de fondo**
- Música global
- Tema para Doctor Rush
- Tema para Caso Clínico

**Efectos de sonido**
- Navegación de menú
- Respuestas correctas e incorrectas
- Eventos del juego (niveles, diagnósticos, victoria)

---

## 📊 Sistema de Estadísticas

Los datos se almacenan automáticamente en `stats.json`:

- Nombre del jugador  
- Mejores puntuaciones  
- Historial de partidas  
- Tiempo total de juego  
- Número de partidas jugadas  

---

## 🚀 Instalación y Ejecución

### Requisitos
- Python **3.7 o superior**
- Pygame **2.0 o superior**

## 🎮 Vista previa
Ingreso del jugador:
<img width="808" height="637" alt="image" src="https://github.com/user-attachments/assets/826b044a-0376-4103-95a0-86aee9905439" />
Menú:
<img width="806" height="636" alt="image" src="https://github.com/user-attachments/assets/67b6983e-5364-4d9d-9c5b-4f0e2f239a73" />
Doctor Rush:
<img width="810" height="640" alt="image" src="https://github.com/user-attachments/assets/ee72a9e8-427b-4f87-ab97-b321af90250b" />
Caso clínico:
<img width="808" height="641" alt="image" src="https://github.com/user-attachments/assets/ca04106f-3274-4d9c-ad5e-560fd1923ba6" />
Estadísticas:
<img width="808" height="642" alt="image" src="https://github.com/user-attachments/assets/05eef49a-7042-4ffc-94e5-b5e1016046d0" />

### Instalación
```bash
pip install pygame




