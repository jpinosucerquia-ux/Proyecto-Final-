# vista/vistas_loader/vista_login.py
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import os

UI_PATH = os.path.join(
    os.path.dirname(__file__),
    '..', 'ui', 'Login.ui'
)

class VistaLogin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(UI_PATH, self)

        self.lblmensaje.setText("")
    def mostrar_mensaje_error(self, mensaje: str):
        """Muestra un mensaje de error o estado en la etiqueta lblmensaje."""
        self.lblmensaje.setText(mensaje)
