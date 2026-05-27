"""
Utilidades geoespaciales.
Merge de datos con geometrías municipales.
"""

import logging

import geopandas as gpd
import pandas as pd

from src.config import ARCHIVO_GEOJSON

logger = logging.getLogger(__name__)


def cargar_geometrias(simplify_tolerance: float = 0.01) -> gpd.GeoDataFrame:
    """
    Carga y simplifica las geometrías municipales.

    Args:
        simplify_tolerance: Tolerancia para simplificación (menor = más detalle).

    Returns:
        GeoDataFrame con geometrías municipales simplificadas.
    """
    gdf = gpd.read_file(ARCHIVO_GEOJSON)
    gdf["geometry"] = gdf["geometry"].simplify(simplify_tolerance)
    logger.info(f"GeoJSON cargado: {len(gdf)} municipios")
    return gdf


def merge_con_geometrias(
    df: pd.DataFrame,
    gdf: gpd.GeoDataFrame,
    columna_codigo: str = "codigo_municipio",
) -> gpd.GeoDataFrame:
    """
    Merge de datos tabulares con geometrías municipales.

    Args:
        df: DataFrame con datos de criminalidad.
        gdf: GeoDataFrame con geometrías.
        columna_codigo: Nombre de la columna con código DIVIPOLA.

    Returns:
        GeoDataFrame con datos y geometrías combinados.
    """
    # TODO: Implementar merge
    # 1. Asegurar que los códigos sean del mismo tipo (str de 5 dígitos)
    # 2. Merge por código municipal
    # 3. Reportar municipios sin geometría y geometrías sin datos
    raise NotImplementedError("Implementar merge con geometrías")


def validar_cobertura(df: pd.DataFrame, gdf: gpd.GeoDataFrame) -> dict:
    """
    Valida cuántos municipios del GeoJSON tienen datos y viceversa.

    Returns:
        Dict con métricas de cobertura.
    """
    # TODO: Implementar validación
    return {
        "municipios_con_datos": 0,
        "municipios_sin_datos": 0,
        "datos_sin_geometria": 0,
        "cobertura_pct": 0.0,
    }
