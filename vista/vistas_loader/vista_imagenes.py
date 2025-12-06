# vista/archivos para cargar vistas/vista_imagenes.py

from PyQt5.QtWidgets import QMainWindow, QSlider
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
import os

# --- 1. Definición de la Ruta del Archivo .ui ---
# Asume que este archivo .py está en 'vista/archivos para cargar vistas/'
# y que el .ui está en 'vista/ui/' (de ahí el '..\\ui')
UI_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui', 'Imagenesmedicas.ui')

# -------------------------------------------------

class VistaImagenes(QMainWindow):
    """
    Clase de la Vista para el procesamiento de Imágenes Médicas (DICOM, NIFTI, JPG/PNG).
    Hereda de QMainWindow.
    """
    
    # --- Señales Personalizadas (Interfaces con el Controlador) ---
    
    # Señal para solicitar la carga de un archivo de imagen médica
    cargar_imagen_signal = pyqtSignal()
    
    # Señal para solicitar el procesamiento de la imagen cargada (filtros, HU, etc.)
    procesar_imagen_signal = pyqtSignal()
    
    # Señal para solicitar el guardado de la imagen procesada
    guardar_imagen_signal = pyqtSignal()
    
    # Señal para solicitar la visualización de la información del paciente
    ver_info_paciente_signal = pyqtSignal()
    
    # Señales para la interactividad de los cortes 3D (axial, coronal, sagital)
    # Emite el nuevo valor del slider (índice del corte)
    slider_axial_changed = pyqtSignal(int)
    slider_coronal_changed = pyqtSignal(int)
    slider_sagital_changed = pyqtSignal(int)
    
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
            
        self.setWindowTitle("Procesamiento de Imágenes Médicas")
        
        # 3. Conexiones a los widgets

        # Conexiones de botones principales
        self.btnCargarImagenMedica.clicked.connect(self.cargar_imagen_signal.emit)
        self.btnProcesarImagen.clicked.connect(self.procesar_imagen_signal.emit)
        self.btnGuardarImagen.clicked.connect(self.guardar_imagen_signal.emit)
        self.btnInfoPaciente.clicked.connect(self.ver_info_paciente_signal.emit)
        self.btnvolverimagenes.clicked.connect(self.volver_signal.emit)

        # Conexiones de los sliders interactivos (Requerimiento de la tarea)
        # El controlador se conectará a estas señales para actualizar los cortes
        self.Slideraxial.valueChanged.connect(self.slider_axial_changed.emit)
        self.Slidercoronal.valueChanged.connect(self.slider_coronal_changed.emit)
        self.Slidersagital.valueChanged.connect(self.slider_sagital_changed.emit)
        
        # Inicializar elementos
        self.lblrtaEstado.setText("Esperando carga de archivo...")
        self.lblrtaArchivoC.setText("Ninguno")
        self.limpiar_visualizaciones()

    # --- Métodos de Interfaz (Actualizaciones desde el Controlador) ---

    def limpiar_visualizaciones(self):
        """Limpia las etiquetas de imagen al inicio o al cargar un nuevo archivo."""
        self.lblImagenAxial.clear()
        self.lblImagenCoronal.clear()
        self.lblImagenSagital.clear()
        
    def actualizar_corte_axial(self, q_pixmap: QPixmap, max_value: int):
        """Muestra el corte axial y actualiza el rango del slider."""
        self.lblImagenAxial.setPixmap(q_pixmap)
        self.Slideraxial.setMaximum(max_value)
        
    def actualizar_corte_coronal(self, q_pixmap: QPixmap, max_value: int):
        """Muestra el corte coronal y actualiza el rango del slider."""
        self.lblImagenCoronal.setPixmap(q_pixmap)
        self.Slidercoronal.setMaximum(max_value)

    def actualizar_corte_sagital(self, q_pixmap: QPixmap, max_value: int):
        """Muestra el corte sagital y actualiza el rango del slider."""
        self.lblImagenSagital.setPixmap(q_pixmap)
        self.Slidersagital.setMaximum(max_value)
        
    def mostrar_estado(self, mensaje: str):
        """Muestra un mensaje de estado en lblrtaEstado."""
        self.lblrtaEstado.setText(mensaje)
        
    def mostrar_archivo_cargado(self, nombre_archivo: str):
        """Muestra el nombre del archivo que se cargó."""
        self.lblrtaArchivoC.setText(nombre_archivo)
        
# -------------------------------------------------
# El uso real se hará desde el main.py y el controlador_imagenes.py