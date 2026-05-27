"""
Pipeline de transformación.
Limpieza, normalización y merge con DIVIPOLA.
"""

import logging

import pandas as pd
from unidecode import unidecode

from src.config import ARCHIVO_DELITOS_RAW, ARCHIVO_DIVIPOLA, ARCHIVO_PROCESADO, PROCESSED_DIR

logger = logging.getLogger(__name__)


def normalizar_texto(texto: str) -> str:
    """Normaliza texto: sin tildes, mayúsculas, espacios extra."""
    if pd.isna(texto):
        return texto
    return unidecode(str(texto)).upper().strip()


def limpiar_delitos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el dataset de delitos.

    - Normaliza nombres de municipios y departamentos
    - Parsea fechas
    - Elimina duplicados
    - Categoriza tipos de delito
    """
    df = df.copy()

    # TODO: Implementar limpieza según la estructura real del dataset
    # df["municipio_norm"] = df["municipio"].apply(normalizar_texto)
    # df["departamento_norm"] = df["departamento"].apply(normalizar_texto)
    # df["fecha"] = pd.to_datetime(df["fecha_hecho"], errors="coerce")
    # df = df.dropna(subset=["fecha"])
    # df = df.drop_duplicates()

    logger.info(f"Dataset limpio: {len(df)} registros")
    return df


def merge_con_divipola(df: pd.DataFrame, divipola: pd.DataFrame) -> pd.DataFrame:
    """
    Asigna código DIVIPOLA estándar a cada registro.
    Usa matching por nombre normalizado como fallback.
    """
    # TODO: Implementar merge con DIVIPOLA
    # 1. Intentar merge por código municipal si existe
    # 2. Fallback: merge por nombre normalizado
    # 3. Logging de municipios que no matchearon
    return df


def ejecutar_transformacion():
    """Ejecuta el pipeline completo de transformación."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Cargando datos crudos...")
    df = pd.read_csv(ARCHIVO_DELITOS_RAW)
    divipola = pd.read_csv(ARCHIVO_DIVIPOLA)

    logger.info("Limpiando datos...")
    df = limpiar_delitos(df)

    logger.info("Merge con DIVIPOLA...")
    df = merge_con_divipola(df, divipola)

    logger.info(f"Guardando datos procesados en {ARCHIVO_PROCESADO}")
    df.to_parquet(ARCHIVO_PROCESADO, index=False)

    logger.info("Transformación completada.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ejecutar_transformacion()
