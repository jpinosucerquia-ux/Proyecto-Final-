   # ============================================================
# MODELO TABULAR (Datos CSV)
# ============================================================

import pandas as pd


class ModeloTabular:
    """
    Modelo para:
    - Cargar archivos CSV
    - Mostrar columnas
    - Extraer columnas individuales para graficar
    """

    def __init__(self):
        self.df = None

    def cargar_csv(self, ruta):
        self.df = pd.read_csv(ruta)
        return self.df

    def obtener_columnas(self):
        return list(self.df.columns) if self.df is not None else []

    def obtener_columna(self, nombre):
        if self.df is None:
            raise ValueError("Debe cargar un CSV primero.")
        return self.df[nombre]