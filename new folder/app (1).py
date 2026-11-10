import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Línea de Vida y Perfil Vocacional",
    page_icon="🌱",
    layout="wide"
)

# Estilo visual accesible y sobrio
st.title("🌱 Línea de Vida y Perfil Vocacional")
st.caption("Herramienta educativa de reflexión para estudiantes de enseñanza media")

# Inicialización del estado de la sesión (Session State)
if 'hitos' not in st.session_state:
    st.session_state.hitos = []
if 'paso' not in st.session_state:
    st.session_state.paso = 1

# Aviso de Privacidad por Diseño
st.info(
    "🔒 **Privacidad garantizada:** Esta actividad es personal. No solicitamos tu nombre "
    "ni datos personales obligatorios. Todo se procesa localmente en esta sesión."
)

# BARRA DE NAVEGACIÓN EN LA BARRA LATERAL
st.sidebar.title("Navegación")
pasos_titulos = [
    "1. Inicio e Instrucciones",
    "2. Registro de Acontecimientos",
    "3. Gráfico de Línea de Vida",
    "4. Preguntas de Reflexión",
    "5. Pistas Vocacionales",
    "6. Exportar Resultados"
]

paso_seleccionado = st.sidebar.radio("Ir al paso:", pasos_titulos, index=st.session_state.paso - 1)
st.session_state.paso = pasos_titulos.index(paso_seleccionado) + 1

st.divider()

# -----------------------------------------------------------------------------
# PASO 1: INICIO
# -----------------------------------------------------------------------------
if st.session_state.paso == 1:
    st.header("1. Bienvenida y Propósito")
    st.write("""
    Esta aplicación te acompaña a construir tu **línea de vida personal y escolar**, 
    ayudándote a identificar tus vivencias más significativas, aprendizajes y proyecciones 
    para la construcción de tu perfil vocacional.
    """)
    
    codigo = st.text_input("Código o identificador de estudiante (Opcional, si tu profesor/a lo solicita):", key="codigo_estudiante")
    
    st.markdown("---")
    if st.button("Comenzar a registrar hitos ➡️", type="primary"):
        st.session_state.paso = 2
        st.rerun()

# -----------------------------------------------------------------------------
# PASO 2: REGISTRO DE HITOS
# -----------------------------------------------------------------------------
elif st.session_state.paso == 2:
    st.header("2. Registro de Acontecimientos Significativos")
    st.write("Agrega los hitos importantes de tu trayectoria escolar o personal. Puedes agregar todos los que desees.")

    with st.form("form_hito", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            periodo = st.selectbox(
                "Período o Curso:",
                ["7.º Básico", "8.º Básico", "1.º Medio", "2.º Medio", "3.º Medio", "4.º Medio", "Otro / Etapa previa"]
            )
            categoria = st.selectbox(
                "Categoría:",
                ["Escolar / Académica", "Intereses / Actividades", "Familiar / Social", "Personal", "Comunitaria"]
            )
        with col2:
            valoracion = st.slider(
                "Valoración subjetiva (0 = Muy negativa, 5 = Neutral, 10 = Muy positiva):",
                min_value=0, max_value=10, value=5
            )
        
        descripcion = st.text_input("Descripción breve del acontecimiento (Obligatorio):", placeholder="Ej: Participé en la feria científica del colegio.")
        significado = st.text_area("Significado o aprendizaje asociado (Opcional):", placeholder="¿Qué significó para ti o qué aprendiste?")

        submitted = st.form_submit_button("➕ Agregar Acontecimiento", type="primary")
        if submitted:
            if descripcion.strip() == "":
                st.error("Por favor, ingresa una descripción para el acontecimiento.")
            else:
                st.session_state.hitos.append({
                    "Periodo": periodo,
                    "Categoria": categoria,
                    "Descripcion": descripcion,
                    "Valoracion": valoracion,
                    "Significado": significado
                })
                st.success("¡Acontecimiento agregado con éxito!")

    st.subheader("Tus acontecimientos registrados:")
    if len(st.session_state.hitos) == 0:
        st.info("Aún no has agregado ningún acontecimiento.")
    else:
        df_hitos = pd.DataFrame(st.session_state.hitos)
        st.dataframe(df_hitos[["Periodo", "Categoria", "Descripcion", "Valoracion", "Significado"]], use_container_width=True)
        
        if st.button("🗑️ Borrar último acontecimiento"):
            st.session_state.hitos.pop()
            st.rerun()

    st.markdown("---")
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav2:
        if st.button("Ver Gráfico de Línea de Vida ➡️", type="primary"):
            if len(st.session_state.hitos) == 0:
                st.warning("Agrega al menos un acontecimiento antes de avanzar.")
            else:
                st.session_state.paso = 3
                st.rerun()

# -----------------------------------------------------------------------------
# PASO 3: VISUALIZACIÓN DE LA LÍNEA DE VIDA
# -----------------------------------------------------------------------------
elif st.session_state.paso == 3:
    st.header("3. Gráfico de tu Línea de Vida")
    
    if len(st.session_state.hitos) == 0:
        st.warning("No hay datos para mostrar. Vuelve al paso 2 para agregar hitos.")
    else:
        df = pd.DataFrame(st.session_state.hitos)
        
        # Gráfico interactivo con Plotly
        fig = px.line(
            df, 
            x="Periodo", 
            y="Valoracion", 
            text="Descripcion",
            markers=True,
            hover_data=["Categoria", "Significado"],
            title="Trayectoria de Acontecimientos y Valoración Subjetiva"
        )
        fig.update_traces(textposition="top center", marker=dict(size=10, color='#2563eb'))
        fig.update_layout(
            yaxis=dict(range=[-0.5, 10.5], dtick=1, title="Valoración (0 a 10)"),
            xaxis=dict(title="Período / Curso"),
            height=450
        )
        
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    if st.button("Continuar a Preguntas de Reflexión ➡️", type="primary"):
        st.session_state.paso = 4
        st.rerun()

# -----------------------------------------------------------------------------
# PASO 4: REFLEXIÓN PERSONAL
# -----------------------------------------------------------------------------
elif st.session_state.paso == 4:
    st.header("4. Preguntas de Reflexión Personal")
    st.write("Responde libremente a las siguientes preguntas para profundizar en tu historia. Ninguna respuesta es obligatoria.")

    r1 = st.text_area("1. ¿Qué acontecimientos consideras especialmente importantes en tu trayectoria?", key="ref_1")
    r2 = st.text_area("2. ¿Qué experiencias te hicieron sentir que aprendías o eras capaz de hacer algo?", key="ref_2")
    r3 = st.text_area("3. ¿Qué actividades o asignaturas has disfrutado y qué te atrae de ellas?", key="ref_3")
    r4 = st.text_area("4. ¿Qué dificultades has enfrentado y qué estrategias utilizaste?", key="ref_4")
    r5 = st.text_area("5. ¿Qué metas u objetivos te gustaría plantearte a corto o mediano plazo?", key="ref_5")

    st.markdown("---")
    if st.button("Ver Pistas para el Perfil Vocacional ➡️", type="primary"):
        st.session_state.paso = 5
        st.rerun()

# -----------------------------------------------------------------------------
# PASO 5: PISTAS PARA EL PERFIL VOCACIONAL
# -----------------------------------------------------------------------------
elif st.session_state.paso == 5:
    st.header("5. Pistas para tu Perfil Vocacional")
    st.write("Estas dimensiones emergen de tus registros como insumo para dialogar con tu profesor/a jefe o persona orientadora:")

    if len(st.session_state.hitos) > 0:
        df = pd.DataFrame(st.session_state.hitos)
        academicos = df[(df['Categoria'] == 'Escolar / Académica') & (df['Valoracion'] >= 7)]
        intereses = df[(df['Categoria'] == 'Intereses / Actividades') & (df['Valoracion'] >= 7)]
        dificultades = df[df['Valoracion'] <= 4]

        if not academicos.empty:
            st.success(f"⭐ **Fortalezas Académicas:** Destacan vivencias muy positivas en áreas escolares como: *{', '.join(academicos['Descripcion'].tolist())}*.")
        if not intereses.empty:
            st.info(f"🎨 **Intereses y Motivaciones:** Muestras entusiasmo en actividades como: *{', '.join(intereses['Descripcion'].tolist())}*.")
        if not dificultades.empty:
            st.warning(f"🌱 **Áreas de Desafío y Resiliencia:** Has registrado momentos complejos (*{', '.join(dificultades['Descripcion'].tolist())}*). Reflexionar sobre cómo los afrontaste revela tus estrategias de aprendizaje.")
    else:
        st.info("Registra más hitos en el Paso 2 para ver análisis específicos.")

    st.markdown("---")
    if st.button("Ir a Exportación de Resultados ➡️", type="primary"):
        st.session_state.paso = 6
        st.rerun()

# -----------------------------------------------------------------------------
# PASO 6: EXPORTACIÓN
# -----------------------------------------------------------------------------
elif st.session_state.paso == 6:
    st.header("6. Exportar y Conservar Resultados")
    st.write("Descarga los archivos con tu información para guardarlos en tu equipo o compartirlos en tu proceso de orientación.")

    if len(st.session_state.hitos) > 0:
        df = pd.DataFrame(st.session_state.hitos)
        
        # Exportación CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Descargar Datos en CSV (Compatible con Excel)",
            data=csv,
            file_name="linea_de_vida_datos.csv",
            mime="text/csv"
        )

    st.markdown("---")
    if st.button("🗑️ Borrar todos los datos de esta sesión", type="secondary"):
        st.session_state.hitos = []
        st.session_state.paso = 1
        st.success("Datos eliminados correctamente.")
        st.rerun()