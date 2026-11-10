import streamlit as st

st.header("🗓️ Registro de Acontecimientos")
st.caption(
    "Registra los acontecimientos significativos de tu trayectoria personal "
    "y escolar, así como su valoración subjetiva (de 0 a 10) y el significado "
    "o aprendizaje asociado."
)

if "milestones" not in st.session_state:
    st.session_state.milestones = []

with st.form(key="milestone_form", clear_on_submit=True):
    st.subheader("Agregar Nuevo Acontecimiento")

    col1, col2 = st.columns(2)
    with col1:
        # Listado escolar completo desde Pre-kínder hasta 4° Medio
        milestone_period = st.selectbox(
            label="Período o curso escolar:",
            options=[
                "Pre-kínder",
                "Kínder",
                "1° Básico",
                "2° Básico",
                "3° Básico",
                "4° Básico",
                "5° Básico",
                "6° Básico",
                "7° Básico",
                "8° Básico",
                "1° Medio",
                "2° Medio",
                "3° Medio",
                "4° Medio",
            ],
            # index=0,
        )
    with col2:
        milestone_category = st.selectbox(
            label="Categoría del acontecimiento:",
            options=[
                "Escolar/Académica",
                "Intereses/Actividades",
                "Familiar/Social",
                "Personal",
                "Comunitaria / Otra",
            ],
        )

    milestone_description = st.text_input(
        label="Descripción breve del acontecimiento",
        placeholder="Ej. Participación en feria científica o cambio importante.",
    )

    milestone_valuation = st.slider(
        label="Valoración subjetiva:",
        min_value=0,
        max_value=10,
        value=5,
    )

    # Indicación estilizada de la escala de valoración
    st.markdown(
        """
        <div style="padding: 8px 12px; background-color: #f0f2f6; border-radius: 6px; font-size: 13px; color: #31333F; margin-bottom: 10px;">
            <b>Guía de valoración:</b> 
            <span style="color: #d32f2f;">0 - Muy negativa</span> &nbsp;|&nbsp; 
            <span style="color: #6c757d;">5 - Ni positiva ni negativa</span> &nbsp;|&nbsp; 
            <span style="color: #2e7d32;">10 - Muy positiva</span><br>
        </div>
        """,
        unsafe_allow_html=True,
    )

    milestone_meaning = st.text_area(
        label="¿Qué significó este acontecimiento para ti o qué aprendiste?",
        placeholder="Escribe aquí tu reflexión o aprendizaje...",
        height=100,
    )

    submit_milestone = st.form_submit_button(
        label="Agregar Acontecimiento",
        width="stretch",
    )

if submit_milestone:
    if not milestone_description.strip():
        st.error("Por favor, ingresa una descripción para el acontecimiento.")
    else:
        new_id = (
            max([m["id"] for m in st.session_state.milestones]) + 1
            if st.session_state.milestones
            else 1
        )
        st.session_state.milestones.append(
            {
                "id": new_id,
                "period": milestone_period,
                "description": milestone_description,
                "valuation": milestone_valuation,
                "category": milestone_category,
                "meaning": milestone_meaning,
            }
        )
        st.success("¡Acontecimiento registrado exitosamente!")
        st.rerun()

st.markdown("---")
st.subheader("📋 Listado de Acontecimientos Registrados")

if not st.session_state.milestones:
    st.info("Aún no has registrado ningún acontecimiento.")
else:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        sort_option = st.selectbox(
            "Ordenar listado por:",
            options=[
                "Cronológico (por orden de período)",
                "Valoración (Mayor a menor)",
                "Valoración (Menor a mayor)",
            ],
        )
    with col_f2:
        filter_category = st.selectbox(
            label="Filtrar por categoría:",
            options=["Todas"] + list(set([m["category"] for m in st.session_state.milestones])),
        )

    display_list = list(st.session_state.milestones)

    if filter_category != "Todas":
        display_list = [m for m in display_list if m["category"] == filter_category]

    # Diccionario de orden cronológico actualizado con toda la trayectoria escolar
    period_order = {
        "Pre-kínder": 0,
        "Kínder": 1,
        "1° Básico": 2,
        "2° Básico": 3,
        "3° Básico": 4,
        "4° Básico": 5,
        "5° Básico": 6,
        "6° Básico": 7,
        "7° Básico": 8,
        "8° Básico": 9,
        "1° Medio": 10,
        "2° Medio": 11,
        "3° Medio": 12,
        "4° Medio": 13,
    }

    if "Cronológico" in sort_option:
        display_list.sort(key=lambda x: period_order.get(x["period"], 99))
    elif "Mayor a menor" in sort_option:
        display_list.sort(key=lambda x: x["valuation"], reverse=True)
    else:
        display_list.sort(key=lambda x: x["valuation"])

    for milestone in display_list:
        real_index = next(
            i for i, m in enumerate(st.session_state.milestones) if m["id"] == milestone["id"]
        )

        with st.container(border=True):
            col_info, col_actions = st.columns([4, 1])

            with col_info:
                st.markdown(
                    f"**[{milestone['period']}]** - *{milestone['category']}* "
                    f"(Valoración: **{milestone['valuation']}/10**)"
                )
                st.write(f"**Hito:** {milestone['description']}")
                if milestone["meaning"]:
                    st.caption(f"**Reflexión:** {milestone['meaning']}")

            with col_actions:
                st.write("")
                if st.button("🗑️ Eliminar", key=f"del_{milestone['id']}"):
                    st.session_state.milestones.pop(real_index)
                    st.rerun()