"""Mi línea de vida: herramienta de reflexión para el perfil vocacional.
Sin cuentas, sin base de datos, sin analítica. Nada se escribe en disco ni se envía a terceros:
los datos viven solo en la memoria de la sesión y se pierden al cerrar o al borrar."""
import csv, io, json, uuid
from collections import Counter
from datetime import date
from xml.sax.saxutils import escape

import textwrap
from html import escape as hesc
import plotly.graph_objects as go
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st



# st.set_page_config(page_title="Mi línea de vida", page_icon="🧭", layout="centered")
st.markdown("""<style>
.stButton>button,.stDownloadButton>button{min-height:3rem;font-size:1.05rem;border-radius:.6rem}
html{font-size:17px}
</style>""", unsafe_allow_html=True)

# ---------------- Constantes ----------------
CURSOS = ["7.º básico", "8.º básico", "1.º medio", "2.º medio", "3.º medio", "4.º medio"]
EDADES = [f"{a} años" for a in range(10, 20)]
Y = date.today().year
ANIOS = [str(a) for a in range(Y - 9, Y + 2)]
MAESTRO = {"Curso escolar": CURSOS, "Edad": EDADES, "Año": ANIOS}
RANGO0 = {"Curso escolar": ("7.º básico", "2.º medio"), "Edad": ("12 años", "17 años"),
          "Año": (str(Y - 6), str(Y))}
TODOS = CURSOS + EDADES + ANIOS
CATS = ["Sin categoría", "Escolar / académica", "Intereses / actividades",
        "Familiar / social", "Personal", "Comunitaria", "Otra"]
MARK = dict(zip(CATS, ["o", "s", "^", "D", "P", "v", "X"]))
PASOS = ["Inicio", "Períodos", "Acontecimientos", "Mi línea de vida", "Reflexión", "Resumen y descarga"]

PREGUNTAS = [
    "¿Qué acontecimientos consideras especialmente importantes en tu trayectoria?",
    "¿Qué experiencias te hicieron sentir que aprendías o eras capaz de hacer algo?",
    "¿Qué actividades o asignaturas has disfrutado? ¿Qué te atrae de ellas?",
    "¿Qué dificultades has enfrentado y qué estrategias utilizaste?",
    "¿Qué personas, grupos o espacios te han apoyado?",
    "¿Qué experiencias cambiaron tus intereses o la manera de imaginar tu futuro?",
    "¿Qué te gustaría seguir explorando o aprendiendo?",
    "¿Qué metas te gustaría plantearte a corto o mediano plazo?",
]
# Pistas para profundizar (nunca conclusiones): categoría -> (dimensión, pregunta)
PISTA_CAT = {
    "Escolar / académica": ("Fortalezas académicas y logros", "¿Qué hiciste o aprendiste aquí que te hizo sentir capaz? ¿Qué te gustaría seguir desarrollando?"),
    "Intereses / actividades": ("Intereses y motivaciones", "¿Qué te atrajo de esta actividad? ¿Te gustaría explorarla más?"),
    "Familiar / social": ("Redes de apoyo y contexto familiar/social", "¿Qué personas o espacios te apoyaron o fueron importantes en este momento?"),
    "Comunitaria": ("Habilidades sociales y emocionales", "¿Qué aprendiste al colaborar o participar con otras personas?"),
    "Personal": ("Estrategias y estilo de aprendizaje", "¿Qué estrategias usaste o qué aprendiste de esta experiencia?"),
}
PISTA_REFL = {
    1: ("Fortalezas académicas y logros", "¿Qué te hace sentir capaz en estas experiencias y cómo podrías seguir desarrollándolo?"),
    2: ("Intereses y motivaciones", "¿Qué de estas actividades o asignaturas te entusiasma y por qué?"),
    3: ("Áreas de mejora, estrategias y estilo de aprendizaje", "¿Qué estrategias te han resultado útiles y cuáles podrías probar?"),
    4: ("Redes de apoyo y contexto familiar/social", "¿Con qué apoyos cuentas hoy y cuáles te gustaría fortalecer?"),
    5: ("Intereses y motivaciones", "¿Cómo ha cambiado lo que te interesa o lo que imaginas para tu futuro?"),
    6: ("Metas y proyecciones vocacionales", "¿Cómo podrías explorar eso en los próximos meses?"),
    7: ("Metas y proyecciones vocacionales", "¿Qué primer paso concreto podrías dar?"),
}
AVISO = "La valoración es subjetiva y personal: no es una nota, una evaluación psicológica ni un diagnóstico. La línea de vida es solo una herramienta de reflexión y no recomienda carreras."

# ---------------- Estado ----------------
S = st.session_state
for k, v in dict(step=0, eventos=[], unidad="Curso escolar", rangos={}, refl={}, edit=None,
                 delid=None, fk=0, borrar=False).items():
    S.setdefault(k, v)


def periodos():
    m = MAESTRO[S.unidad]
    a, b = S.rangos.get(S.unidad, RANGO0[S.unidad])
    base = m[m.index(a): m.index(b) + 1]
    extra = sorted({e["periodo"] for e in S.eventos} - set(base), key=lambda p: TODOS.index(p) if p in TODOS else 999)
    return base + extra


def ordenados():
    P = periodos()
    return sorted(S.eventos, key=lambda e: P.index(e["periodo"]) if e["periodo"] in P else 999)


def aspectos():
    out = [(f"Hito {n}", *PISTA_CAT[e["cat"]]) for n, e in enumerate(ordenados(), 1) if e["cat"] in PISTA_CAT]
    out += [(f"Reflexión {i + 1}", *PISTA_REFL[i]) for i in sorted(PISTA_REFL) if S.refl.get(i, "").strip()]
    return out


# ---------------- Gráfico ----------------
def grafico_png():
    P, ev = periodos(), ordenados()
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=130)
    cnt, seen, pts = Counter(e["periodo"] for e in ev), Counter(), []
    for e in ev:
        k, i = cnt[e["periodo"]], seen[e["periodo"]]
        seen[e["periodo"]] += 1
        pts.append((P.index(e["periodo"]) + (0 if k == 1 else -0.28 + 0.56 * i / (k - 1)), e["val"], e["cat"]))
    if len(pts) > 1:  # la línea solo indica secuencia, no causalidad
        ax.plot([p[0] for p in pts], [p[1] for p in pts], ls="--", color="#9aa8b5", lw=1.2, zorder=1)
    for n, (x, y, c) in enumerate(pts, 1):
        ax.scatter(x, y, s=330, marker=MARK[c], color="#1f4e79", edgecolor="white", zorder=3,
                   label=c if c != "Sin categoría" and c not in ax.get_legend_handles_labels()[1] else None)
        ax.text(x, y, str(n), color="white", ha="center", va="center", fontsize=8, fontweight="bold", zorder=4)
    ax.set_xticks(range(len(P)))
    ax.set_xticklabels(P, rotation=30 if len(P) > 7 else 0, ha="right" if len(P) > 7 else "center")
    ax.set_xlim(-0.6, len(P) - 0.4)
    ax.set_ylim(-0.6, 10.6)
    ax.set_yticks(range(11))
    ax.set_yticklabels({0: "0 · muy negativa", 5: "5 · intermedia", 10: "10 · muy positiva"}.get(i, str(i)) for i in range(11))
    ax.set_xlabel(f"Tiempo ({S.unidad.lower()})")
    ax.set_ylabel("Valoración personal (0 a 10)")
    ax.grid(alpha=.25)
    if ax.get_legend_handles_labels()[1]:
        ax.legend(loc="upper center", bbox_to_anchor=(.5, -.2), ncol=3, frameon=False, fontsize=8)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    return buf.getvalue()


SIMB = dict(zip(CATS, ["circle", "square", "triangle-up", "diamond", "cross", "triangle-down", "x"]))
ETIQ_Y = [{0: "0 · muy negativa", 5: "5 · intermedia", 10: "10 · muy positiva"}.get(v, str(v)) for v in range(11)]
PLOT_CFG = {"displayModeBar": False}


def _hover(n, e):
    fmt = lambda t: "<br>".join(hesc(l) for l in textwrap.wrap(t, 48))
    h = f"<b>{n}. {hesc(e['periodo'])}</b> · valoración {e['val']}/10<br>{fmt(e['desc'])}"
    if e["cat"] != "Sin categoría":
        h += f"<br><i>Categoría: {hesc(e['cat'])}</i>"
    if e["sig"]:
        h += f"<br><br><b>Significado:</b><br>{fmt(e['sig'])}"
    return h


def grafico_plotly():
    """Gráfico interactivo: al pasar el cursor (o tocar en tablet) se ve el detalle del hito."""
    P, ev = periodos(), ordenados()
    cnt, seen, pts = Counter(e["periodo"] for e in ev), Counter(), []
    for n, e in enumerate(ev, 1):
        k, i = cnt[e["periodo"]], seen[e["periodo"]]
        seen[e["periodo"]] += 1
        pts.append((n, P.index(e["periodo"]) + (0 if k == 1 else -0.28 + 0.56 * i / (k - 1)), e))
    fig = go.Figure()
    if len(pts) > 1:  # la línea solo indica secuencia, no causalidad
        fig.add_scatter(x=[p[1] for p in pts], y=[p[2]["val"] for p in pts], mode="lines", hoverinfo="skip",
                        line=dict(color="#9aa8b5", dash="dash", width=1.5), showlegend=False)
    for c in CATS:
        q = [p for p in pts if p[2]["cat"] == c]
        if q:
            fig.add_scatter(x=[p[1] for p in q], y=[p[2]["val"] for p in q], mode="markers+text", name=c,
                            text=[str(p[0]) for p in q], textfont=dict(color="white", size=12),
                            customdata=[_hover(p[0], p[2]) for p in q], hovertemplate="%{customdata}<extra></extra>",
                            marker=dict(symbol=SIMB[c], size=30, color="#1f4e79", line=dict(color="white", width=2)))
    fig.update_layout(
        height=480, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white", dragmode=False,
        hoverlabel=dict(bgcolor="white", font=dict(color="#1a1a1a", size=14), align="left"),
        legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center"),
        xaxis=dict(tickmode="array", tickvals=list(range(len(P))), ticktext=P, range=[-0.6, len(P) - 0.4],
                   title=f"Tiempo ({S.unidad.lower()})", showgrid=True, gridcolor="#e6ebf0", fixedrange=True),
        yaxis=dict(tickmode="array", tickvals=list(range(11)), range=[-0.6, 10.6], fixedrange=True,
                   ticktext=ETIQ_Y,
                   title="Valoración personal (0 a 10)", showgrid=True, gridcolor="#e6ebf0"))
    return fig


# ---------------- Exportaciones ----------------
def seguro(t):  # evita fórmulas al abrir en Excel
    return "'" + t if t[:1] in "=+-@" else t


def exportar_csv(codigo):
    out = io.StringIO()
    w = csv.writer(out, delimiter=";", quoting=csv.QUOTE_ALL)
    w.writerow(["Código local", "Tipo de registro", "Período", "Relato del estudiante (acontecimiento)",
                "Valoración del estudiante (0-10)", "Categoría", "Reflexión del estudiante (significado/aprendizaje)",
                "Pregunta de reflexión", "Respuesta de reflexión", "Aspectos para profundizar"])
    asp = aspectos()
    for n, e in enumerate(ordenados(), 1):
        pistas = " | ".join(f"{d}: {q}" for o, d, q in asp if o == f"Hito {n}")
        w.writerow([codigo, "Acontecimiento", e["periodo"], seguro(e["desc"]), e["val"], e["cat"],
                    seguro(e["sig"]), "", "", pistas])
    for i, q in enumerate(PREGUNTAS):
        r = S.refl.get(i, "").strip()
        if r:
            pistas = " | ".join(f"{d}: {p}" for o, d, p in asp if o == f"Reflexión {i + 1}")
            w.writerow([codigo, "Reflexión", "", "", "", "", "", q, seguro(r), pistas])
    return ("\ufeff" + out.getvalue()).encode("utf-8")  # BOM: tildes correctas en Excel


def exportar_json():
    return json.dumps({"version": 1, "unidad": S.unidad, "rangos": S.rangos, "eventos": S.eventos,
                       "reflexiones": {str(k): v for k, v in S.refl.items()}},
                      ensure_ascii=False, indent=2).encode("utf-8")


def exportar_pdf(codigo, con_fecha):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    ss = getSampleStyleSheet()
    P = lambda t, s="Normal": Paragraph(escape(str(t)).replace("\n", "<br/>"), ss[s])
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm,
                            bottomMargin=2 * cm, title="Mi línea de vida")
    st_ = [P("Mi línea de vida", "Title")]
    meta = ([f"Fecha: {date.today():%d-%m-%Y}"] if con_fecha else []) + ([f"Código local: {codigo}"] if codigo else [])
    if meta:
        st_.append(P("  ·  ".join(meta)))
    st_ += [Spacer(1, 8), Image(io.BytesIO(grafico_png()), width=17 * cm, height=17 * cm * 5.2 / 10), Spacer(1, 10),
            P("Relato, valoración y reflexión del estudiante", "Heading2")]
    rows = [[P(h, "Normal") for h in ["N.º", "Período", "Relato", "Val.", "Categoría", "Reflexión"]]]
    for n, e in enumerate(ordenados(), 1):
        rows.append([P(n), P(e["periodo"]), P(e["desc"]), P(e["val"]), P(e["cat"]), P(e["sig"] or "—")])
    t = Table(rows, colWidths=[1 * cm, 2.6 * cm, 5.2 * cm, 1.2 * cm, 2.6 * cm, 4.4 * cm], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce6f0")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    st_.append(t)
    resp = [(q, S.refl.get(i, "").strip()) for i, q in enumerate(PREGUNTAS) if S.refl.get(i, "").strip()]
    if resp:
        st_.append(P("Mis reflexiones", "Heading2"))
        for q, r in resp:
            st_ += [P(q, "Heading4"), P(r), Spacer(1, 4)]
    asp = aspectos()
    if asp:
        st_.append(P("Aspectos para profundizar con mi profesor/a u orientador/a", "Heading2"))
        st_.append(P("Son preguntas para conversar, no conclusiones ni diagnósticos."))
        for o, d, q in asp:
            st_.append(P(f"{o} · {d}: {q}"))
    st_ += [Spacer(1, 14), P(AVISO, "Italic")]
    doc.build(st_)
    return buf.getvalue()


# ---------------- Pasos ----------------
def paso_inicio():
    st.header("Mi línea de vida")
    st.write("Una **línea de vida** es un gráfico que te ayuda a mirar tu trayectoria: algunos momentos "
             "importantes de tu vida escolar y personal, cuándo ocurrieron y cómo los valoras hoy. "
             "Sirve para reflexionar sobre lo que has aprendido, lo que te interesa y lo que quieres explorar, "
             "y puede ser un insumo para conversar con tu profesor/a jefe u orientador/a.")
    st.info("**Tú decides qué incluir.** Comparte solo aquello que te sientas cómodo/a registrando. "
            "No escribas nombres de otras personas, direcciones, diagnósticos ni detalles íntimos. "
            "Puedes omitir preguntas y eliminar cualquier registro.")
    with st.expander("¿Quién verá mi información y para qué se usará? (texto que el establecimiento debe adaptar)"):
        st.write("Lo que escribas aquí no se envía a nadie automáticamente. Solo tú decides si descargas el archivo "
                 "y a quién se lo entregas. Tu profesor/a u orientador/a podrá revisar únicamente lo que tú "
                 "decidas compartir, para conversar contigo y apoyar tu perfil vocacional. "
                 "*[Establecimiento: indique aquí quién resguarda los archivos, por cuánto tiempo y bajo qué protocolo.]*")
    st.caption(AVISO)
    with st.expander("¿Ya tienes un archivo de respaldo (.json)? Cargarlo"):
        up = st.file_uploader("Archivo de respaldo", type="json")
        if up and st.button("Cargar mi trabajo"):
            try:
                d = json.load(up)
                ev = [{k: str(e[k]) if k != "val" else int(e[k]) for k in ("id", "periodo", "desc", "val", "cat", "sig")} for e in d["eventos"]]
                assert all(0 <= e["val"] <= 10 for e in ev) and d["unidad"] in MAESTRO
                S.eventos, S.unidad = ev, d["unidad"]
                S.rangos = {k: tuple(v) for k, v in d.get("rangos", {}).items() if k in MAESTRO and all(x in MAESTRO[k] for x in v)}
                S.refl = {int(k): str(v) for k, v in d.get("reflexiones", {}).items()}
                st.success("Trabajo cargado.")
            except Exception:
                st.error("No se pudo leer el archivo. Verifica que sea un respaldo descargado desde esta aplicación.")


def paso_periodos():
    st.header("1. ¿Qué período quieres mostrar?")
    S.unidad = st.radio("Unidad del eje horizontal", list(MAESTRO), index=list(MAESTRO).index(S.unidad), horizontal=True)
    m = MAESTRO[S.unidad]
    ini, fin = st.select_slider("Desde / hasta", options=m, value=S.rangos.get(S.unidad, RANGO0[S.unidad]))
    S.rangos[S.unidad] = (ini, fin)
    st.write("Tu línea irá de izquierda a derecha:", " → ".join(periodos()))
    st.caption("No necesitas fechas exactas: elige el curso, edad o año aproximado. Puedes cambiar esto más adelante.")


def paso_registro():
    st.header("2. Registra tus acontecimientos")
    st.caption("Ejemplo ficticio: «Participé en la feria científica del colegio» · 8.º básico · valoración 9.")
    P = periodos()
    ed = next((e for e in S.eventos if e["id"] == S.edit), None)
    with st.form(f"form_{S.fk}"):
        periodo = st.selectbox("¿Cuándo ocurrió? (aproximado)", P, index=P.index(ed["periodo"]) if ed and ed["periodo"] in P else 0)
        desc = st.text_area("Describe brevemente el acontecimiento", value=ed["desc"] if ed else "", max_chars=300)
        val = st.slider("¿Cómo valoras esta experiencia?", 0, 10, ed["val"] if ed else 5)
        st.caption("**0** = experiencia muy negativa · **5** = intermedia · **10** = muy positiva. "
                   "Es tu opinión personal; no es una nota ni una medición de ti.")
        cat = st.selectbox("Categoría (opcional)", CATS, index=CATS.index(ed["cat"]) if ed else 0)
        sig = st.text_area("¿Qué significó o qué aprendiste? (opcional, pero útil para tu perfil vocacional)",
                           value=ed["sig"] if ed else "", max_chars=500)
        c1, c2 = st.columns(2)
        ok = c1.form_submit_button("Guardar cambios" if ed else "Agregar acontecimiento", type="primary", width="stretch")
        cancel = c2.form_submit_button("Cancelar edición", width="stretch", disabled=ed is None)
    if cancel:
        S.edit, S.fk = None, S.fk + 1
        st.rerun()
    if ok:
        if not desc.strip():
            st.error("Escribe una descripción breve del acontecimiento.")
        else:
            nuevo = dict(id=ed["id"] if ed else uuid.uuid4().hex, periodo=periodo, desc=desc.strip(), val=int(val), cat=cat, sig=sig.strip())
            S.eventos = [nuevo if e["id"] == nuevo["id"] else e for e in S.eventos] if ed else S.eventos + [nuevo]
            S.edit, S.fk = None, S.fk + 1
            st.rerun()
    st.subheader(f"Mis acontecimientos ({len(S.eventos)})")
    for n, e in enumerate(ordenados(), 1):
        with st.container(border=True):
            st.markdown(f"**{n}. {e['periodo']}** · valoración **{e['val']}/10** · {e['cat']}")
            st.write(e["desc"])
            if e["sig"]:
                st.caption("Significado: " + e["sig"])
            a, b, _ = st.columns([1, 1, 2])
            if a.button("Editar", key=f"ed{e['id']}"):
                S.edit, S.fk = e["id"], S.fk + 1
                st.rerun()
            if b.button("Eliminar", key=f"del{e['id']}"):
                S.delid = e["id"]
                st.rerun()
            if S.delid == e["id"]:
                st.warning("¿Eliminar este acontecimiento? No se puede deshacer.")
                y, nn, _ = st.columns([1, 1, 2])
                if y.button("Sí, eliminar", key=f"y{e['id']}"):
                    S.eventos = [x for x in S.eventos if x["id"] != e["id"]]
                    S.delid = S.edit = None
                    st.rerun()
                if nn.button("No", key=f"n{e['id']}"):
                    S.delid = None
                    st.rerun()


def paso_linea():
    st.header("3. Mi línea de vida")
    if not S.eventos:
        st.info("Aún no has agregado acontecimientos. Vuelve al paso anterior para registrarlos.")
        return
    tab1, tab2 = st.tabs(["Gráfico", "Lista"])
    with tab1:
        st.plotly_chart(grafico_plotly(), width="stretch", config=PLOT_CFG)
        st.caption("Pasa el cursor (o toca en tablet) sobre un punto para ver el detalle. Cada número corresponde al acontecimiento de la lista. La línea punteada solo muestra el orden "
                   "de los hitos; no indica que uno cause al otro. " + AVISO)
    with tab2:
        for n, e in enumerate(ordenados(), 1):
            st.markdown(f"**{n}. {e['periodo']}** · valoración {e['val']}/10 · {e['cat']}  \n{e['desc']}")
            if e["sig"]:
                st.caption("Significado: " + e["sig"])


def paso_reflexion():
    st.header("4. Preguntas para reflexionar")
    st.caption("Todas son opcionales y puedes dejarlas en blanco. No hay respuestas correctas ni puntajes.")
    for i, q in enumerate(PREGUNTAS):
        S.refl[i] = st.text_area(f"{i + 1}. {q}", value=S.refl.get(i, ""), max_chars=800)


def paso_resumen():
    st.header("5. Resumen y descarga")
    if S.eventos:
        st.plotly_chart(grafico_plotly(), width="stretch", config=PLOT_CFG)
    else:
        st.info("Aún no hay acontecimientos registrados.")
    st.subheader("Aspectos para profundizar")
    st.caption("Son pistas para conversar con tu profesor/a u orientador/a, no conclusiones sobre ti, tus capacidades ni tu vocación.")
    for o, d, q in aspectos():
        st.markdown(f"- **{o} · {d}.** {q}")
    if not aspectos():
        st.write("Aparecerán cuando asignes categorías a tus hitos o respondas preguntas de reflexión.")
    st.divider()
    codigo = st.text_input("Código local (opcional; no uses tu nombre ni tu RUT)", max_chars=20)
    fecha = st.checkbox("Incluir fecha en el PDF", value=True)
    c1, c2, c3 = st.columns(3)
    c1.download_button("⬇ PDF para mí", exportar_pdf(codigo, fecha), "mi_linea_de_vida.pdf", "application/pdf", width="stretch")
    c2.download_button("⬇ CSV (Excel/LibreOffice)", exportar_csv(codigo), "linea_de_vida.csv", "text/csv", width="stretch")
    c3.download_button("⬇ Respaldo (.json)", exportar_json(), "respaldo_linea_de_vida.json", "application/json", width="stretch")
    st.caption("Los archivos se guardan en tu dispositivo y nadie los recibe automáticamente. Guarda el respaldo si quieres "
               "continuar después (cárgalo desde el Inicio). Para eliminarlos, bórralos de tu carpeta de descargas y usa el botón "
               "«Borrar mis datos» del menú lateral.")


# ---------------- Navegación ----------------
with st.sidebar:
    st.subheader("Pasos")
    for i, nombre in enumerate(PASOS):
        if st.button(("➤ " if i == S.step else "") + f"{i + 1}. {nombre}", key=f"nav{i}", width="stretch"):
            S.step = i
            st.rerun()
    st.divider()
    if st.button("🗑 Borrar mis datos y cerrar", width="stretch"):
        S.borrar = True
    if S.borrar:
        st.warning("Se eliminará todo lo registrado en esta sesión. Descarga antes lo que quieras conservar.")
        if st.button("Sí, borrar todo", type="primary", width="stretch"):
            S.clear()
            st.rerun()
        if st.button("Cancelar", width="stretch"):
            S.borrar = False
            st.rerun()

st.progress((S.step + 1) / len(PASOS), text=f"Paso {S.step + 1} de {len(PASOS)}: {PASOS[S.step]}")
[paso_inicio, paso_periodos, paso_registro, paso_linea, paso_reflexion, paso_resumen][S.step]()
a, b = st.columns(2)
if S.step > 0 and a.button("← Anterior", width="stretch"):
    S.step -= 1
    st.rerun()
if S.step < len(PASOS) - 1 and b.button("Siguiente →", type="primary", width="stretch"):
    S.step += 1
    st.rerun()
