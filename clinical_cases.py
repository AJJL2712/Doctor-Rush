"""
Sistema de Casos Clínicos
Contiene casos clínicos reales y la lógica del juego de casos clínicos.
"""

import copy
import random
from constants import COLOR_WHITE, COLOR_GREEN, COLOR_RED, COLOR_BLUE

# FASES DEL JUEGO DE CASO CLÍNICO
CASE_PHASE_READING = 0  # Leyendo el caso
CASE_PHASE_TESTS = 1    # Eligiendo pruebas
CASE_PHASE_RESULTS = 2  # Viendo resultados de pruebas
CASE_PHASE_DIAGNOSIS = 3  # Eligiendo diagnóstico
CASE_PHASE_TREATMENT = 4  # Eligiendo tratamiento
CASE_PHASE_RESULT = 5   # Viendo resultado final

# DIFICULTADES Y PUNTUACIÓN
DIFFICULTY_EASY = "easy"
DIFFICULTY_MEDIUM = "medium"
DIFFICULTY_HARD = "hard"

POINTS_EASY = 2
POINTS_MEDIUM = 3
POINTS_HARD = 5
POINTS_TO_WIN = 15

# Tipos de pruebas disponibles
TEST_TYPES = {
    "ecg": "Electrocardiograma",
    "xray": "Rayos X",
    "blood": "Exámenes de sangre",
    "ct": "Tomografía",
    "observation": "Observación",
    "hospitalization": "Hospitalización inmediata"
}

# Casos clínicos predefinidos - ORDENADOS POR DIFICULTAD (fácil a difícil)
CLINICAL_CASES = [
    # ========== FÁCILES (2 puntos) ==========
    {
        "id": 1,
        "title": "Caso 1: Gripe en Niño",
        "difficulty": DIFFICULTY_EASY,
        "patient_data": {
            "name": "B.C.",
            "age": 6,
            "sex": "Masculino",
            "occupation": "Estudiante",
            "chief_complaint": "Fiebre y tos desde hace 2 días"
        },
        "history": {
            "personal": "Vacunas completas",
            "family": "Sano",
            "habits": "Normal",
            "medication": "Ninguna"
        },
        "symptoms": {
            "onset": "2 días",
            "duration": "Leve",
            "intensity": "Moderado",
            "worsening": "Actividad",
            "improving": "Reposo"
        },
        "physical_exam": {
            "vital_signs": "Temp: 38.5°C, FC: 100 lpm, FR: 22 rpm, SatO2: 98%",
            "findings": "Cuadro viral, sin signos de complicación"
        },
        "correct_tests": ["observation"],
        "optional_tests": [],
        "unnecessary_tests": ["xray", "ct", "blood", "ecg"],
        "test_results": {
            "ecg": "No aplica",
            "blood": "No necesario",
            "xray": "No indicado",
            "ct": "Excesivo",
            "observation": "Control clínico suficiente, cuadro viral",
            "hospitalization": "No"
        },
        "diagnoses": [
            {"text": "Infección viral", "correct": True},
            {"text": "Neumonía", "correct": False},
            {"text": "Asma", "correct": False},
            {"text": "Sepsis", "correct": False}
        ],
        "treatments": [
            {"text": "Reposo, hidratación y control", "correct": True},
            {"text": "Antibióticos", "correct": False},
            {"text": "Hospitalización", "correct": False},
            {"text": "Sedantes", "correct": False}
        ],
        "outcomes": {
            "correct": "Se recupera bien en pocos días.",
            "partial": "Recuperación lenta pero sin complicaciones.",
            "incorrect": "Efectos innecesarios de tratamiento excesivo."
        },
        "explanation": "No todo es antibióticos. Muchos cuadros son virales y solo requieren manejo sintomático."
    },
    {
        "id": 2,
        "title": "Caso 2: Crisis Asmática Leve",
        "difficulty": DIFFICULTY_EASY,
        "patient_data": {
            "name": "L.R.",
            "age": 16,
            "sex": "Masculino",
            "occupation": "Estudiante",
            "chief_complaint": "Dificultad respiratoria progresiva desde hace 2 horas"
        },
        "history": {
            "personal": "Asma desde niño",
            "family": "Madre con asma",
            "habits": "No fumador, alérgico a polen",
            "medication": "Salbutamol inhalador (uso ocasional)"
        },
        "symptoms": {
            "onset": "Progresivo después de exposición a polvo",
            "duration": "2 horas",
            "intensity": "Moderado",
            "worsening": "Con el esfuerzo",
            "improving": "Parcialmente con salbutamol"
        },
        "physical_exam": {
            "vital_signs": "TA: 120/80, FC: 110 lpm, FR: 30 rpm, Temp: 36.8°C, SatO2: 94%",
            "findings": "Sibilancias bilaterales leves"
        },
        "correct_tests": ["observation"],
        "optional_tests": ["xray"],
        "unnecessary_tests": ["ct", "ecg"],
        "test_results": {
            "ecg": "Normal",
            "blood": "No necesario inicialmente",
            "xray": "No hay infiltrados, hiperinsuflación leve",
            "ct": "No indicada",
            "observation": "Mejora parcial con broncodilatadores",
            "hospitalization": "No necesaria"
        },
        "diagnoses": [
            {"text": "Crisis asmática moderada", "correct": True},
            {"text": "Neumonía bacteriana", "correct": False},
            {"text": "Ansiedad aguda", "correct": False},
            {"text": "Edema pulmonar", "correct": False}
        ],
        "treatments": [
            {"text": "Broncodilatador + Corticoide inhalado + Oxígeno", "correct": True},
            {"text": "Solo reposo", "correct": False},
            {"text": "Antibiótico", "correct": False},
            {"text": "Cirugía", "correct": False}
        ],
        "outcomes": {
            "correct": "El paciente mejora y se estabiliza.",
            "partial": "Mejora lentamente pero sigue en riesgo.",
            "incorrect": "El paciente se descompensa y requiere UCI."
        },
        "explanation": "La crisis asmática requiere manejo respiratorio inmediato. No necesitas TAC ni ECG si es clínicamente evidente."
    },
    
    # ========== INTERMEDIOS (3 puntos) ==========
    {
        "id": 3,
        "title": "Caso 3: Dolor Abdominal Agudo",
        "difficulty": DIFFICULTY_MEDIUM,
        "patient_data": {
            "name": "L.S.",
            "age": 32,
            "sex": "Femenino",
            "occupation": "Enfermera",
            "chief_complaint": "Dolor abdominal intenso en cuadrante inferior derecho desde hace 6 horas"
        },
        "history": {
            "personal": "Saludable",
            "family": "Sin antecedentes relevantes",
            "habits": "No fumadora, ejercicio regular",
            "medication": "Anticonceptivos orales"
        },
        "symptoms": {
            "onset": "Dolor periumbilical que migró a FID",
            "duration": "6 horas",
            "intensity": "Severo (9/10)",
            "worsening": "Con el movimiento, tos",
            "improving": "Flexionando las piernas"
        },
        "physical_exam": {
            "vital_signs": "TA: 120/80, FC: 100 lpm, FR: 20 rpm, Temp: 38.2°C, SatO2: 98%",
            "findings": "Dolor a la palpación en FID, signo de McBurney positivo, defensa muscular, signo de Blumberg positivo"
        },
        "correct_tests": ["blood", "observation"],
        "optional_tests": ["xray"],
        "unnecessary_tests": ["ecg", "ct"],
        "test_results": {
            "ecg": "Ritmo sinusal normal",
            "blood": "Leucocitos: 14,500 (elevados), Neutrófilos: 85%, PCR: 45 mg/L (elevada)",
            "xray": "Abdomen sin signos de obstrucción, posible fecalito apendicular",
            "ct": "No necesaria inicialmente, pero útil si diagnóstico dudoso",
            "observation": "Dolor persistente, fiebre en aumento",
            "hospitalization": "Indicada para cirugía"
        },
        "diagnoses": [
            {"text": "Apendicitis aguda", "correct": True},
            {"text": "Gastroenteritis", "correct": False, "similar": False},
            {"text": "Quiste de ovario roto", "correct": False, "similar": True},
            {"text": "Cólico renal", "correct": False, "similar": False}
        ],
        "treatments": [
            {"text": "Hospitalización inmediata para apendicectomía", "correct": True},
            {"text": "Antibióticos orales y observación ambulatoria", "correct": False, "dangerous": True},
            {"text": "Analgésicos y alta", "correct": False, "dangerous": True},
            {"text": "Laxantes", "correct": False, "dangerous": True}
        ],
        "outcomes": {
            "correct": "Apendicectomía exitosa. Paciente se recupera sin complicaciones. Alta en 2 días.",
            "partial": "Retraso en el diagnóstico. Apendicitis complicada. Mayor tiempo de recuperación.",
            "incorrect": "Apendicitis perforada. Peritonitis. Requiere cirugía de urgencia y mayor morbilidad."
        },
        "explanation": "La apendicitis aguda requiere diagnóstico rápido y cirugía. Los signos clásicos (McBurney, Blumberg) junto con leucocitosis y fiebre son diagnósticos. El retraso puede llevar a perforación y peritonitis."
    },
    {
        "id": 4,
        "title": "Caso 4: Dificultad Respiratoria",
        "difficulty": DIFFICULTY_MEDIUM,
        "patient_data": {
            "name": "M.R.",
            "age": 28,
            "sex": "Femenino",
            "occupation": "Estudiante",
            "chief_complaint": "Dificultad para respirar y sibilancias desde hace 3 horas"
        },
        "history": {
            "personal": "Asma bronquial desde la infancia",
            "family": "Madre con asma",
            "habits": "No fumadora, alérgica a polen y ácaros",
            "medication": "Salbutamol inhalador (uso ocasional)"
        },
        "symptoms": {
            "onset": "Progresivo después de exposición a polvo",
            "duration": "3 horas",
            "intensity": "Moderado a severo",
            "worsening": "Con el esfuerzo, al hablar",
            "improving": "Parcialmente con salbutamol"
        },
        "physical_exam": {
            "vital_signs": "TA: 110/70, FC: 110 lpm, FR: 28 rpm, Temp: 36.8°C, SatO2: 92%",
            "findings": "Sibilancias bilaterales, uso de músculos accesorios, tiraje intercostal"
        },
        "correct_tests": ["blood", "observation"],
        "optional_tests": ["xray"],
        "unnecessary_tests": ["ecg", "ct"],
        "test_results": {
            "ecg": "Taquicardia sinusal, sin otras alteraciones",
            "blood": "Leucocitos: 8500, Eosinófilos: 8% (ligeramente elevado), Gasometría: pH 7.38, pCO2 42, pO2 68",
            "xray": "Hiperinsuflación pulmonar, sin infiltrados",
            "ct": "No indicada en este caso",
            "observation": "Mejora parcial con broncodilatadores",
            "hospitalization": "No aplica"
        },
        "diagnoses": [
            {"text": "Crisis asmática aguda moderada-severa", "correct": True},
            {"text": "Neumonía", "correct": False, "similar": False},
            {"text": "EPOC", "correct": False, "similar": False},
            {"text": "Ansiedad/ataque de pánico", "correct": False, "dangerous": True}
        ],
        "treatments": [
            {"text": "Oxígeno, Salbutamol nebulizado, Corticosteroides sistémicos", "correct": True},
            {"text": "Solo salbutamol inhalador", "correct": False, "dangerous": True},
            {"text": "Antibióticos y reposo", "correct": False, "dangerous": False},
            {"text": "Sedantes", "correct": False, "dangerous": True}
        ],
        "outcomes": {
            "correct": "Paciente responde bien al tratamiento. Mejora significativa en 2 horas. Alta con seguimiento.",
            "partial": "Paciente mejora lentamente. Requiere más tiempo de observación.",
            "incorrect": "Paciente empeora. Crisis asmática severa. Requiere intubación y UCI."
        },
        "explanation": "La crisis asmática requiere broncodilatadores de acción rápida y corticosteroides para reducir la inflamación. La saturación de O2 baja (92%) y el uso de músculos accesorios indican gravedad. No usar sedantes (deprimen la respiración)."
    },
    {
        "id": 5,
        "title": "Caso 5: Neumonía",
        "difficulty": DIFFICULTY_MEDIUM,
        "patient_data": {
            "name": "A.T.",
            "age": 45,
            "sex": "Femenino",
            "occupation": "Maestra",
            "chief_complaint": "Fiebre, tos productiva y dificultad para respirar desde hace 3 días"
        },
        "history": {
            "personal": "Sin antecedentes relevantes",
            "family": "Sin antecedentes importantes",
            "habits": "No fumadora",
            "medication": "Ninguna"
        },
        "symptoms": {
            "onset": "Progresivo",
            "duration": "3 días",
            "intensity": "Moderado",
            "worsening": "Con esfuerzo",
            "improving": "No mejora"
        },
        "physical_exam": {
            "vital_signs": "TA: 120/80, FC: 105 lpm, FR: 26 rpm, Temp: 38.8°C, SatO2: 90%",
            "findings": "Crepitantes pulmonares, matidez a la percusión"
        },
        "correct_tests": ["xray", "blood"],
        "optional_tests": ["observation"],
        "unnecessary_tests": ["ct", "ecg"],
        "test_results": {
            "ecg": "Normal",
            "blood": "Leucocitos elevados (15,000), PCR elevada (80 mg/L)",
            "xray": "Infiltrados pulmonares en lóbulo inferior derecho",
            "ct": "Excesivo para este caso",
            "observation": "Requiere antibióticos",
            "hospitalization": "Dependiendo gravedad"
        },
        "diagnoses": [
            {"text": "Neumonía adquirida en comunidad", "correct": True},
            {"text": "Covid", "correct": False},
            {"text": "Asma", "correct": False},
            {"text": "Bronquitis leve", "correct": False}
        ],
        "treatments": [
            {"text": "Antibióticos + oxígeno", "correct": True},
            {"text": "Solo reposo", "correct": False, "dangerous": True},
            {"text": "Sedantes", "correct": False},
            {"text": "Simple analgesia", "correct": False}
        ],
        "outcomes": {
            "correct": "Paciente mejora progresivamente.",
            "partial": "Mejora lenta.",
            "incorrect": "Insuficiencia respiratoria."
        },
        "explanation": "La neumonía requiere antibióticos y soporte respiratorio."
    },
    {
        "id": 6,
        "title": "Caso 6: Emergencia Hipertensiva",
        "difficulty": DIFFICULTY_MEDIUM,
        "patient_data": {
            "name": "M.T.",
            "age": 55,
            "sex": "Femenino",
            "occupation": "Ama de casa",
            "chief_complaint": "Cefalea intensa, mareos, visión borrosa"
        },
        "history": {
            "personal": "Hipertensión desde hace 6 años",
            "family": "Padre hipertenso",
            "habits": "Dejó medicación hace 3 meses",
            "medication": "Ninguna actualmente"
        },
        "symptoms": {
            "onset": "Progresivo",
            "duration": "4 horas",
            "intensity": "Severo",
            "worsening": "Constante",
            "improving": "Nada"
        },
        "physical_exam": {
            "vital_signs": "TA: 190/120, FC: 95 lpm, FR: 20 rpm, Temp: 36.5°C, SatO2: 98%",
            "findings": "Conciencia normal, sin déficit neurológico focal"
        },
        "correct_tests": ["blood"],
        "optional_tests": ["ecg"],
        "unnecessary_tests": ["ct", "xray"],
        "test_results": {
            "ecg": "Signos leves de sobrecarga ventricular",
            "blood": "Función renal elevada, sugiere daño en órganos",
            "xray": "Normal",
            "ct": "No necesaria si no hay déficit neurológico",
            "observation": "No suficiente",
            "hospitalization": "Recomendado"
        },
        "diagnoses": [
            {"text": "Emergencia hipertensiva", "correct": True},
            {"text": "Migraña común", "correct": False},
            {"text": "Ataque de pánico", "correct": False},
            {"text": "Hipoglucemia", "correct": False}
        ],
        "treatments": [
            {"text": "Medicamento antihipertensivo intravenoso + control hospitalario", "correct": True},
            {"text": "Solo analgésicos", "correct": False},
            {"text": "Reposo en casa", "correct": False},
            {"text": "Agua y esperar", "correct": False}
        ],
        "outcomes": {
            "correct": "La presión baja progresivamente y el paciente se estabiliza.",
            "partial": "Baja pero sigue en riesgo.",
            "incorrect": "Puede presentar derrame cerebral o fallo renal."
        },
        "explanation": "Una presión tan alta sin control es peligrosa y requiere manejo hospitalario inmediato."
    },
    
    # ========== DIFÍCILES (5 puntos) ==========
    {
        "id": 7,
        "title": "Caso 7: Dolor Torácico",
        "difficulty": DIFFICULTY_HARD,
        "patient_data": {
            "name": "J.M.",
            "age": 55,
            "sex": "Masculino",
            "occupation": "Obrero",
            "chief_complaint": "Dolor en el pecho de inicio súbito hace 2 horas"
        },
        "history": {
            "personal": "Hipertensión arterial, diabetes tipo 2",
            "family": "Padre con infarto a los 60 años",
            "habits": "Fumador de 20 cigarrillos/día, sedentario",
            "medication": "Metformina, Losartán"
        },
        "symptoms": {
            "onset": "Súbito, mientras descansaba",
            "duration": "2 horas",
            "intensity": "Severo (8/10)",
            "worsening": "Con el movimiento",
            "improving": "Ligeramente con reposo"
        },
        "physical_exam": {
            "vital_signs": "TA: 160/95, FC: 95 lpm, FR: 18 rpm, Temp: 36.5°C, SatO2: 96%",
            "findings": "Diaforesis, palidez, dolor a la palpación del tórax"
        },
        "correct_tests": ["ecg", "blood"],
        "optional_tests": ["xray"],
        "unnecessary_tests": ["ct"],
        "test_results": {
            "ecg": "Elevación del segmento ST en derivaciones II, III, aVF. Ritmo sinusal.",
            "blood": "Troponina: 2.5 ng/mL (elevada), CK-MB: 45 U/L (elevada), Glucosa: 180 mg/dL",
            "xray": "Tórax sin alteraciones agudas",
            "ct": "No indicada en este caso",
            "observation": "No aplica",
            "hospitalization": "No aplica"
        },
        "diagnoses": [
            {"text": "Infarto agudo de miocardio (IAM) con elevación del ST", "correct": True},
            {"text": "Angina inestable", "correct": False, "similar": True},
            {"text": "Pericarditis aguda", "correct": False, "similar": False},
            {"text": "Dolor musculoesquelético", "correct": False, "dangerous": False}
        ],
        "treatments": [
            {"text": "Aspirina, Clopidogrel, Atorvastatina, Reperfusión (trombolisis o angioplastia)", "correct": True},
            {"text": "Solo analgésicos y observación", "correct": False, "dangerous": True},
            {"text": "Antibióticos y reposo", "correct": False, "dangerous": False},
            {"text": "Derivar a otro especialista sin tratamiento", "correct": False, "dangerous": True}
        ],
        "outcomes": {
            "correct": "Paciente estabilizado. Reperfusión exitosa. Pronóstico favorable con seguimiento.",
            "partial": "Paciente estabilizado pero tratamiento subóptimo. Mayor riesgo de complicaciones.",
            "incorrect": "Paciente empeora. Retraso en el tratamiento crítico. Complicaciones severas."
        },
        "explanation": "El IAM con elevación del ST requiere reperfusión inmediata. La elevación del ST en derivaciones inferiores (II, III, aVF) indica oclusión de la arteria coronaria derecha o circunfleja. El tiempo es crítico: 'tiempo es músculo'."
    },
    {
        "id": 8,
        "title": "Caso 8: Accidente Cerebrovascular",
        "difficulty": DIFFICULTY_HARD,
        "patient_data": {
            "name": "R.G.",
            "age": 67,
            "sex": "Masculino",
            "occupation": "Jubilado",
            "chief_complaint": "Debilidad en lado derecho del cuerpo y dificultad para hablar desde hace 1 hora"
        },
        "history": {
            "personal": "Hipertensión, dislipidemia",
            "family": "Madre con ACV",
            "habits": "Ex-fumador",
            "medication": "Amlodipina, Simvastatina"
        },
        "symptoms": {
            "onset": "Súbito",
            "duration": "1 hora",
            "intensity": "Grave",
            "worsening": "Progresión gradual",
            "improving": "No mejora"
        },
        "physical_exam": {
            "vital_signs": "TA: 170/100, FC: 88 lpm, FR: 20 rpm, Temp: 36.7°C, SatO2: 97%",
            "findings": "Hemiparesia derecha, desviación bucal, lenguaje dificultoso"
        },
        "correct_tests": ["ct", "blood"],
        "optional_tests": ["ecg"],
        "unnecessary_tests": ["xray"],
        "test_results": {
            "ecg": "Ritmo sinusal, sin alteraciones",
            "blood": "Glucosa normal, sin alteraciones graves",
            "xray": "Sin relevancia clínica",
            "ct": "No muestra sangrado → sospecha de ACV isquémico",
            "observation": "Déficit neurológico persiste",
            "hospitalization": "Recomendado"
        },
        "diagnoses": [
            {"text": "Accidente cerebrovascular isquémico", "correct": True},
            {"text": "Hipoglucemia", "correct": False},
            {"text": "Crisis epiléptica", "correct": False},
            {"text": "Migraña complicada", "correct": False}
        ],
        "treatments": [
            {"text": "Trombolisis en ventana terapéutica + hospitalización", "correct": True},
            {"text": "Solo observación", "correct": False, "dangerous": True},
            {"text": "Antibióticos", "correct": False},
            {"text": "Alta a domicilio", "correct": False, "dangerous": True}
        ],
        "outcomes": {
            "correct": "El paciente mejora y recupera parte de la movilidad.",
            "partial": "Mejora leve, déficit persiste.",
            "incorrect": "Empeora. Secuelas permanentes."
        },
        "explanation": "El ACV isquémico requiere manejo urgente. La tomografía descarta sangrado para permitir trombolisis."
    },
    {
        "id": 9,
        "title": "Caso 9: Cetoacidosis Diabética",
        "difficulty": DIFFICULTY_HARD,
        "patient_data": {
            "name": "K.L.",
            "age": 24,
            "sex": "Masculino",
            "occupation": "Estudiante",
            "chief_complaint": "Náuseas, vómitos, sed excesiva y respiración profunda"
        },
        "history": {
            "personal": "Diabetes tipo 1",
            "family": "Padre diabético",
            "habits": "Mala adherencia a insulina",
            "medication": "Insulina irregular"
        },
        "symptoms": {
            "onset": "2 días",
            "duration": "Progresivo",
            "intensity": "Grave",
            "worsening": "No tratado",
            "improving": "Nada"
        },
        "physical_exam": {
            "vital_signs": "TA: 100/65, FC: 120 lpm, FR: 30 rpm, Temp: 37°C, SatO2: 97%",
            "findings": "Aliento cetónico, respiración Kussmaul, deshidratación"
        },
        "correct_tests": ["blood", "hospitalization"],
        "optional_tests": ["observation"],
        "unnecessary_tests": ["xray", "ecg", "ct"],
        "test_results": {
            "ecg": "Normal",
            "blood": "Glucosa 450 mg/dL, cetonas elevadas, acidosis metabólica",
            "xray": "Normal",
            "ct": "Sin utilidad",
            "observation": "No suficiente",
            "hospitalization": "Requerida"
        },
        "diagnoses": [
            {"text": "Cetoacidosis diabética", "correct": True},
            {"text": "Gastroenteritis", "correct": False},
            {"text": "Ansiedad", "correct": False},
            {"text": "Asma", "correct": False}
        ],
        "treatments": [
            {"text": "Insulina IV + líquidos + electrolitos", "correct": True},
            {"text": "Solo suero oral", "correct": False, "dangerous": True},
            {"text": "Analgésicos", "correct": False},
            {"text": "Alta", "correct": False, "dangerous": True}
        ],
        "outcomes": {
            "correct": "Paciente se estabiliza.",
            "partial": "Mejora lenta.",
            "incorrect": "Shock y muerte."
        },
        "explanation": "La CAD es emergencia metabólica. Requiere manejo hospitalario inmediato."
    },
    {
        "id": 10,
        "title": "Caso 10: Hemorragia Digestiva",
        "difficulty": DIFFICULTY_HARD,
        "patient_data": {
            "name": "P.G.",
            "age": 52,
            "sex": "Masculino",
            "occupation": "Administrador",
            "chief_complaint": "Vómito con sangre y debilidad intensa"
        },
        "history": {
            "personal": "Úlcera péptica",
            "family": "Sin relevancia",
            "habits": "Alcohol ocasional",
            "medication": "AINES frecuentes"
        },
        "symptoms": {
            "onset": "Súbito",
            "duration": "4 horas",
            "intensity": "Severo",
            "worsening": "Continuo",
            "improving": "Nada"
        },
        "physical_exam": {
            "vital_signs": "TA: 85/50, FC: 130 lpm, FR: 20 rpm, Temp: 36.5°C, SatO2: 95%",
            "findings": "Palidez, sudoración, debilidad extrema"
        },
        "correct_tests": ["blood", "hospitalization"],
        "optional_tests": [],
        "unnecessary_tests": ["ecg", "ct", "xray", "observation"],
        "test_results": {
            "blood": "Hb 7 g/dl (anemia severa)",
            "xray": "No relevante",
            "ecg": "Taquicardia",
            "ct": "Inútil",
            "observation": "No suficiente",
            "hospitalization": "Necesaria urgente"
        },
        "diagnoses": [
            {"text": "Hemorragia digestiva alta", "correct": True},
            {"text": "Gastritis leve", "correct": False},
            {"text": "Anemia crónica", "correct": False},
            {"text": "Ansiedad", "correct": False}
        ],
        "treatments": [
            {"text": "Reposición de volumen + endoscopia urgente", "correct": True},
            {"text": "Solo analgésicos", "correct": False},
            {"text": "Alta inmediata", "correct": False, "dangerous": True},
            {"text": "Sedantes", "correct": False}
        ],
        "outcomes": {
            "correct": "Estabilidad y control del sangrado.",
            "partial": "Requiere transfusión.",
            "incorrect": "Shock hemorrágico y muerte."
        },
        "explanation": "Sangrado digestivo es emergencia. Primero estabilizar, luego endoscopia."
    },
    {
        "id": 11,
        "title": "Caso 11: Trauma Craneoencefálico",
        "difficulty": DIFFICULTY_HARD,
        "patient_data": {
            "name": "D.P.",
            "age": 19,
            "sex": "Masculino",
            "occupation": "Estudiante",
            "chief_complaint": "Golpe en la cabeza tras accidente en moto"
        },
        "history": {
            "personal": "Sano",
            "family": "Sin relevancia",
            "habits": "Conductor imprudente",
            "medication": "Ninguna"
        },
        "symptoms": {
            "onset": "Inmediato",
            "duration": "30 minutos",
            "intensity": "Grave",
            "worsening": "Pérdida de conciencia breve",
            "improving": "No mejora"
        },
        "physical_exam": {
            "vital_signs": "TA: 130/85, FC: 95 lpm, FR: 22 rpm, Temp: 36.5°C, SatO2: 98%",
            "findings": "Confusión, vómito, dolor intenso"
        },
        "correct_tests": ["ct", "hospitalization"],
        "optional_tests": ["observation"],
        "unnecessary_tests": ["ecg", "blood"],
        "test_results": {
            "ecg": "Normal",
            "blood": "Normal",
            "xray": "No aplica",
            "ct": "Contusión cerebral",
            "observation": "Inestable",
            "hospitalization": "Urgente"
        },
        "diagnoses": [
            {"text": "Trauma craneoencefálico moderado", "correct": True},
            {"text": "Migraña", "correct": False},
            {"text": "Deshidratación", "correct": False},
            {"text": "Estrés", "correct": False}
        ],
        "treatments": [
            {"text": "Hospitalización + neurocirugía si requiere", "correct": True},
            {"text": "Solo reposo", "correct": False, "dangerous": True},
            {"text": "Analgésicos", "correct": False},
            {"text": "Alta inmediata", "correct": False, "dangerous": True}
        ],
        "outcomes": {
            "correct": "Paciente estable.",
            "partial": "Secuelas leves.",
            "incorrect": "Daño permanente."
        },
        "explanation": "El trauma craneal requiere TAC urgente y vigilancia hospitalaria."
    },
    {
        "id": 12,
        "title": "Caso 12: Embarazo Ectópico",
        "difficulty": DIFFICULTY_HARD,
        "patient_data": {
            "name": "S.M.",
            "age": 29,
            "sex": "Femenino",
            "occupation": "Administradora",
            "chief_complaint": "Dolor abdominal + retraso menstrual + sangrado"
        },
        "history": {
            "personal": "Un embarazo previo",
            "family": "Normal",
            "habits": "Saludable",
            "medication": "Ninguna"
        },
        "symptoms": {
            "onset": "48 horas",
            "duration": "Progresivo",
            "intensity": "Severo",
            "worsening": "Movimiento",
            "improving": "Nada"
        },
        "physical_exam": {
            "vital_signs": "TA: 95/60, FC: 120 lpm, FR: 20 rpm, Temp: 36.5°C, SatO2: 98%",
            "findings": "Dolor intenso y signos de shock"
        },
        "correct_tests": ["blood", "ct", "hospitalization"],
        "optional_tests": [],
        "unnecessary_tests": ["ecg", "xray"],
        "test_results": {
            "ecg": "Normal",
            "blood": "Beta hCG elevada",
            "xray": "No aplica",
            "ct": "Masa anexial compatible con ectópico",
            "observation": "No suficiente",
            "hospitalization": "Urgente"
        },
        "diagnoses": [
            {"text": "Embarazo ectópico", "correct": True},
            {"text": "Apendicitis", "correct": False},
            {"text": "Colitis", "correct": False},
            {"text": "Gastroenteritis", "correct": False}
        ],
        "treatments": [
            {"text": "Cirugía de emergencia", "correct": True},
            {"text": "Medicamentos simples", "correct": False, "dangerous": True},
            {"text": "Reposo", "correct": False},
            {"text": "Alta", "correct": False, "dangerous": True}
        ],
        "outcomes": {
            "correct": "Paciente salva la vida.",
            "partial": "Complicaciones.",
            "incorrect": "Shock hemorrágico y muerte."
        },
        "explanation": "El ectópico es letal si no se trata de inmediato."
    },
    {
        "id": 13,
        "title": "Caso 13: Preeclampsia",
        "difficulty": DIFFICULTY_HARD,
        "patient_data": {
            "name": "S.N.",
            "age": 30,
            "sex": "Femenino",
            "occupation": "Docente",
            "chief_complaint": "Dolor de cabeza, visión borrosa y hinchazón"
        },
        "history": {
            "personal": "Primer embarazo",
            "family": "Madre con preeclampsia",
            "habits": "Saludable",
            "medication": "Prenatales"
        },
        "symptoms": {
            "onset": "48h",
            "duration": "2 días",
            "intensity": "Progresivo",
            "worsening": "Constante",
            "improving": "Nada"
        },
        "physical_exam": {
            "vital_signs": "TA: 170/110, FC: 90 lpm, FR: 18 rpm, Temp: 36.5°C, SatO2: 98%",
            "findings": "Edema generalizado"
        },
        "correct_tests": ["blood", "hospitalization"],
        "optional_tests": ["observation"],
        "unnecessary_tests": ["ct", "xray", "ecg"],
        "test_results": {
            "blood": "Proteinuria marcada",
            "hospitalization": "Requerida",
            "xray": "Inútil",
            "ct": "Riesgoso",
            "ecg": "Normal"
        },
        "diagnoses": [
            {"text": "Preeclampsia severa", "correct": True},
            {"text": "Migraña", "correct": False},
            {"text": "Estrés", "correct": False},
            {"text": "Infección urinaria", "correct": False}
        ],
        "treatments": [
            {"text": "Hospitalizar + control TA + manejo obstétrico", "correct": True},
            {"text": "Solo reposo", "correct": False},
            {"text": "Alta a casa", "correct": False, "dangerous": True},
            {"text": "Analgésicos únicamente", "correct": False}
        ],
        "outcomes": {
            "correct": "Madre y bebé estables.",
            "partial": "Complicaciones.",
            "incorrect": "Riesgo vital."
        },
        "explanation": "Preeclampsia es potencialmente mortal. Se maneja en hospital."
    }
]


# Variables globales para el sistema de gestión de casos
_used_case_ids = set()  # IDs de casos ya usados
_case_progression_stage = 0  # 0: inicial (2 fáciles), 1: intermedios (3), 2: difíciles (2), 3: infinito (intermedios/difíciles)
_easy_cases_used = 0
_medium_cases_used = 0
_hard_cases_used = 0
_last_difficulty_infinite = None  # Última dificultad usada en modo infinito

def reset_case_progression():
    """Resetea el sistema de progresión de casos."""
    global _used_case_ids, _case_progression_stage, _easy_cases_used, _medium_cases_used, _hard_cases_used, _last_difficulty_infinite
    _used_case_ids = set()
    _case_progression_stage = 0
    _easy_cases_used = 0
    _medium_cases_used = 0
    _hard_cases_used = 0
    _last_difficulty_infinite = None

def get_random_case(infinite_mode=False):
    """
    Retorna un caso clínico según la progresión:
    - Primero: 2 fáciles
    - Segundo: 3 intermedios
    - Tercero: 2 difíciles
    - Después: alterna entre intermedios y difíciles (o solo difíciles si infinite_mode=True)
    No repite casos hasta que todos de esa dificultad hayan salido.
    
    Args:
        infinite_mode: Si es True, solo devuelve casos difíciles
    """
    global _used_case_ids, _case_progression_stage, _easy_cases_used, _medium_cases_used, _hard_cases_used
    
    # Obtener casos por dificultad
    easy_cases = get_cases_by_difficulty(DIFFICULTY_EASY)
    medium_cases = get_cases_by_difficulty(DIFFICULTY_MEDIUM)
    hard_cases = get_cases_by_difficulty(DIFFICULTY_HARD)
    
    # Si está en modo infinito, solo devolver casos difíciles
    if infinite_mode:
        available_cases = [c for c in hard_cases if c["id"] not in _used_case_ids]
        if len(available_cases) == 0:
            # Si se agotaron todos los difíciles, resetear
            _used_case_ids = set()
            available_cases = hard_cases
        selected_case = random.choice(available_cases)
        _used_case_ids.add(selected_case["id"])
        case_copy = copy.deepcopy(selected_case)
        random.shuffle(case_copy["diagnoses"])
        return case_copy
    
    available_cases = []
    target_difficulty = None
    
    # Determinar qué dificultad usar según la progresión
    if _case_progression_stage == 0:
        # Fase 1: 2 casos fáciles
        available_cases = [c for c in easy_cases if c["id"] not in _used_case_ids]
        target_difficulty = DIFFICULTY_EASY
        if len(available_cases) == 0:
            # Si ya se usaron todos los fáciles, pasar a intermedios
            _case_progression_stage = 1
            _used_case_ids = set()  # Resetear para intermedios
            available_cases = [c for c in medium_cases if c["id"] not in _used_case_ids]
            target_difficulty = DIFFICULTY_MEDIUM
        elif _easy_cases_used >= 2:
            # Ya se usaron 2 fáciles, pasar a intermedios
            _case_progression_stage = 1
            _used_case_ids = set()  # Resetear para intermedios
            available_cases = [c for c in medium_cases if c["id"] not in _used_case_ids]
            target_difficulty = DIFFICULTY_MEDIUM
    
    if _case_progression_stage == 1:
        # Fase 2: 3 casos intermedios
        available_cases = [c for c in medium_cases if c["id"] not in _used_case_ids]
        target_difficulty = DIFFICULTY_MEDIUM
        if len(available_cases) == 0:
            # Si ya se usaron todos los intermedios, pasar a difíciles
            _case_progression_stage = 2
            _used_case_ids = set()  # Resetear para difíciles
            available_cases = [c for c in hard_cases if c["id"] not in _used_case_ids]
            target_difficulty = DIFFICULTY_HARD
        elif _medium_cases_used >= 3:
            # Ya se usaron 3 intermedios, pasar a difíciles
            _case_progression_stage = 2
            _used_case_ids = set()  # Resetear para difíciles
            available_cases = [c for c in hard_cases if c["id"] not in _used_case_ids]
            target_difficulty = DIFFICULTY_HARD
    
    if _case_progression_stage == 2:
        # Fase 3: 2 casos difíciles
        available_cases = [c for c in hard_cases if c["id"] not in _used_case_ids]
        target_difficulty = DIFFICULTY_HARD
        if len(available_cases) == 0:
            # Si ya se usaron todos los difíciles, pasar a modo infinito
            _case_progression_stage = 3
            _used_case_ids = set()  # Resetear para modo infinito
            available_cases = [c for c in medium_cases if c["id"] not in _used_case_ids]
            target_difficulty = DIFFICULTY_MEDIUM
        elif _hard_cases_used >= 2:
            # Ya se usaron 2 difíciles, pasar a modo infinito
            _case_progression_stage = 3
            _used_case_ids = set()  # Resetear para modo infinito
            # Alternar entre intermedios y difíciles
            if len([c for c in medium_cases if c["id"] not in _used_case_ids]) > 0:
                available_cases = [c for c in medium_cases if c["id"] not in _used_case_ids]
                target_difficulty = DIFFICULTY_MEDIUM
            else:
                available_cases = [c for c in hard_cases if c["id"] not in _used_case_ids]
                target_difficulty = DIFFICULTY_HARD
    
    if _case_progression_stage == 3:
        # Modo infinito: alternar entre intermedios y difíciles
        global _last_difficulty_infinite
        medium_available = [c for c in medium_cases if c["id"] not in _used_case_ids]
        hard_available = [c for c in hard_cases if c["id"] not in _used_case_ids]
        
        # Si una dificultad se agotó, usar la otra
        if len(medium_available) == 0 and len(hard_available) > 0:
            available_cases = hard_available
            target_difficulty = DIFFICULTY_HARD
        elif len(hard_available) == 0 and len(medium_available) > 0:
            available_cases = medium_available
            target_difficulty = DIFFICULTY_MEDIUM
        elif len(medium_available) == 0 and len(hard_available) == 0:
            # Si ambas se agotaron, resetear y empezar con intermedios
            _used_case_ids = set()
            available_cases = medium_cases
            target_difficulty = DIFFICULTY_MEDIUM
            _last_difficulty_infinite = DIFFICULTY_MEDIUM
        else:
            # Alternar: si el último fue medio, usar difícil; si fue difícil, usar medio
            if _last_difficulty_infinite == DIFFICULTY_MEDIUM:
                # Último fue medio, usar difícil
                available_cases = hard_available
                target_difficulty = DIFFICULTY_HARD
            else:
                # Último fue difícil o es el primero, usar medio
                available_cases = medium_available
                target_difficulty = DIFFICULTY_MEDIUM
    
    # Si no hay casos disponibles, usar cualquier caso (no debería pasar)
    if len(available_cases) == 0:
        available_cases = CLINICAL_CASES
    
    # Seleccionar caso aleatorio de los disponibles
    selected_case = random.choice(available_cases)
    
    # Copia para no modificar el caso original y barajar diagnósticos
    case_copy = copy.deepcopy(selected_case)
    random.shuffle(case_copy["diagnoses"])
    
    # Marcar como usado y actualizar contadores
    _used_case_ids.add(selected_case["id"])
    if selected_case["difficulty"] == DIFFICULTY_EASY:
        _easy_cases_used += 1
    elif selected_case["difficulty"] == DIFFICULTY_MEDIUM:
        _medium_cases_used += 1
    elif selected_case["difficulty"] == DIFFICULTY_HARD:
        _hard_cases_used += 1
    
    # Actualizar última dificultad en modo infinito
    if _case_progression_stage == 3:
        _last_difficulty_infinite = selected_case["difficulty"]
    
    return case_copy


def get_case_by_id(case_id):
    """Retorna un caso clínico por su ID."""
    for case in CLINICAL_CASES:
        if case.get("id") == case_id:
            return case
    return None


def get_cases_by_difficulty(difficulty):
    """Retorna todos los casos de una dificultad específica."""
    return [case for case in CLINICAL_CASES if case.get("difficulty") == difficulty]


def get_points_for_difficulty(difficulty):
    """Retorna los puntos que otorga un caso según su dificultad."""
    if difficulty == DIFFICULTY_EASY:
        return POINTS_EASY
    elif difficulty == DIFFICULTY_MEDIUM:
        return POINTS_MEDIUM
    elif difficulty == DIFFICULTY_HARD:
        return POINTS_HARD
    return 0


def calculate_test_score(selected_tests, correct_tests, optional_tests, unnecessary_tests):
    """
    Calcula la puntuación por las pruebas seleccionadas.
    
    Returns:
        (score, feedback) - Puntuación y mensaje de retroalimentación
    """
    score = 0
    feedback_parts = []
    
    # Puntos por pruebas correctas
    for test in correct_tests:
        if test in selected_tests:
            score += 20
            feedback_parts.append(f"+20: {TEST_TYPES[test]} era necesaria")
        else:
            score -= 10
            feedback_parts.append(f"-10: Faltó {TEST_TYPES[test]} (necesaria)")
    
    # Puntos por pruebas opcionales
    for test in optional_tests:
        if test in selected_tests:
            score += 10
            feedback_parts.append(f"+10: {TEST_TYPES[test]} fue útil")
    
    # Penalización por pruebas innecesarias
    for test in unnecessary_tests:
        if test in selected_tests:
            score -= 15
            feedback_parts.append(f"-15: {TEST_TYPES[test]} era innecesaria")
    
    # Penalización por pruebas no relacionadas
    for test in selected_tests:
        if test not in correct_tests and test not in optional_tests:
            if test not in unnecessary_tests:  # Si no está en ninguna categoría conocida
                score -= 5
                feedback_parts.append(f"-5: {TEST_TYPES[test]} no era relevante")
    
    feedback = " | ".join(feedback_parts) if feedback_parts else "Sin pruebas seleccionadas"
    return score, feedback


def calculate_final_score(test_score, diagnosis_correct, treatment_correct, time_taken, max_time, case_difficulty):
    """
    Calcula la puntuación final del caso clínico.
    
    Args:
        test_score: Puntuación de las pruebas
        diagnosis_correct: Si el diagnóstico fue correcto
        treatment_correct: Si el tratamiento fue correcto
        time_taken: Tiempo tomado en milisegundos
        max_time: Tiempo máximo permitido en milisegundos
        case_difficulty: Dificultad del caso ("easy", "medium", "hard")
    
    Returns:
        Puntuación total
    """
    total = test_score
    
    # Bonificación por diagnóstico correcto
    if diagnosis_correct:
        total += 50
    else:
        total -= 30
    
    # Bonificación por tratamiento correcto
    if treatment_correct:
        total += 50
    else:
        total -= 30
    
    # Bonificación por rapidez (si completó en menos del 50% del tiempo)
    if time_taken < max_time * 0.5:
        total += 20
    elif time_taken < max_time * 0.75:
        total += 10
    
    return max(0, total)  # No permitir puntuación negativa
