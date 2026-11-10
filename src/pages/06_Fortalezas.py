import streamlit as st

st.set_page_config(
    page_title="Fortalezas",
    page_icon="⭐",
)

st.header("6. Fortalezas académicas")
st.caption(
    "Identificar las capacidades, desempeños y disposiciones favorables que "
    "el estudiante manifiesta en su trayectoria escolar, reconociendo su "
    "potencial contribución al desarrollo de intereses y expectativas "
    "vocacionales."
)

with st.form(key="academic_strengths_form"):
    with st.container(border=True):
        st.subheader("Habilidades, Áreas de Interés y/o Materias Destacadas")

        outstanding_subjects = st.multiselect(
            label="Asignaturas o áreas de mayor interés y desempeño:",
            options=[
                "Matemáticas y Pensamiento Lógico",
                "Lenguaje y Comunicación / Literatura",
                "Ciencias Naturales / Biología / Física / Química",
                "Historia, Geografía y Ciencias Sociales",
                "Artes Visuales / Música / Expresión Artística",
                "Educación Física y Deportes",
                "Tecnología / Programación / Computación",
                "Idiomas / Inglés",
                "Talleres técnicos o vocacionales específicos",
            ],
            default=st.session_state.data.get("outstanding_subjects", []),
            help="Selecciona las áreas donde el estudiante destaca o muestra mayor facilidad.",
        )

        academic_skills_description = st.text_area(
            label="Detalle de habilidades y desempeños destacados",
            placeholder=(
                "Describe las habilidades específicas, conocimientos previos "
                "o logros sobresalientes en los que demuestra mayor facilidad, "
                "participación activa o potencial vocacional."
            ),
            value=st.session_state.data.get("academic_skills_description", ""),
            height=120,
        )

    with st.container(border=True):
        st.subheader("Actitudes Positivas hacia el Estudio")

        positive_attitudes = st.multiselect(
            label="Disposiciones favorables que favorecen su aprendizaje:",
            options=[
                "Perseverancia ante la dificultad",
                "Responsabilidad y cumplimiento de deberes",
                "Curiosidad intelectual e investigación autónoma",
                "Autonomía en la ejecución de tareas",
                "Compromiso y participación activa en clases",
                "Capacidad crítica y reflexiva",
                "Disposición para el trabajo colaborativo",
            ],
            default=st.session_state.data.get("positive_attitudes", []),
        )

        attitudes_description = st.text_area(
            label="Descripción del impacto de estas actitudes",
            placeholder=(
                "Describe cómo estas disposiciones o fortalezas actúan como "
                "motores para su aprendizaje y de qué manera apoyan su "
                "proceso de exploración y futuras decisiones vocacionales."
            ),
            value=st.session_state.data.get("attitudes_description", ""),
            height=130,
        )

    save_fortalezas = st.form_submit_button(label="Guardar", width="content")

if save_fortalezas:
    st.session_state.data["outstanding_subjects"] = outstanding_subjects
    st.session_state.data["academic_skills_description"] = academic_skills_description
    st.session_state.data["positive_attitudes"] = positive_attitudes
    st.session_state.data["attitudes_description"] = attitudes_description
    # st.toast("Fortalezas académicas guardadas correctamente.")
    st.switch_page("pages/07_Debilidades.py")