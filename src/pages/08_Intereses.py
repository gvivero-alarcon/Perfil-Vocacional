import streamlit as st

st.set_page_config(
    page_title="Intereses",
    page_icon="🎯",
)

st.header("8. Intereses y motivaciones")
st.caption(
    "Explorar las actividades, experiencias y aspiraciones que despiertan "
    "interés en el estudiante, reconociendo su relación con la construcción "
    "de preferencias, expectativas y posibles trayectorias vocacionales."
)

with st.form(key="interests_motivations_form"):
    with st.container(border=True):
        st.subheader("Actividades que Disfruta")

        enjoyed_activities = st.multiselect(
            label="Áreas de disfrute, curiosidad y participación:",
            options=[
                "Actividades artísticas y creativas (dibujo, música, teatro)",
                "Deportes y actividad física",
                "Lectura, escritura o creación de relatos",
                "Experimentación científica y robótica",
                "Uso de tecnología, videojuegos o programación",
                "Participación social, voluntariado o liderazgo grupal",
                "Naturaleza, ecología o cuidado de animales",
                "Juegos de estrategia, lógica o resolución de acertijos",
            ],
            default=st.session_state.data.get("enjoyed_activities", []),
            help="Selecciona aquellas actividades que generan mayor satisfacción y motivación espontánea en el estudiante.",
        )

        activities_description = st.text_area(
            label="Detalle de experiencias y motivación intrínseca",
            placeholder=(
                "Describe las experiencias académicas, recreativas, sociales "
                "o personales que despiertan su curiosidad y cómo se vinculan "
                "con sus preferencias o futuros intereses vocacionales."
            ),
            value=st.session_state.data.get("activities_description", ""),
            height=120,
        )

    with st.container(border=True):
        st.subheader("Sueños o Metas Personales")

        personal_aspirations_description = st.text_area(
            label="Aspiraciones, proyecciones e intereses futuros",
            placeholder=(
                "Describe las metas o proyecciones que el estudiante "
                "considera significativas para su futuro (sin exigir una "
                "elección vocacional definitiva o rígida)."
            ),
            value=st.session_state.data.get("personal_aspirations_description", ""),
            height=130,
        )

    save_intereses = st.form_submit_button(label="Guardar", width="content")

if save_intereses:
    st.session_state.data["enjoyed_activities"] = enjoyed_activities
    st.session_state.data["activities_description"] = activities_description
    st.session_state.data["personal_aspirations_description"] = personal_aspirations_description
    # st.toast("Intereses y motivaciones guardados correctamente.")
    st.switch_page("pages/09_Logros.py")