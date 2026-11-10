import streamlit as st


st.set_page_config(
    page_title="Familia",
    page_icon="👨‍👩‍👧‍👦"
)

st.header("2. Contexto familiar y social")
st.caption(
    "Caracterizar las condiciones familiares y sociales que forman parte del "
    "entorno de desarrollo del estudiante, considerando las relaciones, "
    "expectativas y recursos que pueden influir en la construcción de sus "
    "intereses y decisiones vocacionales."
)

with st.form(key="family_context_form"):

    with st.container(border=True):
        st.subheader("Composición Familiar")

        household_members = st.multiselect(
            label="Integrantes que conviven en el hogar:",
            options=[
                "Madre",
                "Padre",
                "Madrastra",
                "Padrastro",
                "Hermanos/as",
                "Abuelos/as",
                "Tíos/as",
                "Primos/as",
                "Tutor/a legal",
                "Otro",
            ],
            help=(
                "Selecciona todas las personas que viven actualmente "
                "con el estudiante."
            ),
        )

        family_structure_description = st.text_area(
            label="Descripción de la estructura y relaciones significativas",
            placeholder=(
                "Describe las personas significativas que participan "
                "activamente en el acompañamiento y desarrollo del "
                "estudiante, dinámicas familiares relevantes, etc."
            ),
            height=120,
        )

    with st.container(border=True):
        st.subheader("Situación Socioeconómica y Recursos")

        socioeconomic_bracket = st.selectbox(
            label=(
                "Tramo socioeconómico o caracterización del entorno "
                "(opcional):"
            ),
            options=[
                "No especificado",
                "Tramo vulnerable / Apoyo estatal",
                "Ingreso medio-bajo",
                "Ingreso medio",
                "Ingreso medio-alto / alto",
            ],
        )

        environment_resources_description = st.text_area(
            label="Condiciones y recursos del entorno",
            placeholder=(
                "Identifica condiciones físicas, financieras o de "
                "conectividad del entorno que puedan facilitar o limitar el "
                "acceso a oportunidades educativas y de desarrollo vocacional "
                "(ej. acceso a internet, libros, espacio de estudio, red de "
                "apoyo local)."
            ),
            height=130,
        )


    with st.container(border=True):
        st.subheader("Expectativas Familiares")

        family_involvement_level = st.select_slider(
            label=(
                "Nivel de involucramiento familiar en proyectos futuros "
                "del estudiante:"
            ),
            options=["Muy bajo", "Bajo", "Moderado", "Alto", "Muy alto"],
            value="Alto",
        )

        family_expectations_description = st.text_area(
            label="Aspiraciones e influencias familiares",
            placeholder=(
                "Describe las aspiraciones, orientaciones o presiones "
                "familiares sobre la continuidad de estudios "
                "técnicos/superiores, campos laborales de interés o "
                "proyectos futuros."
            ),
            height=130,
        )
        