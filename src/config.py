"""
Configuración central del proyecto.
Rutas, constantes y parámetros globales.
"""

from pathlib import Path

# ── Rutas ──────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
GEO_DIR = DATA_DIR / "geo"

# ── Datos Abiertos Colombia (API SODA) ─────────────────
SOCRATA_DOMAIN = "www.datos.gov.co"
SOCRATA_APP_TOKEN = None  # Opcional: mejora rate limits

# Dataset IDs en datos.gov.co (actualizar con los reales)
DATASETS = {
    # TODO: Reemplazar con los dataset IDs reales después de explorar datos.gov.co
    "delitos": "DATASET_ID_AQUI",
}

# ── Parámetros de análisis ─────────────────────────────
TASA_POR = 100_000  # Tasa por cada 100,000 habitantes
ANIO_MIN = 2018
ANIO_MAX = 2024

# ── Archivos de salida ─────────────────────────────────
ARCHIVO_DELITOS_RAW = RAW_DIR / "delitos.csv"
ARCHIVO_DIVIPOLA = RAW_DIR / "divipola.csv"
ARCHIVO_POBLACION = RAW_DIR / "poblacion_municipal.csv"
ARCHIVO_GEOJSON = GEO_DIR / "municipios.geojson"
ARCHIVO_PROCESADO = PROCESSED_DIR / "delitos_procesados.parquet"
ARCHIVO_TASAS = PROCESSED_DIR / "tasas_municipales.parquet"
