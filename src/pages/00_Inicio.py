import streamlit as st

# Título de la página:
st.set_page_config(
    page_title="Mi línea de vida",
    page_icon="🧭",
    layout="centered"
)

st.title("Línea de Vida Digital y Perfil Vocacional")
st.subheader("Herramienta de reflexión para el proyecto de vida")

st.markdown(
    "Bienvenido/a a la aplicación web de **Línea de Vida y Perfil "
    "Vocacional**. Esta herramienta pedagógica está diseñada para acompañar "
    "a estudiantes de enseñanza media en el reconocimiento de su trayectoria "
    "personal y escolar, facilitando la toma de decisiones vocacionales "
    "junto a sus profesores jefes y orientadores."
)

st.markdown("---")

# ---------------------------------------------------------
# Propósito y Principios de Privacidad
# ---------------------------------------------------------
col_purpose, col_privacy = st.columns(2)

with col_purpose:
    with st.container(border=True):
        st.markdown("### 🎯 Propósito")
        st.markdown(
            "- **Registrar e integrar:** Permite ordenar cronológicamente los "
            "hitos significativos de tu trayectoria escolar y personal.\n"
            "- **Valorar y reflexionar:** Asigna valoraciones subjetivas a "
            "tus experiencias para reconocer aprendizajes, intereses y "
            "metas.\n"
            "- **Construir tu perfil:** Genera insumos estructurados para "
            "orientar la conversación sobre tu futuro académico y laboral."
        )

with col_privacy:
    with st.container(border=True):
        st.markdown("### 🔒 Privacidad y Control Local")
        st.markdown(
            "- **Tú decides qué compartir:** Registra solo aquellas "
            "experiencias con las que te sientas cómodo/a.\n"
            "- **Sin diagnósticos automáticos:** La aplicación no califica "
            "ni etiqueta tus capacidades; apoya el diálogo con tu orientador.\n"
            "- **Privacidad garantizada:** Tus datos no se envían a servidores "
            "externos ni bases de datos centralizadas; se procesan en tu "
            "dispositivo."
        )

st.markdown("---")

# ---------------------------------------------------------
# Estructura del Perfil Vocacional
# ---------------------------------------------------------
st.header("📋 Estructura del Perfil Vocacional")
st.caption(
    "La aplicación organiza la información recolectada en 10 secciones "
    "fundamentales para la elaboración de tu perfil:"
)

vocational_sections = [
    (
        "1. Datos personales",
        "Antecedentes generales para contextualizar tu etapa de desarrollo "
        "y trayectoria escolar.",
    ),
    (
        "2. Contexto familiar y social",
        "Estructura familiar, condiciones del entorno y expectativas respecto "
        "a la continuidad de estudios.",
    ),
    (
        "3. Relación con compañeros y profesores",
        "Vínculos interpersonales en el contexto escolar y su impacto en tu "
        "confianza e integración.",
    ),
    (
        "4. Redes de apoyo",
        "Personas, instituciones y recursos disponibles (internos y externos) "
        "que acompañan tu trayectoria.",
    ),
    (
        "5. Estilo y ritmo de aprendizaje",
        "Estrategias pedagógicas y condiciones que favorecen tu estudio (sin "
        "categorizaciones rígidas).",
    ),
    (
        "6. Fortalezas académicas",
        "Asignaturas destacadas, conocimientos previos y actitudes positivas "
        "hacia el aprendizaje.",
    ),
    (
        "7. Áreas de mejora o dificultades",
        "Identificación de barreras pedagógicas o contextuales que requieren "
        "mayor acompañamiento.",
    ),
    (
        "8. Intereses y motivaciones",
        "Actividades que disfrutas y experiencias que despiertan curiosidad "
        "e interés futuro.",
    ),
    (
        "9. Logros y metas",
        "Reconocimiento de avances recientes y proyecciones a corto, mediano "
        "y largo plazo.",
    ),
    (
        "10. Habilidades sociales y emocionales",
        "Recursos socioemocionales, comunicación asertiva, empatía y trabajo "
        "en equipo.",
    ),
]

for section_title, section_description in vocational_sections:
    with st.expander(section_title):
        st.write(section_description)

st.markdown("---")

# ---------------------------------------------------------
# Confirmación de Inicio
# ---------------------------------------------------------
st.subheader("¿Listo/a para comenzar?")
st.write(
    "Avanza a la primera sección utilizando la barra lateral de navegación "
    "para iniciar el registro de tus antecedentes y la construcción de tu "
    "Línea de Vida."
)

start_activity = st.button(
    label="Iniciar Registro del Perfil Vocacional",
    type="primary",
    use_container_width=True,
)

if start_activity:
    st.info(
        "Utiliza el menú de la izquierda para desplegar el formulario "
        "de la **Sección 1: Datos Personales**."
    )