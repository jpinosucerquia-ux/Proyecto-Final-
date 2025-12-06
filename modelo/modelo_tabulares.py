import pandas as pd

class ModeloTabular:

    def __init__(self):
        self.df = None

    def cargar_csv(self, ruta):
        self.df = pd.read_csv(ruta)
        return self.df

    def obtener_columnas(self):
        if self.df is None:
            return []
        return list(self.df.columns)

    def obtener_columna(self, nombre):
        return self.df[nombre]

        
