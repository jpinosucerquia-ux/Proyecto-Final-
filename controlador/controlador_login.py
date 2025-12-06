from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
from vista.vistas_loader.vista_login import VistaLogin

class SignalHandler(QObject):
        login_exitoso = pyqtSignal(str) # Emite el nombre de usuario

class ControladorLogin(QObject):
        
    def __init__(self, modelo_auth):
        super().__init__()
        self.modelo = modelo_auth
        self.vista = VistaLogin()
        self.signal_handler = SignalHandler()
        self.login_exitoso = self.signal_handler.login_exitoso # Exponer la señal
        self.vista.btnIngresar.clicked.connect(self.validar_credenciales)

    def validar_credenciales(self):
        usuario = self.vista.lnputUsuario.text()
        contrasena = self.vista.InputContrasena.text()

        login_exitoso = (usuario != "" and contrasena != "")

        if login_exitoso:
            self.signal_handler.login_exitoso.emit(usuario) # EMITE LA SEÑAL
            self.vista.close() # <--- CIERRA LA VENTANA DE LOGIN AQUÍ
        else:
            self.vista.mostrar_mensaje_error("Credenciales incorrectas")
