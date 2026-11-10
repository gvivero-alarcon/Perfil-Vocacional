import streamlit as st


st.set_page_config(
    page_title="Logros",
    page_icon="🏆"
)

st.header("9. Logros y metas")
st.caption(
    "Reconocer experiencias de logro y proyecciones personales que permitan "
    "comprender cómo el estudiante valora sus avances, establece "
    "propósitos y visualiza posibilidades de desarrollo futuro."
)

with st.form(key="achievements_goals_form"):

    # ---------------------------------------------------------
    # 9.1 Logros Recientes
    # ---------------------------------------------------------
    with st.container(border=True):
        st.subheader("Logros Recientes")

        recent_achievement_types = st.multiselect(
            label="Ámbitos de logros significativos identificados:",
            options=[
                "Académico (mejora de notas, superar una materia difícil)",
                "Personal (desarrollo de hábitos, mayor autonomía)",
                "Social (mejora en relaciones con pares, resolución de conflictos)",
                "Extracurricular (deporte, arte, talleres, competencias)",
                "Familiar (colaboración y superación de dificultades)",
            ],
            help=(
                "Selecciona las áreas donde el estudiante reconoce o "
                "ha manifestado avances relevantes."
            ),
        )

        recent_achievements_description = st.text_area(
            label="Descripción de experiencias y avances significativos",
            placeholder=(
                "Describe las experiencias concretas que el estudiante considera "
                "significativas en el ámbito académico, personal o social, "
                "y cómo valora su propio progreso."
            ),
            height=120,
        )

    # ---------------------------------------------------------
    # 9.2 Metas a Corto Plazo
    # ---------------------------------------------------------
    with st.container(border=True):
        st.subheader("Metas a Corto Plazo")

        short_term_goals_description = st.text_area(
            label="Propósitos a alcanzar en un período próximo",
            placeholder=(
                "Identifica los objetivos inmediatos (próximos meses o semestre) "
                "y las acciones concretas que el estudiante considera necesarias "
                "para alcanzarlos."
            ),
            height=120,
        )

    # ---------------------------------------------------------
    # 9.3 Metas a Mediano Plazo
    # ---------------------------------------------------------
    with st.container(border=True):
        st.subheader("Metas a Mediano Plazo")

        medium_term_goals_description = st.text_area(
            label="Aspiraciones vinculadas a su proyecto de vida y trayectoria",
            placeholder=(
                "Describe las aspiraciones proyectadas para los próximos años "
                "(finalización de etapas escolares, continuidad formativa o "
                "primeras decisiones de exploración vocacional e intereses "
                "ocupacionales)."
            ),
            height=120,
        )

    # ---------------------------------------------------------
    # 9.4 Metas a Largo Plazo / Sintesis de Acompañamiento
    # ---------------------------------------------------------
    with st.container(border=True):
        st.subheader("Metas a Largo Plazo y Apreciación General")

        long_term_goals_description = st.text_area(
            label="Proyección a largo plazo y necesidades de acompañamiento",
            placeholder=(
                "Registra las apreciaciones fundamentadas basadas en la información "
                "recopilada, identificando aspectos relevantes del proyecto de vida, "
                "necesidades de acompañamiento pedagógico/orientación y elementos "
                "que requieren mayor profundización."
            ),
            height=140,
        )