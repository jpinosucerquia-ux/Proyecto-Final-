# controlador/controlador_imagenes.py

# Importar el Modelo de Imágenes
from modelo.modelo_imagenes import ModeloImagenes 

class ControladorImagenes:
    """
    Controlador para la gestión y procesamiento de imágenes médicas/generales.
    """
    def __init__(self, vista_imagenes, modelo_imagenes):
        self.vista = vista_imagenes
        self.modelo = modelo_imagenes
        
        # Conexión de botones y sliders
        self.vista.ui.btn_cargar_imagen.clicked.connect(self.cargar_archivo)
        self.vista.ui.slider_axial.valueChanged.connect(self.actualizar_corte_axial)
        
        # Conexión para el procesamiento de JPG/PNG
        self.vista.ui.btn_binarizar.clicked.connect(self.binarizar_imagen)

    def cargar_archivo(self):
        """
        Abre un diálogo para seleccionar el archivo y lo envía al Modelo.
        """
        path = self.vista.abrir_dialogo_archivo()
        if path:
            datos_imagen = self.modelo.cargar_imagen(path)
            
            if datos_imagen:
                # Si es DICOM/NIFTI, mostrar cortes.
                if self.modelo.es_imagen_medica(path):
                    self.vista.mostrar_cortes_iniciales(datos_imagen)
                    self.modelo.extraer_metadata_y_guardar(datos_imagen) # Requisito 4
                
                # Si es JPG/PNG, cargar la imagen base para procesamiento.
                else:
                    self.vista.mostrar_imagen_base(datos_imagen)
                    
    def actualizar_corte_axial(self, valor):
        """
        Actualiza la visualización del corte axial basada en el slider.
        """
        corte = self.modelo.obtener_corte_axial(valor)
        self.vista.actualizar_visualizador(corte, 'axial')
        
    def binarizar_imagen(self):
        """
        Aplica el procesamiento de binarización si la imagen es JPG/PNG.
        """
        imagen_procesada = self.modelo.procesar_imagen('binarizar')
        self.vista.mostrar_imagen_procesada(imagen_procesada)