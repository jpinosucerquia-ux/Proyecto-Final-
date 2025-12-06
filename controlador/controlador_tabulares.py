# controlador/controlador_tabulares.py
from PyQt5.QtWidgets import QFileDialog
from vista.vistas_loader.vista_tabulares import VistaTabulares
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ControladorTabulares:
    def __init__(self, modelo):
        self.modelo = modelo
        self.vista = VistaTabulares()
        self.df = None
        
        self.vista.cargar_csv_signal.connect(self.cargar_csv)
        self.vista.graficar_columna_signal.connect(self.graficar_columna)
        
    def cargar_csv(self):
        ruta, _ = QFileDialog.getOpenFileName(self.vista, "Cargar CSV", "", "Archivos CSV (*.csv)")
        if ruta:
            self.df = pd.read_csv(ruta)
            # Requisito: Elegir al menos 4 columnas 
            columnas = self.df.columns.tolist()
            self.vista.cargar_columnas_en_combo(columnas)
            self.vista.mostrar_datos_en_tabla(self.df)
            self.vista.mostrar_estado("CSV Cargado")

    def graficar_columna(self, columna):
        if self.df is not None and columna in self.df.columns:
            fig, ax = plt.subplots()
            ax.plot(self.df[columna])
            ax.set_title(f"Gráfica de {columna}")
            
            canvas = FigureCanvas(fig)
            
            # La vista debe tener un layout en el label o frame donde va la gráfica
            # self.vista.layout_grafica.addWidget(canvas) 
            # Nota: Necesitas ajustar la vista para tener un layout contenedor
            
            self.vista.lblGraficaCSV.setText("") # Ocultar texto si se pone gráfica encima