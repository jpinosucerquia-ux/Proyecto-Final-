import sys
import os
from PyQt5 import QtWidgets

# 1. ACTUALIZACIÓN DE IMPORTACIONES
# Ahora importamos la clase de la vista desde 'vista.vista_login'
# y la clase del modelo desde 'modelo.modelo_auth' (anteriormente autenticacion)
from vista.vista_login import VistaLogin # Clase de la Ventana de Login (Clase que carga Login.ui)
from modelo.modelo_auth import ModeloUsuarios # Clase del Modelo de Autenticación
from controlador.controlador_login import ControladorLogin # Clase del Controlador de Login

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # 2. DEFINICIÓN DE CLASES
    # Usamos la clase Python de la Vista (VistaLogin), que ya carga el archivo .ui
    ventana_login_clase = VistaLogin()
    
    # 3. RUTA DEL ARCHIVO XML
    # La ruta al XML ahora es 'config/usuarios.xml' desde la raíz del proyecto.
    ruta_xml = os.path.join(os.path.dirname(__file__), "config", "usuarios.xml")
    
    # El modelo de usuarios (ModeloUsuarios)
    modelo = ModeloUsuarios(ruta_xml)

    # El controlador de Login
    controlador = ControladorLogin(ventana_login_clase, modelo)

    # 4. MOSTRAR VENTANA
    # Ahora mostramos la clase de la Vista directamente
    ventana_login_clase.show()

    sys.exit(app.exec_())