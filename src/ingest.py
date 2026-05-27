"""
Pipeline de ingesta de datos.
Descarga datasets desde Datos Abiertos Colombia y fuentes del DANE.
"""

import logging
from pathlib import Path

import pandas as pd
import requests

from src.config import (
    SOCRATA_DOMAIN,
    SOCRATA_APP_TOKEN,
    DATASETS,
    RAW_DIR,
    GEO_DIR,
    ARCHIVO_DELITOS_RAW,
    ARCHIVO_DIVIPOLA,
    ARCHIVO_POBLACION,
    ARCHIVO_GEOJSON,
)

logger = logging.getLogger(__name__)


def _asegurar_directorios():
    """Crea los directorios de datos si no existen."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    GEO_DIR.mkdir(parents=True, exist_ok=True)


def _archivo_existe(path: Path) -> bool:
    """Verifica si un archivo ya fue descargado (idempotencia)."""
    if path.exists() and path.stat().st_size > 0:
        logger.info(f"Archivo ya existe, saltando descarga: {path.name}")
        return True
    return False


def descargar_delitos(force: bool = False) -> pd.DataFrame:
    """
    Descarga el dataset de delitos desde Datos Abiertos Colombia.

    Args:
        force: Si True, descarga aunque el archivo ya exista.

    Returns:
        DataFrame con los datos crudos de delitos.
    """
    if not force and _archivo_existe(ARCHIVO_DELITOS_RAW):
        return pd.read_csv(ARCHIVO_DELITOS_RAW)

    # TODO: Implementar descarga real con sodapy
    # from sodapy import Socrata
    # client = Socrata(SOCRATA_DOMAIN, SOCRATA_APP_TOKEN)
    # results = client.get(DATASETS["delitos"], limit=500000)
    # df = pd.DataFrame.from_records(results)

    raise NotImplementedError(
        "Implementar descarga después de identificar el dataset ID correcto en datos.gov.co"
    )


def descargar_divipola(force: bool = False) -> pd.DataFrame:
    """Descarga la tabla DIVIPOLA del DANE."""
    if not force and _archivo_existe(ARCHIVO_DIVIPOLA):
        return pd.read_csv(ARCHIVO_DIVIPOLA)

    # TODO: Implementar descarga desde DANE
    raise NotImplementedError("Implementar descarga de DIVIPOLA")


def descargar_poblacion(force: bool = False) -> pd.DataFrame:
    """Descarga proyecciones de población municipal del DANE."""
    if not force and _archivo_existe(ARCHIVO_POBLACION):
        return pd.read_csv(ARCHIVO_POBLACION)

    # TODO: Implementar descarga desde DANE
    raise NotImplementedError("Implementar descarga de proyecciones de población")


def descargar_geojson(force: bool = False) -> Path:
    """Descarga el GeoJSON de municipios de Colombia."""
    if not force and _archivo_existe(ARCHIVO_GEOJSON):
        return ARCHIVO_GEOJSON

    # TODO: Implementar descarga del GeoJSON
    # Fuente sugerida: https://github.com/... (buscar repo con geometrías municipales)
    raise NotImplementedError("Implementar descarga del GeoJSON municipal")


def ejecutar_ingesta(force: bool = False):
    """Ejecuta el pipeline completo de ingesta."""
    _asegurar_directorios()
    logger.info("Iniciando pipeline de ingesta...")

    descargar_delitos(force=force)
    descargar_divipola(force=force)
    descargar_poblacion(force=force)
    descargar_geojson(force=force)

    logger.info("Pipeline de ingesta completado.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ejecutar_ingesta()
