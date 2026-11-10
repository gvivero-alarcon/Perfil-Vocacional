import streamlit as st

st.set_page_config(
    page_title="Aprendizaje",
    page_icon="🧠",
)

st.header("5. Estilo y ritmo de aprendizaje")
st.caption(
    "Describir las formas, estrategias y condiciones que favorecen el "
    "aprendizaje del estudiante, considerando sus preferencias, tiempos y "
    "necesidades de apoyo en distintas experiencias educativas."
)

st.info(
    "💡 **Orientación Pedagógica:** Evitar clasificar al estudiante mediante "
    "estilos de aprendizaje fijos (como categorizaciones rígidas VAK: visual, "
    "auditivo o kinestésico), ya que no existe evidencia suficiente que "
    "sostenga que enseñar según estas categorías mejore el aprendizaje. Se "
    "recomienda enfocar la descripción en las estrategias pedagógicas, ritmos "
    "de trabajo y apalancamientos concretos que potencian su desarrollo.",
    icon="ℹ️",
)

with st.form(key="learning_style_pace_form"):
    with st.container(border=True):
        st.subheader("Condiciones y Estrategias de Aprendizaje")

        work_pace = st.select_slider(
            label="Ritmo habitual de trabajo y procesamiento:",
            options=[
                "Pausado (requiere más tiempo)",
                "Variable según asignatura",
                "Promedio / Estándar",
                "Rápido / Autónomo",
            ],
            value=st.session_state.data.get("work_pace", "Promedio / Estándar"),
        )

        facilitating_strategies = st.multiselect(
            label="Estrategias y condiciones que favorecen su aprendizaje:",
            options=[
                "Uso de organizadores gráficos y esquemas",
                "Trabajo colaborativo y discusión en grupo",
                "Instrucciones paso a paso / Modelamiento",
                "Actividades prácticas / Aprendizaje basado en proyectos",
                "Estudio autónomo con guía",
                "Tiempos extendidos para evaluaciones",
                "Fragmentación de tareas complejas",
                "Ambientes estructurados con pocas distracciones",
            ],
            default=st.session_state.data.get("facilitating_strategies", []),
        )

        learning_conditions_description = st.text_area(
            label="Descripción cualitativa del proceso de aprendizaje",
            placeholder=(
                "Describe las condiciones específicas, nivel de autonomía, "
                "respuesta ante el error, tolerancia a la frustración y "
                "necesidades específicas de apoyo pedagógico en el aula."
            ),
            value=st.session_state.data.get("learning_conditions_description", ""),
            height=140,
        )

    save_aprendizaje = st.form_submit_button(label="Guardar", width="content")

if save_aprendizaje:
    st.session_state.data["work_pace"] = work_pace
    st.session_state.data["facilitating_strategies"] = facilitating_strategies
    st.session_state.data["learning_conditions_description"] = learning_conditions_description
    # st.toast("Estilo y ritmo de aprendizaje guardado correctamente.")
    st.switch_page("pages/06_Fortalezas.py")