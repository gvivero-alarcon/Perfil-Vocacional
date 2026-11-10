import streamlit as st


st.set_page_config(
    page_title="Debilidades",
    page_icon="⚠️"
)

st.header("7. Áreas de mejora o dificultades")
st.caption(
    "Identificar las dificultades y barreras que experimenta el estudiante "
    "durante su trayectoria educativa, considerando factores personales, "
    "pedagógicos y contextuales que pueden incidir en sus oportunidades de "
    "aprendizaje."
)

with st.form(key="learning_barriers_form"):
    with st.container(border=True):
        st.subheader("Materias o Habilidades con Mayor Requerimiento de Apoyo")

        subjects_needing_support = st.multiselect(
            label="Asignaturas o ámbitos con mayores barreras:",
            options=[
                "Matemáticas y Razonamiento Lógico-Matemático",
                "Comprensión Lectora y Escritura",
                "Ciencias Naturales (Física / Química / Biología)",
                "Historia y Ciencias Sociales",
                "Idiomas (Inglés)",
                "Organización y Gestión del Tiempo",
                "Expresión Oral / Presentaciones",
                "Habilidades Motrices / Educación Física",
            ],
            help=(
                "Selecciona las áreas donde el estudiante requiere "
                "mayor acompañamiento pedagógico."
            ),
        )

        skill_barriers_description = st.text_area(
            label="Detalle de materias, habilidades o aprendizajes específicos",
            placeholder=(
                "Describe los contenidos, habilidades o tareas puntuales "
                "en las que requiere mayor fortalecimiento, acompañamiento "
                "o adaptación."
            ),
            height=120,
        )

    with st.container(border=True):
        st.subheader("Aspectos que Dificultan su Aprendizaje")

        contextual_barrier_factors = st.multiselect(
            label="Factores contextuales, pedagógicos o personales intervinientes:",
            options=[
                "Estrategias pedagógicas poco diversificadas / Rigidez evaluativa",
                "Falta de recursos o apoyos específicos en la escuela",
                "Baja tolerancia a la frustración / Ansiedad ante evaluaciones",
                "Dificultades en la atención o concentración prolongada",
                "Inasistencias continuas o interrupción de trayectoria escolar",
                "Situación familiar o emocional compleja",
                "Escaso espacio o tiempo para el estudio en el hogar",
                "Dificultad para el trabajo en equipo o interacción grupal",
            ],
            help=(
                "Considera barreras del entorno escolar, familiar o pedagógico."
            ),
        )

        learning_obstacles_description = st.text_area(
            label="Análisis de condiciones que obstaculizan su progreso",
            placeholder=(
                "Examina las condiciones personales, escolares o de entorno "
                "que dificultan su participación y aprendizaje, evitando "
                "atribuir las barreras de forma exclusiva al estudiante."
            ),
            height=140,
        )