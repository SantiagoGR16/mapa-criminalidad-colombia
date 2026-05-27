"""
🗺️ Mapa de Criminalidad Municipal — Colombia
Dashboard interactivo con Streamlit.
"""

import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
from sodapy import Socrata

# ── Configuración de página ────────────────────────────
st.set_page_config(
    page_title="Mapa de Criminalidad — Colombia",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos CSS ────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
    }

    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 20px 24px;
        color: white;
        text-align: center;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 4px 0;
    }

    .kpi-label {
        font-size: 0.85rem;
        opacity: 0.75;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .kpi-delta {
        font-size: 0.9rem;
        margin-top: 4px;
    }

    .kpi-delta.up { color: #ff6b6b; }
    .kpi-delta.down { color: #51cf66; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%);
    }

    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Funciones de carga de datos ────────────────────────
@st.cache_data(ttl=3600, show_spinner="Descargando datos de criminalidad...")
def cargar_delitos():
    """Descarga todos los datasets de delitos desde datos.gov.co."""
    client = Socrata("www.datos.gov.co", None)

    datasets = {
        "Homicidio": ("m8fd-ahd9", "cod_muni"),
        "Hurto a personas": ("4rxi-8m8d", "cod_muni"),
        "Delitos sexuales": ("fpe5-yrmw", "codigo_dane"),
    }

    frames = []
    for tipo, (dataset_id, col_codigo) in datasets.items():
        all_results = []
        offset = 0
        while True:
            r = client.get(dataset_id, limit=50000, offset=offset)
            if not r:
                break
            all_results.extend(r)
            offset += 50000
        df = pd.DataFrame.from_records(all_results)

        # Limpiar
        df["fecha_hecho"] = pd.to_datetime(df["fecha_hecho"], errors="coerce")
        df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0).astype(int)
        df[col_codigo] = df[col_codigo].astype(str).str.replace(".0", "", regex=False)
        if df[col_codigo].str.len().max() > 5:
            df[col_codigo] = df[col_codigo].str[:5]
        df[col_codigo] = df[col_codigo].str.zfill(5)
        df["anio"] = df["fecha_hecho"].dt.year
        df["tipo_delito"] = tipo
        df = df[df["anio"] >= 2020]

        frames.append(df[[col_codigo, "anio", "cantidad", "tipo_delito"]].rename(columns={col_codigo: "cod_muni"}))

    return pd.concat(frames, ignore_index=True)


@st.cache_data(ttl=3600, show_spinner="Descargando datos de población...")
def cargar_poblacion():
    """Descarga proyecciones de población municipal del DANE."""
    pop_url = "https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/DCD-area-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx"
    df_raw = pd.read_excel(pop_url, header=11)
    df_raw.columns = ["cod_depto", "departamento", "cod_muni", "municipio", "anio", "area", "poblacion"]

    fila_perdida = pd.DataFrame([{
        "cod_depto": "05", "departamento": "Antioquia", "cod_muni": "05001",
        "municipio": "Medellín", "anio": 2020, "area": "Total", "poblacion": 2519592
    }])
    df_raw = pd.concat([fila_perdida, df_raw], ignore_index=True)

    df = df_raw[df_raw["area"] == "Total"].copy()
    df["anio"] = df["anio"].astype(int)
    df["poblacion"] = df["poblacion"].astype(int)
    df["cod_muni"] = df["cod_muni"].astype(str).str.split(".").str[0].str.zfill(5)

    return df


@st.cache_data(ttl=86400, show_spinner="Descargando geometrías municipales...")
def cargar_geojson():
    """Descarga el GeoJSON de municipios de Colombia."""
    gdf = gpd.read_file(
        "https://raw.githubusercontent.com/caticoa3/colombia_mapa/master/co_2018_MGN_MPIO_POLITICO.geojson"
    )
    gdf["geometry"] = gdf["geometry"].simplify(0.005)
    return gdf


def calcular_tasas(df_delitos, df_pop):
    """Calcula tasas per cápita por municipio, año y tipo de delito."""
    agrupado = (
        df_delitos.groupby(["anio", "cod_muni", "tipo_delito"])["cantidad"]
        .sum()
        .reset_index()
    )
    agrupado = agrupado.merge(
        df_pop[["cod_muni", "anio", "poblacion", "municipio", "departamento"]],
        on=["cod_muni", "anio"],
        how="left",
    )
    agrupado["tasa"] = (agrupado["cantidad"] / agrupado["poblacion"]) * 100_000
    agrupado = agrupado.dropna(subset=["tasa"])
    return agrupado


# ── Cargar datos ───────────────────────────────────────
df_delitos = cargar_delitos()
df_pop = cargar_poblacion()
gdf_muni = cargar_geojson()
agrupado = calcular_tasas(df_delitos, df_pop)

anios_disponibles = sorted(agrupado["anio"].unique())
delitos_disponibles = sorted(agrupado["tipo_delito"].unique())


# ── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗺️ Filtros")
    st.markdown("---")

    delito_sel = st.selectbox(
        "Tipo de delito",
        delitos_disponibles,
        index=delitos_disponibles.index("Homicidio") if "Homicidio" in delitos_disponibles else 0,
    )

    anio_sel = st.select_slider(
        "Año",
        options=[int(a) for a in anios_disponibles],
        value=int(anios_disponibles[-2]),
    )

    deptos = sorted(agrupado["departamento"].dropna().unique())
    depto_sel = st.multiselect(
        "Departamento (todos si vacío)",
        deptos,
    )

    st.markdown("---")
    st.markdown(
        "**Fuentes:** Policía Nacional (SIEDCO), DANE"
    )
    st.markdown(
        "**Métrica:** Tasa por cada 100,000 hab."
    )


# ── Filtrar datos ──────────────────────────────────────
datos_filtrados = agrupado[
    (agrupado["anio"] == anio_sel) & (agrupado["tipo_delito"] == delito_sel)
].copy()

if depto_sel:
    datos_filtrados = datos_filtrados[datos_filtrados["departamento"].isin(depto_sel)]

# Datos del año anterior para variación
datos_anterior = agrupado[
    (agrupado["anio"] == anio_sel - 1) & (agrupado["tipo_delito"] == delito_sel)
].copy()


# ── KPIs ───────────────────────────────────────────────
st.markdown(f"# 🗺️ Mapa de Criminalidad Municipal — Colombia {anio_sel}")

total_casos = int(datos_filtrados["cantidad"].sum())
tasa_promedio = datos_filtrados["tasa"].mean()
muni_max = datos_filtrados.loc[datos_filtrados["tasa"].idxmax()] if len(datos_filtrados) > 0 else None
muni_min = datos_filtrados[datos_filtrados["tasa"] > 0]
muni_min = muni_min.loc[muni_min["tasa"].idxmin()] if len(muni_min) > 0 else None

# Variación
total_anterior = int(datos_anterior["cantidad"].sum()) if len(datos_anterior) > 0 else 0
variacion = ((total_casos - total_anterior) / total_anterior * 100) if total_anterior > 0 else 0
delta_class = "up" if variacion > 0 else "down"
delta_icon = "▲" if variacion > 0 else "▼"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total casos</div>
        <div class="kpi-value">{total_casos:,}</div>
        <div class="kpi-delta {delta_class}">{delta_icon} {abs(variacion):.1f}% vs {anio_sel - 1}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Tasa promedio</div>
        <div class="kpi-value">{tasa_promedio:.1f}</div>
        <div class="kpi-label" style="margin-top: 4px;">por 100K hab.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if muni_max is not None:
        st.markdown(f"""
        <div class="kpi-card" style="background: linear-gradient(135deg, #5c1a1a 0%, #8b2525 100%);">
            <div class="kpi-label">Municipio más afectado</div>
            <div class="kpi-value" style="font-size: 1.3rem;">{muni_max['municipio']}</div>
            <div class="kpi-delta">Tasa: {muni_max['tasa']:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

with col4:
    if muni_min is not None:
        st.markdown(f"""
        <div class="kpi-card" style="background: linear-gradient(135deg, #1a4a2e 0%, #1e6e3e 100%);">
            <div class="kpi-label">Municipio más seguro</div>
            <div class="kpi-value" style="font-size: 1.3rem;">{muni_min['municipio']}</div>
            <div class="kpi-delta">Tasa: {muni_min['tasa']:.1f}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# ── Mapa y Ranking ─────────────────────────────────────
col_mapa, col_ranking = st.columns([3, 1])

with col_mapa:
    mapa_df = gdf_muni.merge(
        datos_filtrados,
        left_on="MPIO_CCNCT",
        right_on="cod_muni",
        how="left",
    )
    mapa_df["tasa"] = mapa_df["tasa"].fillna(0)
    tope = mapa_df[mapa_df["tasa"] > 0]["tasa"].quantile(0.95) if len(mapa_df[mapa_df["tasa"] > 0]) > 0 else 100

    fig = px.choropleth(
        mapa_df,
        geojson=mapa_df.geometry,
        locations=mapa_df.index,
        color="tasa",
        color_continuous_scale="YlOrRd",
        range_color=[0, tope],
        labels={"tasa": "Tasa x 100K"},
        hover_name="MPIO_CNMBR",
        hover_data={"DPTO_CNMBR": True, "tasa": ":.1f"},
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=650,
        coloraxis_colorbar=dict(
            title="Tasa x 100K",
            thickness=15,
            len=0.6,
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

with col_ranking:
    st.markdown(f"### Top 20 — {delito_sel}")
    top20 = (
        datos_filtrados.nlargest(20, "tasa")[["municipio", "departamento", "tasa", "cantidad"]]
        .reset_index(drop=True)
    )
    top20.index = top20.index + 1
    top20.columns = ["Municipio", "Depto", "Tasa", "Casos"]
    top20["Tasa"] = top20["Tasa"].round(1)
    st.dataframe(top20, height=600, use_container_width=True)


# ── Tendencia ──────────────────────────────────────────
st.markdown("---")
st.markdown("### Tendencia nacional")

tendencia = (
    agrupado[agrupado["tipo_delito"] == delito_sel]
    .groupby("anio")["tasa"]
    .mean()
    .reset_index()
)

fig_tend = px.line(
    tendencia,
    x="anio",
    y="tasa",
    markers=True,
    labels={"tasa": "Tasa promedio x 100K", "anio": "Año"},
)

fig_tend.update_traces(
    line_color="#e63946",
    line_width=3,
    marker_size=10,
)

fig_tend.update_layout(
    height=350,
    margin=dict(l=40, r=20, t=20, b=40),
    xaxis=dict(dtick=1),
)

# Marcar el año seleccionado
tasa_sel = tendencia[tendencia["anio"] == anio_sel]["tasa"].values
if len(tasa_sel) > 0:
    fig_tend.add_vline(x=anio_sel, line_dash="dash", line_color="gray", opacity=0.5)

st.plotly_chart(fig_tend, use_container_width=True)


# ── Footer ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align: center; opacity: 0.5; font-size: 0.85rem;'>"
    "Datos: Policía Nacional (SIEDCO) · Población: DANE · "
    "Tasa = (Delitos / Población) × 100,000"
    "</div>",
    unsafe_allow_html=True,
)
