# controlador/controlador_historial.py
from vista.vistas_loader.vista_historial import VistaHistorial

class ControladorHistorial:
    def __init__(self, modelo):
        self.modelo = modelo # Modelo con conexión a SQL/Mongo
        self.vista = VistaHistorial()
        
        self.vista.cargar_registros_signal.connect(self.cargar_registros)
        self.vista.buscar_registro_signal.connect(self.buscar)
        
    def cargar_registros(self):
        # datos = self.modelo.obtener_todos()
        # headers = ["ID", "Usuario", "Fecha", "Actividad"]
        
        # Mock Data
        datos = [[1, "admin", "2025-12-06", "Login"], [2, "user1", "2025-12-06", "FFT"]]
        headers = ["ID", "Usuario", "Fecha", "Actividad"]
        
        self.vista.mostrar_registros(datos, headers)

    def buscar(self, texto):
        # resultados = self.modelo.buscar(texto)
        # self.vista.mostrar_registros(resultados)
        pass