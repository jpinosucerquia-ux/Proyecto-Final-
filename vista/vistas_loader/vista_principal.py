# vista/vistas_loader/vista_principal.py

from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import os


class VistaPrincipal(QMainWindow):

    navegar_imagenes_signal = pyqtSignal()
    navegar_senales_signal = pyqtSignal()
    navegar_csv_signal = pyqtSignal()
    navegar_historial_signal = pyqtSignal()
    cerrar_sesion_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # --- Ruta absoluta segura al UI ---
        UI_PATH = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "ui", "dashboard.ui")
        )

        if not os.path.exists(UI_PATH):
            raise FileNotFoundError(f"No se encontró el archivo UI: {UI_PATH}")

        # ✅ CARGAR EL UI (ESTO FALTABA)
        uic.loadUi(UI_PATH, self)

        self.setWindowTitle("Plataforma Multimodal para Diagnóstico Asistido")

        # ✅ Conectar botones → señales
        self.btnImagenes.clicked.connect(self.navegar_imagenes_signal.emit)
        self.btnSenales.clicked.connect(self.navegar_senales_signal.emit)
        self.btnCSV.clicked.connect(self.navegar_csv_signal.emit)
        self.btnHistorial.clicked.connect(self.navegar_historial_signal.emit)
        self.btnCerrarSesion.clicked.connect(self.cerrar_sesion_signal.emit)

        # Estado inicial
        self.lblusuarioactivo.setText("Bienvenido, Usuario")

    def mostrar_vista_contenido(self, widget: QWidget):
        """
        Inserta una vista (widget) en el stack central
        """
        if self.stackprincipal.indexOf(widget) == -1:
            self.stackprincipal.addWidget(widget)

        self.stackprincipal.setCurrentWidget(widget)

    def actualizar_usuario(self, usuario: str):
        self.lblusuarioactivo.setText(f"Bienvenido, {usuario}")
