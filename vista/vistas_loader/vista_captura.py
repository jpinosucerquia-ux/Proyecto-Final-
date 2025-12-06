# vista/archivos para cargar vistas/vista_captura.py

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
import os

# --- 1. Definición de la Ruta del Archivo .ui ---
# Asume que este archivo .py está en 'vista/archivos para cargar vistas/'
# y que el .ui está en 'vista/ui/' (de ahí el '..\\ui')
UI_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui', 'Captura.ui')

# -------------------------------------------------

class VistaCaptura(QDialog):
    """
    Clase de la Vista para la funcionalidad de Captura de Imagen con OpenCV.
    Hereda de QDialog porque el diseño en el .ui es un Dialog.
    """
    
    # --- Señales Personalizadas (Interfaces con el Controlador) ---
    # La Vista emite estas señales, el Controlador se conecta a ellas.
    
    # Señal emitida al iniciar la ventana para solicitar el encendido de la cámara
    iniciar_stream_signal = pyqtSignal()
    
    # Señal emitida al presionar 'Capturar'. 
    capturar_imagen_signal = pyqtSignal()
    
    # Señal emitida al presionar 'Guardar Temporal'. Envía el nombre del archivo.
    guardar_temporal_signal = pyqtSignal(str) 
    
    # Señal emitida al presionar 'Nueva Captura'
    nueva_captura_signal = pyqtSignal()
    
    # Señal emitida al presionar 'Volver'
    volver_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 2. Cargar el diseño con loadUI (Requerimiento del proyecto)
        try:
            uic.loadUi(UI_PATH, self)
        except FileNotFoundError:
            print(f"Error: No se pudo cargar el archivo UI en la ruta: {UI_PATH}")
            return
            
        self.setWindowTitle("Captura de Imagen")
        
        # Conectar los botones a los métodos internos de la Vista
        self.btnCapturar.clicked.connect(self.handle_capturar)
        self.btnGuardartemporal.clicked.connect(self.handle_guardar_temporal)
        self.btnNuevaCaptura.clicked.connect(self.handle_nueva_captura)
        self.btnvolvercaptura.clicked.connect(self.handle_volver)
        
        # Ocultar o inicializar elementos que no deben estar listos al inicio
        self.lblImagenCapturada.setText("Esperando captura...")
        self.linenombreimagen.clear()
        
    def showEvent(self, event):
        """Método llamado cuando la ventana es mostrada."""
        super().showEvent(event)
        # Emitir la señal para que el controlador inicie el stream de OpenCV
        self.iniciar_stream_signal.emit()

    def handle_capturar(self):
        """Maneja el clic en 'Capturar' y emite la señal al Controlador."""
        self.capturar_imagen_signal.emit()
        
    def handle_nueva_captura(self):
        """Maneja el clic en 'Nueva Captura' y emite la señal al Controlador."""
        self.nueva_captura_signal.emit()

    def handle_guardar_temporal(self):
        """Maneja el clic en 'Guardar Temporal'."""
        nombre_archivo = self.linenombreimagen.text().strip()
        if nombre_archivo:
            # Emitir la señal al Controlador con el nombre deseado
            self.guardar_temporal_signal.emit(nombre_archivo)
        else:
            self.lblestadodecamara.setText("ERROR: Ingrese un nombre de archivo")

    def handle_volver(self):
        """Maneja el clic en 'volver' y emite la señal al Controlador."""
        self.volver_signal.emit()
        
    # --- Métodos que el Controlador puede llamar para actualizar la Vista ---

    def actualizar_stream(self, q_pixmap):
        """Muestra el frame de la cámara en lblStream."""
        self.lblStream.setPixmap(q_pixmap)
        
    def mostrar_estado(self, mensaje: str):
        """Muestra un mensaje de estado en lblestadodecamara."""
        self.lblestadodecamara.setText(mensaje)
        
    def mostrar_imagen_capturada(self, q_pixmap):
        """Muestra la imagen capturada en lblImagenCapturada."""
        self.lblImagenCapturada.setPixmap(q_pixmap)
        
    def limpiar_inputs(self):
        """Limpia la entrada del nombre de la imagen."""
        self.linenombreimagen.clear()
        
# -------------------------------------------------

# Ejemplo de uso (solo para pruebas internas, se debe usar desde main.py)
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Simulación simple de la Vista:
    vista = VistaCaptura()
    
    # Simulación de la conexión al Controlador (solo para demostrar las señales):
    vista.capturar_imagen_signal.connect(lambda: print("Señal: Capturar Imagen emitida"))
    vista.guardar_temporal_signal.connect(lambda name: print(f"Señal: Guardar Temporal emitida con nombre: {name}"))
    vista.iniciar_stream_signal.connect(lambda: print("Señal: Iniciar Stream emitida"))
    
    vista.show()
    sys.exit(app.exec_())