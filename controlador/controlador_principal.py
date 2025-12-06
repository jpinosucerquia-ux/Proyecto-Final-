# controlador/controlador_principal.py

from PyQt5.QtWidgets import QApplication
from vista.vistas_loader.vista_principal import VistaPrincipal

# Importar los controladores de los módulos
from controlador.controlador_imagenes import ControladorImagenes
from controlador.controlador_senales import ControladorSenales
from controlador.controlador_tabulares import ControladorTabulares
from controlador.controlador_historial import ControladorHistorial


class ControladorPrincipal:
    def __init__(self, usuario):
        """
        Controlador principal del Dashboard.
        Recibe el usuario autenticado desde el login.
        """
        self.usuario = usuario

        self.usuario = usuario
        self.vista = VistaPrincipal()
        self.vista.actualizar_usuario(usuario)


        # Inicializar controladores hijos
        # (sus vistas deben ser QWidget, no QMainWindow ni QDialog)
        self.ctrl_imagenes = ControladorImagenes(modelo=None)
        self.ctrl_senales = ControladorSenales(modelo=None)
        self.ctrl_tabulares = ControladorTabulares(modelo=None)
        self.ctrl_historial = ControladorHistorial(modelo=None)

        # Conectar señales del menú lateral
        self.vista.navegar_imagenes_signal.connect(self.mostrar_imagenes)
        self.vista.navegar_senales_signal.connect(self.mostrar_senales)
        self.vista.navegar_csv_signal.connect(self.mostrar_tabulares)
        self.vista.navegar_historial_signal.connect(self.mostrar_historial)
        self.vista.cerrar_sesion_signal.connect(self.cerrar_sesion)

        # Vista inicial
        self.mostrar_imagenes()

        # Mostrar ventana principal
        self.vista.show()

    # ---------------- Navegación ----------------

    def mostrar_imagenes(self):
        self.vista.mostrar_vista_contenido(self.ctrl_imagenes.vista)

    def mostrar_senales(self):
        self.vista.mostrar_vista_contenido(self.ctrl_senales.vista)

    def mostrar_tabulares(self):
        self.vista.mostrar_vista_contenido(self.ctrl_tabulares.vista)

    def mostrar_historial(self):
        self.vista.mostrar_vista_contenido(self.ctrl_historial.vista)

    def cerrar_sesion(self):
        self.vista.close()
        # El control vuelve a main.py
