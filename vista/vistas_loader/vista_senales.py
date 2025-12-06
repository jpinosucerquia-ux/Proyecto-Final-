# vista/archivos para cargar vistas/vista_senales.py

from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
import os

# --- 1. Definición de la Ruta del Archivo .ui ---
# Asume que este archivo .py está en 'vista/archivos para cargar vistas/'
# y que el .ui está en 'vista/ui/' (de ahí el '..\\ui')
UI_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui', 'señalesbiomedicas.ui')

# -------------------------------------------------

class VistaSenales(QWidget):
    """
    Clase de la Vista para el Procesamiento de Señales Biomédicas (ECG/EEG).
    Hereda de QWidget.
    """
    
    # --- Señales Personalizadas (Interfaces con el Controlador) ---
    
    # Señal para solicitar la carga de la señal biomédica (.mat)
    cargar_senal_signal = pyqtSignal()
    
    # Señal emitida al presionar 'Trans. Fourier', solicita el cálculo de FFT.
    transformada_fourier_signal = pyqtSignal()
    
    # Señal para solicitar la gráfica del espectro de frecuencias de un canal específico
    graficar_espectro_signal = pyqtSignal(str) # Emite el nombre/índice del canal seleccionado [cite: 40]
    
    # Señal para solicitar el cálculo de desviación estándar y el histograma [cite: 41]
    graficar_histograma_signal = pyqtSignal(str) # Emite el eje (o tipo de desviación) seleccionado [cite: 42]
    
    # Señal para volver a la vista principal
    volver_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 2. Cargar el diseño con loadUI
        try:
            uic.loadUi(UI_PATH, self)
        except FileNotFoundError:
            print(f"Error: No se pudo cargar el archivo UI en la ruta: {UI_PATH}")
            return
            
        self.setWindowTitle("Procesamiento de Señales Biomédicas")
        
        # 3. Conexiones a los widgets
        
        # Conexiones de botones principales
        self.btnCargarSenal.clicked.connect(self.cargar_senal_signal.emit)
        self.btnTransFourier.clicked.connect(self.transformada_fourier_signal.emit)
        self.btnGraficarSenal.clicked.connect(self.handle_graficar_espectro)
        self.btngraficarhistograma.clicked.connect(self.handle_graficar_histograma)
        self.btnCerrarsenales.clicked.connect(self.volver_signal.emit)

        # Inicializar elementos
        self.lblarchivocargadosenal.setText("Ninguno")
        self.lblestadosenal.setText("Listo.")
        self.comBoxCanal.clear()
        self.comBoxTiposenal.clear()
        
        # Configuración inicial de la tabla (para resultados FFT)
        self.tablesenal.setSelectionBehavior(QTableWidget.SelectRows)
        self.tablesenal.setEditTriggers(QTableWidget.NoEditTriggers)
        
    # --- Métodos de Interacción (Handlers) ---

    def handle_graficar_espectro(self):
        """Maneja el clic en 'Graficar Señal'."""
        canal_seleccionado = self.comBoxCanal.currentText()
        if canal_seleccionado:
            # Requisito: ver una gráfica del espectro de frecuencias de un canal elegido [cite: 40]
            self.graficar_espectro_signal.emit(canal_seleccionado)
        else:
            self.mostrar_estado("ERROR: Seleccione un canal para graficar.")
            
    def handle_graficar_histograma(self):
        """Maneja el clic en 'Graficar Histograma' (asociado a desviación estándar)[cite: 41, 42]."""
        # Aquí se asume que el ComboBox 'comBoxTiposenal' puede tener opciones de eje 
        # (aunque su nombre sugiere tipo de señal, lo usamos para el requisito del eje)
        eje_seleccionado = self.comBoxTiposenal.currentText()
        if eje_seleccionado:
            # Requisito: botón para calcular desviación estándar y mostrar histograma según el eje [cite: 41, 42]
            self.graficar_histograma_signal.emit(eje_seleccionado)
        else:
            self.mostrar_estado("ERROR: Seleccione un tipo de señal/eje.")


    # --- Métodos que el Controlador puede llamar para actualizar la Vista ---
    
    def cargar_canales(self, lista_canales: list):
        """Carga los nombres de los canales en el QComboBox."""
        self.comBoxCanal.clear()
        self.comBoxCanal.addItems(lista_canales)
        
    def cargar_tipos_senal(self, lista_tipos: list):
        """Carga los tipos de señal (si aplica, o las opciones de eje para el histograma)."""
        self.comBoxTiposenal.clear()
        self.comBoxTiposenal.addItems(lista_tipos)
    
    def mostrar_resultados_fft(self, df_resultados):
        """
        Muestra los resultados de la FFT (frecuencias dominantes y magnitudes) 
        en la QTableWidget 'tablesenal'[cite: 37, 38].
        """
        self.tablesenal.setRowCount(df_resultados.shape[0])
        self.tablesenal.setColumnCount(df_resultados.shape[1])
        self.tablesenal.setHorizontalHeaderLabels(df_resultados.columns)
        
        for row_idx, row_data in df_resultados.iterrows():
            for col_idx, item in enumerate(row_data):
                # Formato a dos decimales para mejor visualización
                self.tablesenal.setItem(row_idx, col_idx, QTableWidgetItem(f"{item:.2f}"))

        self.mostrar_estado("FFT calculada y resultados mostrados.")
        
    def actualizar_grafica_senal(self, widget_matplotlib):
        """
        Inserta el gráfico de la señal/espectro en el área designada (framegraficasenal).
        """
        # Implementación: Limpiar el layout de framegraficasenal y agregar widget_matplotlib
        self.mostrar_estado("Espectro graficado.")
        
    def actualizar_histograma(self, widget_matplotlib):
        """
        Inserta el gráfico del histograma en el área designada (framehistograma).
        """
        # Implementación: Limpiar el layout de framehistograma y agregar widget_matplotlib
        self.mostrar_estado("Histograma de desviación estándar graficado.")
        
    def mostrar_estado(self, mensaje: str):
        """Muestra un mensaje de estado en lblestadosenal."""
        self.lblestadosenal.setText(mensaje)
        
    def mostrar_archivo_cargado(self, nombre_archivo: str):
        """Muestra el nombre del archivo de señal que se cargó."""
        self.lblarchivocargadosenal.setText(nombre_archivo)
        
# -------------------------------------------------