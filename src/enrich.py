"""
Pipeline de enriquecimiento.
Cálculo de tasas per cápita, índices compuestos y variaciones.
"""

import logging

import pandas as pd

from src.config import (
    TASA_POR,
    ARCHIVO_PROCESADO,
    ARCHIVO_POBLACION,
    ARCHIVO_TASAS,
    PROCESSED_DIR,
)

logger = logging.getLogger(__name__)


def calcular_tasas(
    delitos: pd.DataFrame,
    poblacion: pd.DataFrame,
    tasa_por: int = TASA_POR,
) -> pd.DataFrame:
    """
    Calcula tasas de criminalidad per cápita por municipio y año.

    Fórmula: (delitos / población) × 100,000

    Args:
        delitos: DataFrame con conteo de delitos por municipio/año.
        poblacion: DataFrame con población por municipio/año.
        tasa_por: Base de la tasa (default: 100,000 habitantes).

    Returns:
        DataFrame con tasas calculadas.
    """
    # TODO: Implementar cálculo de tasas
    # 1. Agrupar delitos por municipio, año, tipo
    # 2. Merge con población
    # 3. Calcular tasa = (conteo / poblacion) * tasa_por
    # 4. Manejar divisiones por cero (municipios sin población reportada)
    raise NotImplementedError("Implementar cálculo de tasas")


def calcular_variacion_interanual(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la variación porcentual año a año por municipio.

    Fórmula: ((tasa_actual - tasa_anterior) / tasa_anterior) × 100
    """
    # TODO: Implementar variación interanual
    return df


def calcular_indice_compuesto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula un índice compuesto de criminalidad ponderado por gravedad.

    Pesos sugeridos:
    - Homicidio: 10
    - Lesiones personales: 5
    - Hurto: 3
    - Violencia intrafamiliar: 4
    """
    # TODO: Implementar índice compuesto
    return df


def ejecutar_enriquecimiento():
    """Ejecuta el pipeline completo de enriquecimiento."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Cargando datos procesados...")
    delitos = pd.read_parquet(ARCHIVO_PROCESADO)
    poblacion = pd.read_csv(ARCHIVO_POBLACION)

    logger.info("Calculando tasas per cápita...")
    tasas = calcular_tasas(delitos, poblacion)

    logger.info("Calculando variación interanual...")
    tasas = calcular_variacion_interanual(tasas)

    logger.info("Calculando índice compuesto...")
    tasas = calcular_indice_compuesto(tasas)

    logger.info(f"Guardando tasas en {ARCHIVO_TASAS}")
    tasas.to_parquet(ARCHIVO_TASAS, index=False)

    logger.info("Enriquecimiento completado.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ejecutar_enriquecimiento()
