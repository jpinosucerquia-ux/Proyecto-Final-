from PyQt5 import QtCore, QtGui, QtWidgets
class ControladorLogin:
    def __init__(self, ventana_login, modelo):
        self.ventana_login = ventana_login
        self.ui = ventana_login.ui
        self.modelo = modelo

        # Ocultar mensaje al inicio
        self.ui.lblmensaje.setVisible(False)

        # Conectar botones
        self.ui.btnIngresar.clicked.connect(self.login)
        self.ui.btnSalir.clicked.connect(self.ventana_login.close)
    
    def login(self):
        usuario = self.ui.lnputUsuario.text()
        contrasena = self.ui.InputContrasena.text()
        if self.modelo.validar_usuario(usuario, contrasena):
            self.ui.lblmensaje.setVisible(False)
            self.ventana_login.close()
            self.abrir_captura(usuario)
        else:
            self.ui.lblmensaje.setText("Usuario o contraseña incorrecta")
            self.ui.lblmensaje.setStyleSheet("color: red; font-weight: bold;")
            self.ui.lblmensaje.setVisible(True)


    def abrir_captura(self, usuario):
        from Vista.Captura import Ui_Dialog
        self.ventana_captura = QtWidgets.QDialog()
        self.ui_captura = Ui_Dialog()
        self.ui_captura.setupUi(self.ventana_captura)

        # Conectar botones
        self.ui_captura.btnCapturar.clicked.connect(lambda: self.capturar_imagen(usuario))
        self.ui_captura.btnGuardarTemporal.clicked.connect(lambda: self.guardar_temporal(usuario))

        self.ventana_captura.show()

    def capturar_imagen(self, usuario):
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.ultima_imagen = gris
            cv2.imshow("Captura", gris)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
        else:
            print("No se pudo acceder a la cámara")

    def guardar_temporal(self, usuario):
        import cv2
        import os
        if hasattr(self, "ultima_imagen"):
            carpeta = os.path.join("Usuarios", usuario)
            os.makedirs(carpeta, exist_ok=True)
            ruta = os.path.join(carpeta, "temporal.png")
            cv2.imwrite(ruta, self.ultima_imagen)
            print(f"Imagen guardada temporalmente en: {ruta}")
            self.ventana_captura.close()  # cerrar la ventana de captura
            self.abrir_dashboard()        # abrir dashboard
        else:
            print("Primero capture la imagen")

    def abrir_dashboard(self):
        from Vista.dashboard import Ui_MainWindow  # tu vista de dashboard
        self.ventana_dashboard = QtWidgets.QMainWindow()
        self.ui_dashboard = Ui_MainWindow()
        self.ui_dashboard.setupUi(self.ventana_dashboard)
        self.ventana_dashboard.show()