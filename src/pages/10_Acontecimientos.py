import streamlit as st

st.header("🗓️ Registro de Acontecimientos")
st.caption(
    "Registra los acontecimientos significativos de tu trayectoria personal "
    "y escolar, así como su valoración subjetiva (de 0 a 10) y el significado "
    "o aprendizaje asociado[cite: 1]."
)

# Inicializar la lista de acontecimientos en st.session_state si no existe
if "milestones" not in st.session_state:
    st.session_state.milestones = [
        {
            "id": 1,
            "period": "7° Básico",
            "description": "Ingreso al nuevo colegio y participación en taller de ciencias.",
            "valuation": 8,
            "category": "Escolar/Académica",
            "meaning": "Me sentí acogido y descubrí que me gustaba experimentar.",
        },
        {
            "id": 2,
            "period": "8° Básico",
            "description": "Dificultades en matemáticas durante el primer semestre.",
            "valuation": 3,
            "category": "Escolar/Académica",
            "meaning": "Aprendí a pedir ayuda a tiempo y usar nuevas estrategias de estudio.",
        },
    ]

# Formulario para agregar o editar acontecimientos
with st.form(key="milestone_form"):
    st.subheader("Agregar Nuevo Acontecimiento")

    col1, col2 = st.columns(2)
    with col1:
        milestone_period = st.selectbox(
            label="Período o curso escolar:",
            options=[
                "7° Básico",
                "8° Básico",
                "1° Medio",
                "2° Medio",
                "3° Medio",
                "4° Medio",
                # "Otro período / Edad",
            ],
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
        label="Valoración subjetiva (0 = Muy negativa, 10 = Muy positiva):",
        min_value=0,
        max_value=10,
        value=5,
        help=(
            "0: Muy negativa | 5: Intermedia o neutral | 10: Muy positiva. "
            "Esta puntuación no es una calificación de tus capacidades[cite: 1]."
        ),
    )

    milestone_meaning = st.text_area(
        label="Significado, aprendizaje o reflexión (recomendado)",
        placeholder="¿Qué significó este acontecimiento para ti o qué aprendiste?",
        height=100,
    )

    submit_milestone = st.form_submit_button(
        label="Agregar Acontecimiento",
        # use_container_width=True,
        width="stretch"
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
    for index, milestone in enumerate(st.session_state.milestones):
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
                st.write("")  # Espaciado
                if st.button("🗑️ Eliminar", key=f"del_{milestone['id']}"):
                    st.session_state.milestones.pop(index)
                    st.rerun()