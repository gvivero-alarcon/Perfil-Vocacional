import streamlit as st
import pandas as pd
import sqlite3
import hashlib

# Configuración de la página
st.set_page_config(page_title="Línea de Vida Multiusuario", layout="wide")

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA BASE DE DATOS SQLITE (Un archivo local simple: "datos.db")
# -----------------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect('datos_vocacionales.db')
    cursor = conn.cursor()
    
    # Tabla de Usuarios (Alumnos y Profesores)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT,
            rol TEXT,
            institucion TEXT,
            curso TEXT
        )
    ''')
    
    # Tabla de Hitos de la Línea de Vida
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hitos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            institucion TEXT,
            curso TEXT,
            periodo TEXT,
            categoria TEXT,
            descripcion TEXT,
            valoracion INTEGER,
            significado TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Función para encriptar contraseñas de forma simple
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# -----------------------------------------------------------------------------
# INTERFAZ DE AUTENTICACIÓN (LOGIN / REGISTRO)
# -----------------------------------------------------------------------------
st.sidebar.title("🔐 Acceso al Sistema")
menu = ["Iniciar Sesión", "Registrarse (Nuevo Alumno)"]
choice = st.sidebar.selectbox("Selecciona una opción", menu)

if choice == "Iniciar Sesión":
    st.sidebar.subheader("Credenciales")
    user = st.sidebar.text_input("Usuario o Código")
    passwd = st.sidebar.text_input("Contraseña", type="password")
    
    if st.sidebar.button("Entrar"):
        conn = sqlite3.connect('datos_vocacionales.db')
        cursor = conn.cursor()
        cursor.execute('SELECT rol, institucion, curso FROM usuarios WHERE username = ? AND password = ?', (user, make_hash(passwd)))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            st.session_state['logged_in'] = True
            st.session_state['username'] = user
            st.session_state['rol'] = result[0]
            st.session_state['institucion'] = result[1]
            st.session_state['curso'] = result[2]
            st.success(f"¡Bienvenido/a {user}!")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

elif choice == "Registrarse (Nuevo Alumno)":
    st.sidebar.subheader("Crear Cuenta de Alumno")
    new_user = st.sidebar.text_input("Nuevo Usuario / Código Estudiante")
    new_passwd = st.sidebar.text_input("Contraseña", type="password")
    inst = st.sidebar.text_input("Institución / Colegio")
    cur = st.sidebar.selectbox("Curso", ["3° Medio A", "3° Medio B", "4° Medio A", "4° Medio B"])
    
    if st.sidebar.button("Registrarme"):
        if new_user and new_passwd and inst:
            conn = sqlite3.connect('datos_vocacionales.db')
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO usuarios (username, password, rol, institucion, curso) VALUES (?, ?, ?, ?, ?)',
                               (new_user, make_hash(new_passwd), 'Alumno', inst, cur))
                conn.commit()
                conn.close()
                st.sidebar.success("¡Cuenta creada con éxito! Ve a 'Iniciar Sesión'.")
            except sqlite3.IntegrityError:
                conn.close()
                st.sidebar.error("El nombre de usuario ya existe. Elige otro.")
        else:
            st.sidebar.warning("Por favor completa todos los campos.")

# -----------------------------------------------------------------------------
# APLICACIÓN PRINCIPAL SEGÚN EL ROL
# -----------------------------------------------------------------------------
if 'logged_in' in st.session_state and st.session_state['logged_in']:
    
    # Botón para cerrar sesión
    if st.sidebar.button("Cerrar Sesión"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    rol = st.session_state['rol']
    
    # ==========================================
    # VISTA DE ALUMNO
    # ==========================================
    if rol == 'Alumno':
        st.title(f"🌱 Línea de Vida — Alumno: {st.session_state['username']}")
        st.caption(f"Institución: {st.session_state['institucion']} | Curso: {st.session_state['curso']}")
        
        st.subheader("Registrar nuevo acontecimiento")
        with st.form("form_hito_db", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                periodo = st.selectbox("Período o Curso:", ["7.º Básico", "8.º Básico", "1.º Medio", "2.º Medio", "3.º Medio", "4.º Medio"])
                categoria = st.selectbox("Categoría:", ["Escolar / Académica", "Intereses / Actividades", "Familiar / Social", "Personal"])
            with col2:
                valoracion = st.slider("Valoración (0 a 10):", 0, 10, 5)
            
            descripcion = st.text_input("Descripción breve del hito:")
            significado = st.text_area("Significado o aprendizaje (Opcional):")
            
            submitted = st.form_submit_button("Guardar en el sistema")
            if submitted and descripcion:
                conn = sqlite3.connect('datos_vocacionales.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO hitos (username, institucion, curso, periodo, categoria, descripcion, valoracion, significado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (st.session_state['username'], st.session_state['institucion'], st.session_state['curso'], periodo, categoria, descripcion, valoracion, significado))
                conn.commit()
                conn.close()
                st.success("¡Hito guardado correctamente!")
                st.rerun()

        # Mostrar solo los hitos del alumno actual
        st.subheader("Tus registros guardados:")
        conn = sqlite3.connect('datos_vocacionales.db')
        df_mis_hitos = pd.read_sql_query('SELECT periodo, categoria, descripcion, valoracion, significado FROM hitos WHERE username = ?', conn, params=(st.session_state['username'],))
        conn.close()
        
        if not df_mis_hitos.empty:
            st.dataframe(df_mis_hitos, use_container_width=True)
        else:
            st.info("Aún no tienes hitos registrados.")

    # ==========================================
    # VISTA DE PROFESOR / ORIENTADOR
    # ==========================================
    elif rol == 'Profesor':
        st.title("📊 Panel de Profesor / Orientador")
        st.write(f"Monitoreo de respuestas para la institución: **{st.session_state['institucion']}**")
        
        conn = sqlite3.connect('datos_vocacionales.db')
        df_curso = pd.read_sql_query('SELECT username, curso, periodo, categoria, descripcion, valoracion, significado FROM hitos WHERE institucion = ?', conn, params=(st.session_state['institucion'],))
        conn.close()
        
        if not df_curso.empty:
            curso_sel = st.selectbox("Filtrar por curso:", ["Todos"] + list(df_curso['curso'].unique()))
            if curso_sel != "Todos":
                df_curso = df_curso[df_curso['curso'] == curso_sel]
                
            st.subheader("Respuestas de los alumnos")
            st.dataframe(df_curso, use_container_width=True)
            
            # Botón de descarga CSV para el profe
            csv = df_curso.to_csv(index=False).encode('utf-8')
            st.download_button("Descargar reporte en CSV", csv, "reporte_curso.csv", "text/csv")
        else:
            st.info("No hay registros de alumnos en tu institución todavía.")

else:
    st.title("🌱 Plataforma de Orientación Vocacional")
    st.info("👈 Por favor, inicia sesión o regístrate en la barra lateral para comenzar.")
    
    # Nota para crear un profesor de prueba rápidamente
    with st.expander("¿Quieres probar como Profesor de prueba?"):
        st.write("Puedes registrar un usuario manualmente ejecutando una vez un script de prueba o creando un usuario administrador con rol 'Profesor' en la base de datos SQLite.")
        if st.button("Crear cuenta de Profesor de Prueba (Colegio Liceo A-1)"):
            conn = sqlite3.connect('datos_vocacionales.db')
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO usuarios (username, password, rol, institucion, curso) VALUES (?, ?, ?, ?, ?)',
                               ('profesor_juan', make_hash('1234'), 'Profesor', 'Liceo A-1', 'General'))
                conn.commit()
                st.success("¡Usuario creado! Inicia sesión con el usuario: `profesor_juan` y contraseña: `1234`")
            except:
                st.warning("El usuario de prueba ya existe.")
            conn.close()