# Mi línea de vida (Streamlit)

Herramienta de reflexión para estudiantes de enseñanza media, profesores jefes y orientadores.
Sin cuentas, sin base de datos, sin analítica; no escribe nada en disco. No diagnostica ni recomienda carreras.

## Ejecutar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```
Se abre en http://localhost:8501. Para usarla sin conexión en un computador del colegio, basta con esa instalación.

## Privacidad: decisión importante
Streamlit **siempre ejecuta Python en un servidor**. Los textos se guardan solo en la memoria de la sesión
(se pierden al cerrar o al pulsar «Borrar mis datos»), pero **sí viajan al servidor donde corra la app**.
- **Máxima privacidad:** ejecutarla en un computador/servidor del propio establecimiento (red local).
- **Alojamiento gratuito (p. ej. Streamlit Community Cloud u otro):** los relatos pasarían por un servidor de terceros,
  lo que se aparta del principio «sin transmisión a servidores». Verifiquen condiciones del proveedor y
  obtengan la aprobación institucional/jurídica antes de usarlo con estudiantes.
- `.streamlit/config.toml` desactiva la telemetría de Streamlit.
- Para una versión 100 % local en el navegador (sin servidor) habría que reescribirla como app estática (HTML/JS).

## Publicar gratis (si el punto anterior se acepta)
1. Subir esta carpeta a un repositorio público de GitHub (sin datos de estudiantes).
2. En share.streamlit.io: *New app* → elegir repositorio, rama y `app.py`.
3. Compartir el enlace con los estudiantes. Verificar antes las condiciones vigentes del servicio.

## Manual breve para profesores
1. Explique el propósito: reflexionar, no evaluar. La valoración 0–10 es personal, no una nota.
2. Aclare que cada estudiante decide qué incluir y que no debe escribir nombres de terceros ni datos íntimos.
3. Pasos: Inicio → Períodos → Acontecimientos → Mi línea de vida → Reflexión → Resumen y descarga (~30–40 min).
4. El estudiante descarga: **PDF** (para sí), **CSV** (para el establecimiento; separador `;`, abre bien en Excel y LibreOffice)
   y **respaldo .json** (para continuar después desde «Inicio»).
5. Las «pistas para profundizar» son preguntas de conversación, no conclusiones. Resguarde los archivos según el protocolo del colegio.
6. Adapte el texto «¿Quién verá mi información?» en `paso_inicio()` de `app.py`.
7. Use datos para investigación solo con revisión ética y consentimiento/asentimiento.
