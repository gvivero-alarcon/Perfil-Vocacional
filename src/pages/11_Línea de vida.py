import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.header("📈 Visualización de tu Línea de Vida")
st.caption(
    "Gráfico cronológico que muestra la secuencia de tus acontecimientos "
    "mediante tarjetas ubicadas en sus coordenadas exactas."
)

milestones = st.session_state.get("milestones", [])

if not milestones:
    st.warning(
        "⚠️ No hay acontecimientos registrados todavía. Por favor, ve a la "
        "sección de **Registro de Acontecimientos** para agregar hitos."
    )
else:
    df_milestones = pd.DataFrame(milestones)

    # Orden cronológico estándar para los períodos escolares
    period_order = [
        "Pre-kínder", "Kínder", "1° Básico", "2° Básico", "3° Básico", 
        "4° Básico", "5° Básico", "6° Básico", "7° Básico", "8° Básico", 
        "1° Medio", "2° Medio", "3° Medio", "4° Medio"
    ]

    active_periods = [p for p in period_order if p in df_milestones["period"].unique()]
    for p in df_milestones["period"].unique():
        if p not in active_periods:
            active_periods.append(p)

    # Filtro interactivo por categoría
    categories = ["Todas las categorías"] + list(df_milestones["category"].unique())
    selected_category = st.selectbox(
        label="Filtrar acontecimientos en el gráfico por categoría:",
        options=categories,
    )

    if selected_category != "Todas las categorías":
        df_filtered = df_milestones[df_milestones["category"] == selected_category].copy()
    else:
        df_filtered = df_milestones.copy()

    if df_filtered.empty:
        st.info("No hay acontecimientos registrados para la categoría seleccionada.")
    else:
        # Paleta de colores pastel para los fondos de las tarjetas
        category_colors = {
            "Escolar/Académica": "#e3f2fd",
            "Intereses/Actividades": "#e8f5e9",
            "Familiar/Social": "#fff3e0",
            "Personal": "#f3e5f5",
            "Comunitaria / Otra": "#fbe9e7",
        }

        border_colors = {
            "Escolar/Académica": "#1976d2",
            "Intereses/Actividades": "#388e3c",
            "Familiar/Social": "#f57c00",
            "Personal": "#7b1fa2",
            "Comunitaria / Otra": "#d84315",
        }

        fig = go.Figure()

        # 1. Trazas para la Leyenda Superior en formato horizontal y centrada
        unique_cats_in_view = df_filtered["category"].unique()
        for cat in unique_cats_in_view:
            fig.add_trace(
                go.Scatter(
                    x=[None],
                    y=[None],
                    mode="markers",
                    marker=dict(
                        size=12,
                        symbol="square",
                        color=border_colors.get(cat, "#6c757d"),
                    ),
                    name=cat,
                    showlegend=True,
                    hoverinfo="skip",
                )
            )

        # Control básico de posiciones para evitar superposiciones exactas
        coord_tracker = {}

        for _, row in df_filtered.iterrows():
            x_val = row["period"]
            y_val = row["valuation"]

            key = (x_val, y_val)
            if key not in coord_tracker:
                coord_tracker[key] = 0
            else:
                coord_tracker[key] += 1
                y_val = min(10.0, max(0.0, y_val + (coord_tracker[key] * 0.7)))

            cat = row["category"]
            bg_color = category_colors.get(cat, "#f8f9fa")
            border_color = border_colors.get(cat, "#6c757d")

            description_text = row["description"]
            meaning_text = (
                row["meaning"].strip()
                if (row.get("meaning") and str(row["meaning"]).strip())
                else "Sin registro de reflexión"
            )

            # 2. Traza invisible para activar el Hover limpio (solo Hito y Reflexión sin etiquetas)
            fig.add_trace(
                go.Scatter(
                    x=[x_val],
                    y=[y_val],
                    mode="markers",
                    marker=dict(size=30, color="rgba(0,0,0,0)"),
                    customdata=[[description_text, meaning_text]],
                    hovertemplate=(
                        "<b>%{customdata[0]}</b><br>"
                        "<i>%{customdata[1]}</i>"
                        "<extra></extra>"
                    ),
                    showlegend=False,
                )
            )

            # 3. Tarjeta de texto fija en la coordenada exacta con ancho acotado
            fig.add_annotation(
                x=x_val,
                y=y_val,
                text=f"<b>{description_text}</b>",
                width=170,             # Ancho controlado para evitar cortes horizontales
                align="left",
                showarrow=False,
                bgcolor=bg_color,
                bordercolor=border_color,
                borderwidth=1.5,
                borderpad=6,
            )

        # 4. Diseño general: Título centrado, leyenda superior centrada, eje Y estricto de 0 a 10
        fig.update_layout(
            title=dict(
                text="Línea de vida",
                y=0.96,
                x=0.5,
                xanchor="center",
                yanchor="top",
                font=dict(size=20)
            ),
            xaxis=dict(
                type="category",
                categoryorder="array",
                categoryarray=active_periods,
                title="Período o Etapa Escolar",
            ),
            yaxis=dict(
                range=[-0.5, 10.5],
                dtick=1,
                title="Valoración Subjetiva (0 - 10)",
                zeroline=True,
            ),
            template="plotly_white",
            height=720,
            margin=dict(t=120, b=50, l=60, r=40),
            legend=dict(
                title="",
                orientation="h",
                yanchor="bottom",
                y=1.07,  # Ubicada arriba pero separada del título y herramientas
                xanchor="center",
                x=0.5,   # Centrada horizontalmente
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="sans-serif",
                align="left",
            ),
        )

        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

        st.info(
            "💡 **Interpretación:** Cada tarjeta muestra el acontecimiento en su coordenada exacta. "
            "Pasa el cursor sobre ella para leer la reflexión asociada."
        )

        with st.expander("🔍 Ver detalle tabular de los puntos graficados"):
            st.dataframe(
                df_filtered[
                    [
                        "period",
                        "category",
                        "description",
                        "valuation",
                        "meaning",
                    ]
                ],
                use_container_width=True,
            )