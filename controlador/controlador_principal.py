# controlador/controlador_principal.py

from vista.vista_imagenes import VistaImagenes
# Se deben importar el resto de Vistas para la navegación:
# from vista.vista_senales import VistaSenales
# from vista.vista_tabulares import VistaTabulares

class ControladorPrincipal:
    """
    Controlador central para la navegación entre las principales funcionalidades.
    """
    def __init__(self, vista_principal):
        self.vista = vista_principal
        # self.modelo_db = modelo_db # Si maneja el registro de sesión
        
        # Conexión de botones de navegación (asumiendo que existen en VistaPrincipal)
        # Ejemplo: self.vista.ui.btn_imagenes.clicked.connect(self.abrir_imagenes)
        # Ejemplo: self.vista.ui.btn_senales.clicked.connect(self.abrir_senales)
        # Ejemplo: self.vista.ui.btn_tabulares.clicked.connect(self.abrir_tabulares)
        
        # Diccionario para mantener instancias de sub-vistas
        self.vistas_secundarias = {} 

    def abrir_imagenes(self):
        """
        Abre la interfaz de procesamiento de imágenes.
        """
        if 'imagenes' not in self.vistas_secundarias:
            # Requeriría la instancia del modelo de imágenes
            # modelo_img = ... 
            
            vista_img = VistaImagenes()
            # controlador_img = ControladorImagenes(vista_img, modelo_img)
            
            self.vistas_secundarias['imagenes'] = vista_img # o controlador_img
        
        # Asumiendo que la vista principal tiene un QStackedWidget o similar para mostrar el contenido
        # self.vista.ui.stackedWidget.setCurrentWidget(self.vistas_secundarias['imagenes']) 
        
        self.vistas_secundarias['imagenes'].show()
        
    # Aquí se añadirían métodos similares para abrir señales y tabulares...