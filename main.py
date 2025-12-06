# main.py (Versión de Señales Ajustada)

import sys
from PyQt5.QtWidgets import QApplication
from controlador.controlador_login import ControladorLogin
from controlador.controlador_principal import ControladorPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. Crear el controlador de login
    ctrl_login = ControladorLogin(modelo_auth=None)
    
    # Al tener login exitoso, esta función inicia el controlador principal
    def iniciar_app(usuario):
        # Esta función se llama y el controlador de login ya cerró su vista
        principal_ctrl = ControladorPrincipal(usuario)
        principal_ctrl.vista.show()
        # Nota: La aplicación principal (dashboard) mantendrá el QApp vivo
    
    # Conectar la señal del controlador (no de la vista)
    ctrl_login.login_exitoso.connect(iniciar_app)
    
    # Mostrar la ventana de Login para iniciar el ciclo
    ctrl_login.vista.show()
    
    # Entregar el control al bucle de eventos
    sys.exit(app.exec_())