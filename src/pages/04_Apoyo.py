import streamlit as st


st.set_page_config(
    page_title="Apoyo",
    page_icon="🤝"
)

st.header("4. Redes de apoyo con que cuenta")
st.caption(
    "Identificar las personas, instituciones y recursos disponibles para "
    "acompañar al estudiante en su trayectoria educativa y proceso de "
    "exploración vocacional."
)

with st.form(key="support_networks_form"):
    with st.container(border=True):
        st.subheader("Identificación de Redes de Apoyo")

        internal_school_supports = st.multiselect(
            label="Redes o programas internos del establecimiento:",
            options=[
                "Profesor/a Jefe",
                "Equipo PIE",
                "Orientación / Psicopedagogía",
                "Convivencia Escolar",
                "Psicólogo/a Escolar",
                "Tutor/a de asignatura",
                "Talleres extraprogramáticos",
            ],
            help="Selecciona los apoyos internos activos en el colegio.",
        )

        external_supports = st.multiselect(
            label="Redes institucionales o comunitarias externas:",
            options=[
                "Salud Mental (COSAM / CESFAM)",
                "Programas de apoyo social / Municipalidad",
                "Preuniversitario / Refuerzo externo",
                "Organizaciones comunitarias o deportivas",
                "Familia extendida o mentores externos",
                "Ninguna red externa activa",
            ],
        )

        support_networks_description = st.text_area(
            label="Detalle de recursos y efectividad del acompañamiento",
            placeholder=(
                "Describe cómo operan estas redes, quiénes son las personas "
                "clave y cómo facilitan el proceso de exploración vocacional "
                "y la trayectoria educativa del estudiante."
            ),
            height=130,
        )