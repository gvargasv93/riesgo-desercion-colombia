"""
Dashboard: Predicción del Riesgo de Deserción en la Educación Superior Colombiana
Trabajo Aplicado — Diplomado en Ciencia de Datos · SNIES 2023
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Riesgo de Deserción · Educación Superior Colombia",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] { background: #f0f4f8; }
    .kpi-card {
        background: #fff;
        border-radius: 10px;
        padding: 20px 16px;
        text-align: center;
        border-top: 4px solid #1565C0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #1565C0; }
    .kpi-label { font-size: 0.82rem; color: #555; margin-top: 4px; }
    .kpi-card-red  { border-top-color: #C62828; }
    .kpi-card-red  .kpi-value { color: #C62828; }
    .kpi-card-green { border-top-color: #2E7D32; }
    .kpi-card-green .kpi-value { color: #2E7D32; }
    .pred-alto {
        background: #FFEBEE; border: 2px solid #C62828;
        border-radius: 10px; padding: 20px; text-align: center;
    }
    .pred-bajo {
        background: #E8F5E9; border: 2px solid #2E7D32;
        border-radius: 10px; padding: 20px; text-align: center;
    }
    .pred-title { font-size: 1.6rem; font-weight: 700; }
    .pred-alto .pred-title { color: #C62828; }
    .pred-bajo .pred-title { color: #2E7D32; }
    .section-note {
        font-size: 0.82rem; color: #666;
        border-left: 3px solid #90CAF9;
        padding-left: 10px; margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ── Paleta de colores ────────────────────────────────────────────────────────
COLOR_ALTO   = "#C62828"
COLOR_BAJO   = "#2E7D32"
COLOR_AZUL   = "#1565C0"
SCALE_RIESGO = [[0.0, "#E8F5E9"], [0.5, "#FFF9C4"], [1.0, "#B71C1C"]]

COLS_CAT = [
    "SECTOR IES", "NIVEL DE FORMACIÓN", "NIVEL ACADÉMICO", "MODALIDAD",
    "ÁREA DE CONOCIMIENTO", "CARÁCTER IES", "IES ACREDITADA",
    "PROGRAMA ACREDITADO", "SEXO", "DEPARTAMENTO DE OFERTA DEL PROGRAMA",
]
COLS_NUM = ["MATRICULADOS", "MATRICULADOS PRIMER CURSO", "SEMESTRE"]

# ── Carga de datos ───────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    df = pd.read_csv("SNIES_dataset_con_predicciones.csv")
    return df

df = cargar_datos()

# Categorías válidas extraídas del propio dataset
OPCIONES = {
    col: sorted(df[col].dropna().unique().tolist())
    for col in COLS_CAT
}

# ── Navegación lateral ───────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/"
    "Escudo_de_Colombia.svg/120px-Escudo_de_Colombia.svg.png",
    width=60,
)
st.sidebar.title("🎓 Riesgo de Deserción")
st.sidebar.caption("SNIES 2023 · Bosque Aleatorio")
st.sidebar.markdown("---")

modulo = st.sidebar.radio(
    "Módulo",
    [
        "📊  Resumen General",
        "🗺️  Análisis Geográfico",
        "📈  Análisis por Variables",
        "📋  Tabla de Programas",
        "🔮  Predicción Individual",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Trabajo Aplicado · Diplomado en Ciencia de Datos\n\n"
    "Datos: MEN – SNIES 2023"
)

# ════════════════════════════════════════════════════════════════════════════
# MÓDULO 1: RESUMEN GENERAL
# ════════════════════════════════════════════════════════════════════════════
if modulo.startswith("📊"):
    st.title("📊 Resumen General")
    st.markdown(
        '<p class="section-note">Estadísticas descriptivas del dataset SNIES 2023 '
        "(60.796 registros · combinaciones programa-perfil-semestre)</p>",
        unsafe_allow_html=True,
    )

    total     = len(df)
    n_alto    = int((df["RIESGO_DESERCION"] == 1).sum())
    n_bajo    = int((df["RIESGO_DESERCION"] == 0).sum())
    pct_alto  = n_alto / total * 100
    n_dep     = df["DEPARTAMENTO DE OFERTA DEL PROGRAMA"].nunique()
    tasa_media = df["TASA_NO_GRADUACION"].mean() * 100

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-value">{total:,}</div>'
            '<div class="kpi-label">Registros en el dataset</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="kpi-card kpi-card-red"><div class="kpi-value">{pct_alto:.1f}%</div>'
            '<div class="kpi-label">Programas con riesgo alto</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="kpi-card kpi-card-green"><div class="kpi-value">{100-pct_alto:.1f}%</div>'
            '<div class="kpi-label">Programas con riesgo bajo</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-value">{n_dep}</div>'
            '<div class="kpi-label">Departamentos cubiertos</div></div>',
            unsafe_allow_html=True,
        )
    with c5:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-value">{tasa_media:.1f}%</div>'
            '<div class="kpi-label">Tasa media de no graduación</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Distribución de riesgo de deserción")
        fig_pie = go.Figure(go.Pie(
            labels=["Riesgo ALTO", "Riesgo BAJO"],
            values=[n_alto, n_bajo],
            marker_colors=[COLOR_ALTO, COLOR_BAJO],
            hole=0.45,
            textinfo="percent+label",
            textfont_size=14,
        ))
        fig_pie.update_layout(
            showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=340
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.subheader("Riesgo alto por modalidad")
        mod_df = (
            df.groupby("MODALIDAD")["RIESGO_DESERCION"]
            .agg(["sum", "count"])
            .reset_index()
        )
        mod_df["pct"] = mod_df["sum"] / mod_df["count"] * 100
        mod_df = mod_df.sort_values("pct", ascending=True)
        fig_mod = px.bar(
            mod_df,
            x="pct", y="MODALIDAD",
            orientation="h",
            color="pct",
            color_continuous_scale=SCALE_RIESGO,
            range_color=[70, 100],
            labels={"pct": "% Riesgo Alto", "MODALIDAD": ""},
            text=mod_df["pct"].apply(lambda v: f"{v:.1f}%"),
        )
        fig_mod.update_traces(textposition="outside")
        fig_mod.update_coloraxes(showscale=False)
        fig_mod.update_layout(margin=dict(t=20, b=20, l=10, r=60), height=340)
        st.plotly_chart(fig_mod, use_container_width=True)

    st.subheader("Riesgo alto por nivel de formación")
    niv_df = (
        df.groupby("NIVEL DE FORMACIÓN")["RIESGO_DESERCION"]
        .agg(["sum", "count"])
        .reset_index()
    )
    niv_df["pct"] = niv_df["sum"] / niv_df["count"] * 100
    niv_df = niv_df.sort_values("pct", ascending=False)
    fig_niv = px.bar(
        niv_df,
        x="NIVEL DE FORMACIÓN", y="pct",
        color="pct",
        color_continuous_scale=SCALE_RIESGO,
        range_color=[70, 100],
        labels={"pct": "% Riesgo Alto", "NIVEL DE FORMACIÓN": ""},
        text=niv_df["pct"].apply(lambda v: f"{v:.1f}%"),
    )
    fig_niv.update_traces(textposition="outside")
    fig_niv.update_coloraxes(showscale=False)
    fig_niv.update_layout(margin=dict(t=20, b=80), height=380, xaxis_tickangle=-35)
    st.plotly_chart(fig_niv, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# MÓDULO 2: ANÁLISIS GEOGRÁFICO
# ════════════════════════════════════════════════════════════════════════════
elif modulo.startswith("🗺️"):
    st.title("🗺️ Análisis Geográfico")
    st.markdown(
        '<p class="section-note">Porcentaje de combinaciones programa-perfil-semestre '
        "clasificadas como riesgo alto por departamento (SNIES 2023).</p>",
        unsafe_allow_html=True,
    )

    dep_df = (
        df.groupby("DEPARTAMENTO DE OFERTA DEL PROGRAMA")["RIESGO_DESERCION"]
        .agg(total="count", alto="sum")
        .reset_index()
    )
    dep_df["pct_alto"] = dep_df["alto"] / dep_df["total"] * 100
    dep_df = dep_df.sort_values("pct_alto", ascending=True)
    dep_df.columns = ["Departamento", "Total registros", "Riesgo alto", "% Riesgo Alto"]

    fig_dep = px.bar(
        dep_df,
        x="% Riesgo Alto",
        y="Departamento",
        orientation="h",
        color="% Riesgo Alto",
        color_continuous_scale=SCALE_RIESGO,
        range_color=[75, 100],
        text=dep_df["% Riesgo Alto"].apply(lambda v: f"{v:.1f}%"),
        hover_data={"Total registros": True, "Riesgo alto": True},
        labels={"% Riesgo Alto": "% Riesgo Alto"},
    )
    fig_dep.update_traces(textposition="outside")
    fig_dep.update_coloraxes(colorbar_title="% Riesgo")
    fig_dep.update_layout(
        height=820,
        margin=dict(t=20, b=20, l=10, r=80),
        yaxis_title="",
        xaxis=dict(range=[0, 108]),
    )
    st.plotly_chart(fig_dep, use_container_width=True)

    st.markdown("---")
    st.subheader("Detalle por departamento")
    st.dataframe(
        dep_df.sort_values("% Riesgo Alto", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=400,
    )


# ════════════════════════════════════════════════════════════════════════════
# MÓDULO 3: ANÁLISIS POR VARIABLES
# ════════════════════════════════════════════════════════════════════════════
elif modulo.startswith("📈"):
    st.title("📈 Análisis por Variables")
    st.markdown(
        '<p class="section-note">Importancia de cada variable categórica en la '
        "distribución del riesgo de deserción.</p>",
        unsafe_allow_html=True,
    )

    variable = st.selectbox(
        "Selecciona la variable a analizar:",
        [
            "MODALIDAD",
            "NIVEL DE FORMACIÓN",
            "ÁREA DE CONOCIMIENTO",
            "SECTOR IES",
            "CARÁCTER IES",
            "NIVEL ACADÉMICO",
            "IES ACREDITADA",
            "PROGRAMA ACREDITADO",
            "SEXO",
            "DEPARTAMENTO DE OFERTA DEL PROGRAMA",
        ],
    )

    var_df = (
        df.groupby(variable)["RIESGO_DESERCION"]
        .agg(total="count", alto="sum")
        .reset_index()
    )
    var_df["pct_alto"] = var_df["alto"] / var_df["total"] * 100
    var_df["pct_bajo"]  = 100 - var_df["pct_alto"]
    var_df = var_df.sort_values("pct_alto", ascending=False)

    col_chart, col_stats = st.columns([2, 1])

    with col_chart:
        fig_stack = go.Figure()
        fig_stack.add_trace(go.Bar(
            name="Riesgo ALTO",
            y=var_df[variable],
            x=var_df["pct_alto"],
            orientation="h",
            marker_color=COLOR_ALTO,
            text=var_df["pct_alto"].apply(lambda v: f"{v:.1f}%"),
            textposition="inside",
            insidetextanchor="middle",
        ))
        fig_stack.add_trace(go.Bar(
            name="Riesgo BAJO",
            y=var_df[variable],
            x=var_df["pct_bajo"],
            orientation="h",
            marker_color=COLOR_BAJO,
            text=var_df["pct_bajo"].apply(lambda v: f"{v:.1f}%"),
            textposition="inside",
            insidetextanchor="middle",
        ))
        fig_stack.update_layout(
            barmode="stack",
            height=max(380, len(var_df) * 42),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(t=40, b=20, l=10, r=20),
            xaxis=dict(title="% de registros", range=[0, 100]),
            yaxis_title="",
        )
        st.plotly_chart(fig_stack, use_container_width=True)

    with col_stats:
        st.subheader("Resumen")
        tabla = var_df[[variable, "total", "pct_alto"]].copy()
        tabla.columns = ["Categoría", "Registros", "% Riesgo Alto"]
        tabla["% Riesgo Alto"] = tabla["% Riesgo Alto"].round(1)
        st.dataframe(
            tabla.reset_index(drop=True),
            use_container_width=True,
            height=max(300, len(var_df) * 38 + 40),
        )

        prom = var_df["pct_alto"].mean()
        mx   = var_df.iloc[0]
        mn   = var_df.iloc[-1]
        st.metric("Promedio riesgo alto", f"{prom:.1f}%")
        st.metric("Categoría más crítica", mx[variable], f"{mx['pct_alto']:.1f}%")
        st.metric("Categoría menos crítica", mn[variable], f"{mn['pct_alto']:.1f}%")


# ════════════════════════════════════════════════════════════════════════════
# MÓDULO 4: TABLA DE PROGRAMAS
# ════════════════════════════════════════════════════════════════════════════
elif modulo.startswith("📋"):
    st.title("📋 Tabla de Programas por Riesgo")
    st.markdown(
        '<p class="section-note">Explora los registros del dataset filtrados por '
        "riesgo, departamento y modalidad.</p>",
        unsafe_allow_html=True,
    )

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        filtro_riesgo = st.selectbox(
            "Riesgo de deserción",
            ["Todos", "Alto (1)", "Bajo (0)"],
        )
    with col_f2:
        deps_disp = ["Todos"] + sorted(df["DEPARTAMENTO DE OFERTA DEL PROGRAMA"].unique())
        filtro_dep = st.selectbox("Departamento", deps_disp)
    with col_f3:
        mods_disp = ["Todas"] + sorted(df["MODALIDAD"].unique())
        filtro_mod = st.selectbox("Modalidad", mods_disp)
    with col_f4:
        nivs_disp = ["Todos"] + sorted(df["NIVEL DE FORMACIÓN"].unique())
        filtro_niv = st.selectbox("Nivel de formación", nivs_disp)

    df_fil = df.copy()
    if filtro_riesgo == "Alto (1)":
        df_fil = df_fil[df_fil["RIESGO_DESERCION"] == 1]
    elif filtro_riesgo == "Bajo (0)":
        df_fil = df_fil[df_fil["RIESGO_DESERCION"] == 0]
    if filtro_dep != "Todos":
        df_fil = df_fil[df_fil["DEPARTAMENTO DE OFERTA DEL PROGRAMA"] == filtro_dep]
    if filtro_mod != "Todas":
        df_fil = df_fil[df_fil["MODALIDAD"] == filtro_mod]
    if filtro_niv != "Todos":
        df_fil = df_fil[df_fil["NIVEL DE FORMACIÓN"] == filtro_niv]

    n_fil = len(df_fil)
    pct_fil = (df_fil["RIESGO_DESERCION"] == 1).mean() * 100 if n_fil > 0 else 0

    m1, m2 = st.columns(2)
    m1.metric("Registros filtrados", f"{n_fil:,}")
    m2.metric("% Riesgo alto en selección", f"{pct_fil:.1f}%")

    cols_mostrar = [
        "DEPARTAMENTO DE OFERTA DEL PROGRAMA", "MODALIDAD",
        "NIVEL DE FORMACIÓN", "ÁREA DE CONOCIMIENTO",
        "SECTOR IES", "IES ACREDITADA", "PROGRAMA ACREDITADO",
        "MATRICULADOS", "TASA_NO_GRADUACION", "RIESGO_DESERCION", "PROB_RIESGO_ALTO",
    ]
    df_show = df_fil[cols_mostrar].copy()
    df_show["TASA_NO_GRADUACION"] = (df_show["TASA_NO_GRADUACION"] * 100).round(1)
    df_show = df_show.rename(columns={
        "DEPARTAMENTO DE OFERTA DEL PROGRAMA": "Departamento",
        "NIVEL DE FORMACIÓN": "Nivel",
        "ÁREA DE CONOCIMIENTO": "Área",
        "SECTOR IES": "Sector",
        "IES ACREDITADA": "Acred. IES",
        "PROGRAMA ACREDITADO": "Acred. Prog.",
        "TASA_NO_GRADUACION": "Tasa No Grad. (%)",
        "RIESGO_DESERCION": "Riesgo",
        "PROB_RIESGO_ALTO": "Prob. Riesgo Alto (%)",
    })

    st.dataframe(
        df_show.reset_index(drop=True),
        use_container_width=True,
        height=520,
    )

    csv = df_fil.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Descargar selección en CSV",
        data=csv,
        file_name="programas_filtrados.csv",
        mime="text/csv",
    )


# ════════════════════════════════════════════════════════════════════════════
# MÓDULO 5: PREDICCIÓN INDIVIDUAL
# ════════════════════════════════════════════════════════════════════════════
elif modulo.startswith("🔮"):
    st.title("🔮 Predicción Individual")
    st.markdown(
        '<p class="section-note">Selecciona el perfil de un programa para consultar '
        "la probabilidad de riesgo estimada por el modelo de Bosque Aleatorio "
        "(predicciones pre-calculadas sobre el dataset SNIES 2023).</p>",
        unsafe_allow_html=True,
    )

    with st.form("form_prediccion"):
        st.subheader("Variables categóricas")
        c1, c2 = st.columns(2)

        with c1:
            sector        = st.selectbox("Sector IES",            OPCIONES["SECTOR IES"])
            nivel_form    = st.selectbox("Nivel de formación",     OPCIONES["NIVEL DE FORMACIÓN"])
            nivel_acad    = st.selectbox("Nivel académico",        OPCIONES["NIVEL ACADÉMICO"])
            modalidad     = st.selectbox("Modalidad",              OPCIONES["MODALIDAD"])
            area          = st.selectbox("Área de conocimiento",   OPCIONES["ÁREA DE CONOCIMIENTO"])

        with c2:
            caracter      = st.selectbox("Carácter IES",           OPCIONES["CARÁCTER IES"])
            ies_acred     = st.selectbox("IES acreditada",         OPCIONES["IES ACREDITADA"])
            prog_acred    = st.selectbox("Programa acreditado",    OPCIONES["PROGRAMA ACREDITADO"])
            sexo          = st.selectbox("Sexo",                   OPCIONES["SEXO"])
            departamento  = st.selectbox("Departamento de oferta", OPCIONES["DEPARTAMENTO DE OFERTA DEL PROGRAMA"])

        st.subheader("Variables numéricas")
        cn1, cn2, cn3 = st.columns(3)
        with cn1:
            matriculados = st.number_input(
                "Matriculados en el programa", min_value=1, max_value=35000,
                value=50, step=1
            )
        with cn2:
            primer_curso = st.number_input(
                "Matriculados en primer curso", min_value=0, max_value=12000,
                value=10, step=1
            )
        with cn3:
            semestre = st.selectbox("Semestre", [1, 2])

        submitted = st.form_submit_button("🔍 Consultar riesgo", use_container_width=True)

    if submitted:
        # Buscar registros similares en el dataset (coincidencia exacta en variables categóricas)
        filtros = {
            "SECTOR IES": sector,
            "NIVEL DE FORMACIÓN": nivel_form,
            "NIVEL ACADÉMICO": nivel_acad,
            "MODALIDAD": modalidad,
            "ÁREA DE CONOCIMIENTO": area,
            "CARÁCTER IES": caracter,
            "IES ACREDITADA": ies_acred,
            "PROGRAMA ACREDITADO": prog_acred,
            "SEXO": sexo,
            "DEPARTAMENTO DE OFERTA DEL PROGRAMA": departamento,
        }

        mask = pd.Series([True] * len(df), index=df.index)
        for col, val in filtros.items():
            mask = mask & (df[col] == val)

        df_similar = df[mask]

        # Si no hay coincidencia exacta, relajar a las 7 variables más importantes
        if len(df_similar) == 0:
            cols_principales = [
                "SECTOR IES", "NIVEL DE FORMACIÓN", "MODALIDAD",
                "ÁREA DE CONOCIMIENTO", "DEPARTAMENTO DE OFERTA DEL PROGRAMA",
                "CARÁCTER IES", "NIVEL ACADÉMICO",
            ]
            mask2 = pd.Series([True] * len(df), index=df.index)
            for col in cols_principales:
                mask2 = mask2 & (df[col] == filtros[col])
            df_similar = df[mask2]
            nivel_coincidencia = "aproximada (7 variables principales)"
        else:
            nivel_coincidencia = "exacta (10 variables)"

        st.markdown("<br>", unsafe_allow_html=True)

        if len(df_similar) == 0:
            st.warning(
                "No se encontraron registros similares en el dataset para esta combinación. "
                "Prueba con otra combinación de variables."
            )
        else:
            n_similar   = len(df_similar)
            prob_alto   = df_similar["PROB_RIESGO_ALTO"].mean()
            prob_bajo   = 100 - prob_alto
            pred_clase  = 1 if prob_alto >= 50 else 0

            if pred_clase == 1:
                st.markdown(
                    f'<div class="pred-alto">'
                    f'<div class="pred-title">⚠️ RIESGO ALTO DE DESERCIÓN</div>'
                    f'<div style="font-size:1.1rem;margin-top:8px;">'
                    f'Probabilidad estimada: <b>{prob_alto:.1f}%</b></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="pred-bajo">'
                    f'<div class="pred-title">✅ RIESGO BAJO DE DESERCIÓN</div>'
                    f'<div style="font-size:1.1rem;margin-top:8px;">'
                    f'Probabilidad estimada de riesgo bajo: <b>{prob_bajo:.1f}%</b></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            fig_proba = go.Figure(go.Bar(
                x=["Riesgo BAJO", "Riesgo ALTO"],
                y=[prob_bajo, prob_alto],
                marker_color=[COLOR_BAJO, COLOR_ALTO],
                text=[f"{prob_bajo:.1f}%", f"{prob_alto:.1f}%"],
                textposition="outside",
                width=0.4,
            ))
            fig_proba.update_layout(
                title="Probabilidades estimadas por clase",
                yaxis=dict(title="Probabilidad (%)", range=[0, 115]),
                height=320,
                margin=dict(t=50, b=20),
                showlegend=False,
            )
            st.plotly_chart(fig_proba, use_container_width=True)

            st.info(
                f"ℹ️ Resultado basado en **{n_similar:,} registros similares** del dataset SNIES 2023 "
                f"(coincidencia {nivel_coincidencia}). "
                "El modelo de Bosque Aleatorio fue entrenado sobre datos agregados a nivel de "
                "programa-perfil-semestre, no sobre datos individuales de estudiantes.",
                icon=None,
            )
