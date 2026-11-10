import pandas as pd
import plotly.express as px
import streamlit as st

st.header("📈 Visualización de tu Línea de Vida")
st.caption(
    "Gráfico cronológico que muestra la secuencia de tus acontecimientos "
    "y la valoración subjetiva asignada (de 0 a 10)."
)

# Verificar si existen hitos registrados en la sesión
milestones = st.session_state.get("milestones", [])

if not milestones:
    st.warning(
        "⚠️ No hay acontecimientos registrados todavía. Por favor, ve a la "
        "sección de **Registro de Acontecimientos** para agregar hitos."
    )
else:
    df_milestones = pd.DataFrame(milestones)

    # ---------------------------------------------------------
    # Filtro interactivo por categoría
    # ---------------------------------------------------------
    categories = ["Todas las categorías"] + list(
        df_milestones["category"].unique()
    )
    selected_category = st.selectbox(
        label="Filtrar acontecimientos por categoría:",
        options=categories,
    )

    if selected_category != "Todas las categorías":
        df_filtered = df_milestones[
            df_milestones["category"] == selected_category
        ].copy()
    else:
        df_filtered = df_milestones.copy()

    if df_filtered.empty:
        st.info(
            "No hay acontecimientos registrados para la categoría seleccionada."
        )
    else:
        # Preparamos el significado por defecto si está vacío
        df_filtered["clean_meaning"] = df_filtered["meaning"].apply(
            lambda x: x if x else "Sin registro de significado"
        )

        # Gráfico de dispersión utilizando customdata para alimentar el tooltip nativo
        fig = px.scatter(
            df_filtered,
            x="period",
            y="valuation",
            color="category",
            custom_data=["description", "period", "clean_meaning"],
            labels={
                "period": "Período / Trayectoria Escolar",
                "valuation": "Valoración Subjetiva (0 a 10)",
                "category": "Categoría",
            },
            title="Secuencia de Acontecimientos y Valoración Subjetiva",
        )

        # Configuración nativa del tooltip limpio, ordenado y sin texto fijo en pantalla
        fig.update_traces(
            marker=dict(size=15, symbol="circle"),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "%{customdata[1]}<br>"
                "<i>%{customdata[2]}</i><br>"
                "<b>Valoración:</b> %{y} / 10"
                "<extra></extra>"
            ),
        )

        # Diseño general del gráfico y alineación izquierda nativa del tooltip
        fig.update_layout(
            yaxis=dict(range=[-0.5, 10.5], dtick=1),
            xaxis_title="Período o Etapa",
            yaxis_title="Valoración Subjetiva (0 - 10)",
            legend_title="Categorías de Hitos",
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="sans-serif",
                align="left",  # Alinea el texto a la izquierda de forma nativa
            ),
        )

        # Mostrar el gráfico interactivo en Streamlit
        st.plotly_chart(fig, width="stretch", theme="streamlit")

        st.info(
            "💡 **¿Cómo leer tu gráfico?:** Cada punto representa un acontecimiento "
            "en tu trayectoria. Pasa el cursor sobre ellos para ver los detalles "
            "ordenados."
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
                width="stretch",
            )