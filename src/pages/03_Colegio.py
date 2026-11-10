import streamlit as st


st.set_page_config(
    page_title="Colegio",
    page_icon="🏫"
)

st.header("3. Relación con compañeros y profesores")
st.caption(
    "Caracterizar los vínculos interpersonales que establece en el contexto "
    "escolar y su incidencia en la participación, integración y confianza "
    "personal."
)

with st.form(key="peer_teacher_relations_form"):
    with st.container(border=True):
        st.subheader("Vínculos e Integración Escolar")

        peer_relationship_level = st.selectbox(
            label="Integración y relación con pares (compañeros/as):",
            options=[
                "No observada / Sin información",
                "Muy participativo/a y totalmente integrado/a",
                "Relaciones cordiales y participación regular",
                "Selectivo/a (grupo reducido de confianza)",
                "Aislado/a o con dificultades de integración",
                "Presenta conflictos recurrentes",
            ],
        )

        teacher_relationship_level = st.selectbox(
            label="Vínculo y comunicación con profesores/as:",
            options=[
                "No observada / Sin información",
                "Fluida, de confianza y búsqueda activa de apoyo",
                "Respetuosa pero distante / Formal",
                "Pasiva / Solo responde cuando se le requiere",
                "Resistencia a la autoridad o baja comunicación",
            ],
        )

        interpersonal_bonds_description = st.text_area(
            label="Descripción del impacto en la participación y confianza",
            placeholder=(
                "Describe cómo los vínculos con compañeros y profesores "
                "inciden en su participación en clase, trabajo en equipo, "
                "seguridad y confianza personal dentro del establecimiento."
            ),
            height=130,
        )