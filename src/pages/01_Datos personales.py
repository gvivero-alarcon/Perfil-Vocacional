import streamlit as st
from datetime import date


st.set_page_config(
    page_title="Datos personales",
    page_icon="👤",
    layout="centered"
)

st.header("1. Datos personales")
st.caption(
    "Registrar los antecedentes generales que permiten contextualizar al "
    "estudiante y reconocer la etapa de desarrollo y trayectoria escolar en "
    "que se encuentra."
)

with st.form(key="personal_data_form"):
    col1, col2 = st.columns([2, 1])

    with col1:
        full_name = st.text_input(
            label="Nombre completo",
            placeholder="Ej. Juan Pérez",
            value=st.session_state.data["full_name"]
        )

    with col2:
        age = st.number_input(
            label="Edad",
            value=st.session_state.data["age"],
            min_value=0,
            max_value=100,
            step=1
        )

    col3, col4 = st.columns(2)

    with col3:
        date_of_birth = st.date_input(
            label="Fecha de nacimiento",
            value=st.session_state.data["date_of_birth"],
            min_value=date(1990, 1, 1),
            max_value=date.today(),
            format="DD/MM/YYYY"
        )

    with col4:
        school_grade = st.selectbox(
            label="Año escolar",
            options=[
                "7° Básico",
                "8° Básico",
                "1° Medio",
                "2° Medio",
                "3° Medio",
                "4° Medio"
            ],
            # value=st.session_state.data["school_grade"]
        )

    save = st.form_submit_button(
        label="Guardar",
        width="content"
    )

if save:
    if not full_name.strip():
        st.error("Por favor, ingrese su nombre completo antes de continuar.")
    else:
        st.session_state.data["full_name"] = full_name
        st.session_state.data["age"] = age
        st.session_state.data["date_of_birth"] = date_of_birth
        st.session_state.data["school_grade"] = school_grade
        st.toast("Datos personales registrados correctamente.")
        