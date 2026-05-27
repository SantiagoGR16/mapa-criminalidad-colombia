"""Tests para el módulo de transformación."""

import pandas as pd

from src.transform import normalizar_texto


class TestNormalizarTexto:
    def test_quita_tildes(self):
        assert normalizar_texto("Bogotá") == "BOGOTA"

    def test_mayusculas(self):
        assert normalizar_texto("medellín") == "MEDELLIN"

    def test_espacios_extra(self):
        assert normalizar_texto("  San José  ") == "SAN JOSE"

    def test_valor_nulo(self):
        assert pd.isna(normalizar_texto(None))

    def test_numero_como_string(self):
        assert normalizar_texto(123) == "123"
