import streamlit as st

st.set_page_config(
    page_title="Colegio",
    page_icon="🏫",
)

st.header("3. Relación con compañeros y profesores")
st.caption(
    "Caracterizar los vínculos interpersonales que establece en el contexto "
    "escolar y su incidencia en la participación, integración y confianza "
    "personal."
)

peer_options = [
    "No observada / Sin información",
    "Muy participativo/a y totalmente integrado/a",
    "Relaciones cordiales y participación regular",
    "Selectivo/a (grupo reducido de confianza)",
    "Aislado/a o con dificultades de integración",
    "Presenta conflictos recurrentes",
]
saved_peer = st.session_state.data.get("peer_relationship_level", peer_options[0])
peer_index = peer_options.index(saved_peer) if saved_peer in peer_options else 0

teacher_options = [
    "No observada / Sin información",
    "Fluida, de confianza y búsqueda activa de apoyo",
    "Respetuosa pero distante / Formal",
    "Pasiva / Solo responde cuando se le requiere",
    "Resistencia a la autoridad o baja comunicación",
]
saved_teacher = st.session_state.data.get("teacher_relationship_level", teacher_options[0])
teacher_index = teacher_options.index(saved_teacher) if saved_teacher in teacher_options else 0

with st.form(key="peer_teacher_relations_form"):
    with st.container(border=True):
        st.subheader("Vínculos e Integración Escolar")

        peer_relationship_level = st.selectbox(
            label="Integración y relación con pares (compañeros/as):",
            options=peer_options,
            index=peer_index,
        )

        teacher_relationship_level = st.selectbox(
            label="Vínculo y comunicación con profesores/as:",
            options=teacher_options,
            index=teacher_index,
        )

        interpersonal_bonds_description = st.text_area(
            label="Descripción del impacto en la participación y confianza",
            placeholder=(
                "Describe cómo los vínculos con compañeros y profesores "
                "inciden en su participación en clase, trabajo en equipo, "
                "seguridad y confianza personal dentro del establecimiento."
            ),
            value=st.session_state.data.get("interpersonal_bonds_description", ""),
            height=130,
        )

    save_colegio = st.form_submit_button(label="Guardar", width="content")

if save_colegio:
    st.session_state.data["peer_relationship_level"] = peer_relationship_level
    st.session_state.data["teacher_relationship_level"] = teacher_relationship_level
    st.session_state.data["interpersonal_bonds_description"] = interpersonal_bonds_description
    # st.toast("Relación escolar guardada correctamente.")
    st.switch_page("pages/04_Apoyo.py")