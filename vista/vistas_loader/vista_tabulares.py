# vista/archivos para cargar vistas/vista_tabulares.py

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
import os

# --- 1. Definición de la Ruta del Archivo .ui ---
# Asume que este archivo .py está en 'vista/archivos para cargar vistas/'
# y que el .ui está en 'vista/ui/' (de ahí el '..\\ui')
UI_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui', 'CSV.ui')

# -------------------------------------------------

class VistaTabulares(QDialog):
    """
    Clase de la Vista para el procesamiento y análisis de Datos Tabulares (CSV).
    Hereda de QDialog porque el diseño en el .ui es un Dialog.
    """
    
    # --- Señales Personalizadas (Interfaces con el Controlador) ---
    
    # Emite una señal para solicitar la carga de un archivo CSV
    cargar_csv_signal = pyqtSignal()
    
    # Emite la columna seleccionada para que el Controlador genere la gráfica tipo plot.
    # El PDF requiere elegir al menos 4 columnas, por lo que la señal usa la columna seleccionada. [cite: 45, 46]
    graficar_columna_signal = pyqtSignal(str) 
    
    # Señales para operaciones secundarias
    limpiar_grafica_signal = pyqtSignal()
    exportar_grafica_signal = pyqtSignal()
    volver_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 2. Cargar el diseño con loadUI
        try:
            uic.loadUi(UI_PATH, self)
        except FileNotFoundError:
            print(f"Error: No se pudo cargar el archivo UI en la ruta: {UI_PATH}")
            return
            
        self.setWindowTitle("Análisis de Datos Tabulares (CSV)")
        
        # 3. Conexiones a los widgets
        
        # Conexión de botones
        self.btnCargarCSV.clicked.connect(self.handle_cargar_csv)
        self.btnGraficarCSV.clicked.connect(self.handle_graficar_csv)
        self.btnLimpiarGrafica.clicked.connect(self.limpiar_grafica_signal.emit)
        self.btnExportarGrafica.clicked.connect(self.exportar_grafica_signal.emit)
        self.btnvolverCSV.clicked.connect(self.volver_signal.emit)

        # Inicializar elementos
        self.lblrtaestadoCSV.setText("Esperando archivo...")
        self.lblrtavariableCSV.setText("")

    # --- Métodos de Interacción (Handlers) ---

    def handle_cargar_csv(self):
        """Maneja el clic en 'Cargar CSV'."""
        self.cargar_csv_signal.emit()

    def handle_graficar_csv(self):
        """Maneja el clic en 'Graficar CSV'."""
        columna_seleccionada = self.comboColumnas.currentText()
        if columna_seleccionada:
            self.graficar_columna_signal.emit(columna_seleccionada)
        else:
            self.mostrar_estado("ERROR: Seleccione una columna")

    # --- Métodos que el Controlador puede llamar para actualizar la Vista ---
    
    def cargar_columnas_en_combo(self, lista_columnas: list):
        """Carga los nombres de las columnas en el QComboBox."""
        self.comboColumnas.clear()
        self.comboColumnas.addItems(lista_columnas)
    
    def mostrar_datos_en_tabla(self, df):
        """
        Muestra los datos cargados en el QTableWidget (tablaCSV)[cite: 47].
        (La implementación real requeriría convertir el DataFrame de Pandas a un modelo de tabla de PyQt).
        """
        self.tablaCSV.setRowCount(df.shape[0])
        self.tablaCSV.setColumnCount(df.shape[1])
        self.tablaCSV.setHorizontalHeaderLabels(df.columns)
        
        # Ejemplo: Aquí iría la lógica para poblar la QTableWidget con df.values
        # Por ahora solo actualizamos el estado:
        self.mostrar_estado(f"CSV cargado con {df.shape[0]} filas.")
        
    def mostrar_estado(self, mensaje: str):
        """Muestra un mensaje de estado en lblrtaestadoCSV."""
        self.lblrtaestadoCSV.setText(mensaje)
        
    def actualizar_grafica(self, widget_matplotlib):
        """
        Inserta el gráfico generado (Matplotlib Canvas) en el área designada (label)
        para la visualización en la interfaz[cite: 46].
        (La implementación real requiere un layout y un QWidget en lugar de solo un QLabel).
        """
        # Aquí iría la lógica para limpiar el layout del área de gráfica y
        # agregar el widget_matplotlib (e.g., QWidget de Matplotlib).
        self.lblGraficaCSV.setText("Gráfica cargada exitosamente.")
        self.lblrtavariableCSV.setText(self.comboColumnas.currentText())

# -------------------------------------------------

# El uso real se hará desde el main.py y el controlador_tabulares.py