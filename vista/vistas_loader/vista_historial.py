# vista/archivos para cargar vistas/vista_historial.py

from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject
import os

# --- 1. Definición de la Ruta del Archivo .ui ---
# Asume que este archivo .py está en 'vista/archivos para cargar vistas/'
# y que el .ui está en 'vista/ui/' (de ahí el '..\\ui')
UI_PATH = os.path.join(os.path.dirname(__file__), '..', 'ui', 'Historial.ui')

# -------------------------------------------------

class VistaHistorial(QWidget):
    """
    Clase de la Vista para el Historial de Registros de la Base de Datos.
    Hereda de QWidget, lo que lo hace ideal para ser incrustado en la Vista Principal (Dashboard).
    """
    
    # --- Señales Personalizadas (Interfaces con el Controlador) ---
    
    # Señal emitida al mostrar la vista, para solicitar la carga inicial de registros
    cargar_registros_signal = pyqtSignal()
    
    # Señal emitida al presionar 'Buscar', envía el texto de búsqueda
    buscar_registro_signal = pyqtSignal(str) 
    
    # Señal emitida al presionar 'Ver' para ver los detalles de un registro seleccionado
    ver_registro_signal = pyqtSignal(int) # Emite el ID o índice de la fila seleccionada
    
    # Señal emitida al presionar 'Eliminar'
    eliminar_registro_signal = pyqtSignal(int) # Emite el ID o índice de la fila a eliminar
    
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
            
        self.setWindowTitle("Historial de Actividad")
        
        # Configuración inicial de la tabla (opcional, se puede hacer en el controlador)
        self.tableRegistros.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableRegistros.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableRegistros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 3. Conexiones a los widgets
        
        self.btnBuscar.clicked.connect(self.handle_buscar)
        self.btnVer.clicked.connect(self.handle_ver_registro)
        self.btnEliminar.clicked.connect(self.handle_eliminar_registro)
        self.btnvolverhistorial.clicked.connect(self.volver_signal.emit)
        
        # Inicializar el campo de búsqueda
        self.lineBuscar.setText("")

    def handle_buscar(self):
        """Maneja el clic en 'Buscar'."""
        texto_busqueda = self.lineBuscar.text().strip()
        self.buscar_registro_signal.emit(texto_busqueda)

    def handle_ver_registro(self):
        """Maneja el clic en 'Ver' para el registro seleccionado."""
        seleccion = self.tableRegistros.currentRow()
        if seleccion >= 0:
            # Asumimos que la primera columna contiene el ID de la base de datos
            id_registro = self.tableRegistros.item(seleccion, 0).text()
            try:
                self.ver_registro_signal.emit(int(id_registro))
            except ValueError:
                # Si el ID no es numérico, manejar el error
                print("Error: ID de registro inválido.")
        
    def handle_eliminar_registro(self):
        """Maneja el clic en 'Eliminar'."""
        seleccion = self.tableRegistros.currentRow()
        if seleccion >= 0:
            # Asumimos que la primera columna contiene el ID de la base de datos
            id_registro = self.tableRegistros.item(seleccion, 0).text()
            try:
                self.eliminar_registro_signal.emit(int(id_registro))
            except ValueError:
                 print("Error: ID de registro inválido para eliminar.")

    # --- Métodos que el Controlador puede llamar para actualizar la Vista ---

    def mostrar_registros(self, data: list, headers: list):
        """
        Puebla la QTableWidget con los datos de la base de datos.
        :param data: Lista de tuplas o listas con los registros.
        :param headers: Lista de strings con los nombres de las columnas.
        """
        self.tableRegistros.setRowCount(len(data))
        self.tableRegistros.setColumnCount(len(headers))
        self.tableRegistros.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, item in enumerate(row_data):
                self.tableRegistros.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
                
    def showEvent(self, event):
        """Método llamado cuando la ventana es mostrada. Solicita la carga inicial de datos."""
        super().showEvent(event)
        self.cargar_registros_signal.emit()


# -------------------------------------------------
# El uso real se hará desde el main.py y el controlador_historial.py