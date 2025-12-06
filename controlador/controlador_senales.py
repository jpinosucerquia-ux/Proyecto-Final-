# controlador/controlador_senales.py
from PyQt5.QtWidgets import QFileDialog
from vista.vistas_loader.vista_senales import VistaSenales
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ControladorSenales:
    def __init__(self, modelo):
        self.modelo = modelo
        self.vista = VistaSenales()
        
        # Conexiones
        self.vista.cargar_senal_signal.connect(self.cargar_senal)
        self.vista.transformada_fourier_signal.connect(self.calcular_fft)
        self.vista.graficar_espectro_signal.connect(self.graficar_espectro)
        
    def cargar_senal(self):
        ruta, _ = QFileDialog.getOpenFileName(self.vista, "Cargar Señal", "", "Archivos MAT (*.mat)")
        if ruta:
            # canales = self.modelo.cargar_datos(ruta)
            # self.vista.cargar_canales(canales)
            self.vista.mostrar_archivo_cargado(ruta)
            
            # Mock de canales
            self.vista.cargar_canales(["Canal 1", "Canal 2", "Canal 3"])

    def calcular_fft(self):
        # df_fft = self.modelo.calcular_fft()
        # self.vista.mostrar_resultados_fft(df_fft)
        
        # Mock para probar la tabla
        data = {'Frecuencia (Hz)': [10, 20, 30], 'Magnitud': [0.5, 0.8, 0.2]}
        df = pd.DataFrame(data)
        self.vista.mostrar_resultados_fft(df)

    def graficar_espectro(self, canal):
        # data_x, data_y = self.modelo.obtener_espectro(canal)
        
        # Crear gráfico Matplotlib
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot([1, 2, 3], [4, 5, 6]) # Mock data
        ax.set_title(f"Espectro del {canal}")
        ax.set_xlabel("Frecuencia")
        
        canvas = FigureCanvas(fig)
        
        # Insertar canvas en el layout de la vista
        # Nota: La vista necesita un método que acepte el widget y lo ponga en el layout
        # (Debes agregar un QVBoxLayout al framegraficasenal en Designer o por código)
        # self.vista.framegraficasenal.layout().addWidget(canvas)
        pass