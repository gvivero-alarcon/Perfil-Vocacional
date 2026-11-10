import streamlit as st

st.set_page_config(
    page_title="Apoyo",
    page_icon="🤝",
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
            default=st.session_state.data.get("internal_school_supports", []),
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
            default=st.session_state.data.get("external_supports", []),
        )

        support_networks_description = st.text_area(
            label="Detalle de recursos y efectividad del acompañamiento",
            placeholder=(
                "Describe cómo operan estas redes, quiénes son las personas "
                "clave y cómo facilitan el proceso de exploración vocacional "
                "y la trayectoria educativa del estudiante."
            ),
            value=st.session_state.data.get("support_networks_description", ""),
            height=130,
        )

    save_apoyo = st.form_submit_button(label="Guardar", width="content")

if save_apoyo:
    st.session_state.data["internal_school_supports"] = internal_school_supports
    st.session_state.data["external_supports"] = external_supports
    st.session_state.data["support_networks_description"] = support_networks_description
    # st.toast("Redes de apoyo guardadas correctamente.")
    st.switch_page("pages/05_Aprendizaje.py")