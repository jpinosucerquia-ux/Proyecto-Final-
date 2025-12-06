# controlador/controlador_imagenes.py

from PyQt5.QtWidgets import QFileDialog
from vista.vistas_loader.vista_imagenes import VistaImagenes

class ControladorImagenes:
    def __init__(self, modelo):
        self.modelo = modelo
        self.vista = VistaImagenes()
        
        # Conexiones
        self.vista.cargar_imagen_signal.connect(self.cargar_imagen)
        self.vista.slider_axial_changed.connect(self.actualizar_axial)
        self.vista.slider_coronal_changed.connect(self.actualizar_coronal)
        self.vista.slider_sagital_changed.connect(self.actualizar_sagital)
        
    def cargar_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self.vista,
            "Abrir Imagen",
            "",
            "Archivos Médicos (*.dcm *.nii *.nii.gz *.jpg *.png)"
        )
        
        if not ruta:
            return

        # self.modelo.cargar_imagen(ruta)

        self.vista.limpiar_visualizaciones()
        self.vista.mostrar_archivo_cargado(ruta.split("/")[-1])
        self.vista.mostrar_estado("Imagen cargada exitosamente")

        # Placeholder para dimensiones reales
        # dims = self.modelo.obtener_dimensiones()
        # self.vista.Slideraxial.setMaximum(dims[0] - 1)
        # self.vista.Slidercoronal.setMaximum(dims[1] - 1)
        # self.vista.Slidersagital.setMaximum(dims[2] - 1)

    def actualizar_axial(self, indice: int):
        # slice_data = self.modelo.obtener_corte("axial", indice)
        # pix = self.convertir_a_pixmap(slice_data)
        # self.vista.actualizar_corte_axial(pix, max_value)
        pass

    def actualizar_coronal(self, indice: int):
        pass

    def actualizar_sagital(self, indice: int):
        pass
