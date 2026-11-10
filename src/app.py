import streamlit as st
from datetime import date


# 1. Inicialización del estado global:
if "data" not in st.session_state:
    st.session_state.data = {
        "full_name": "",
        "age": 12,
        "date_of_birth": date(2014, 1, 1),
        "school_grade": "7° Básico"
    }

if "milestones" not in st.session_state:
    st.session_state.milestones = []

# 2. Definición de las páginas indicando archivo, título con número e ícono
home_page = st.Page(
    page="pages/00_Inicio.py",
    title="Inicio",
    icon="🏠",
    default=True,
)

section_01_page = st.Page(
    page="pages/01_Datos personales.py",
    title="1. Datos Personales",
    icon="👤",
)

section_02_page = st.Page(
    page="pages/02_Familia.py",
    title="2. Contexto Familiar y Social",
    icon="👨‍👩‍👧‍👦",
)

section_03_page = st.Page(
    page="pages/03_Colegio.py",
    title="3. Relación con Compañeros y Profesores",
    icon="🏫",
)

section_04_page = st.Page(
    page="pages/04_Apoyo.py",
    title="4. Redes de Apoyo",
    icon="🤝",
)

section_05_page = st.Page(
    page="pages/05_Aprendizaje.py",
    title="5. Estilo y Ritmo de Aprendizaje",
    icon="🧠",
)

section_06_page = st.Page(
    page="pages/06_Fortalezas.py",
    title="6. Fortalezas Académicas",
    icon="⭐",
)

section_07_page = st.Page(
    page="pages/07_Debilidades.py",
    title="7. Áreas de Mejora o Dificultades",
    icon="⚠️",
)

section_08_page = st.Page(
    page="pages/08_Intereses.py",
    title="8. Intereses y Motivaciones",
    icon="🎯",
)

section_09_page = st.Page(
    page="pages/09_Logros.py",
    title="9. Logros y Metas",
    icon="🏆",
)

section_10_page = st.Page(
    page="pages/10_Acontecimientos.py",
    title="1. Acontecimientos",
    icon="🚩",
)

section_11_page = st.Page(
    page="pages/11_Línea de vida.py",
    title="2. Línea de vida",
    icon="📈",
)

section_12_page = st.Page(
    page="pages/12_Resultados.py",
    title="Perfil",
    icon="📋",
)

# 2. Configuración del menú de navegación agrupado o lineal
pg = st.navigation(
    {
        "General": [home_page],
        "Perfil vocacional": [
            section_01_page,
            section_02_page,
            section_03_page,
            section_04_page,
            section_05_page,
            section_06_page,
            section_07_page,
            section_08_page,
            section_09_page
        ],
        "Línea de vida": [
            section_10_page,
            section_11_page
        ],
        "Resultados": [section_12_page]
    }
)

# 3. Renderizar la página seleccionada
pg.run()