# controlador/controlador_tabulares.py

from modelo.modelo_tabulares import ModeloTabulares

class ControladorTabulares:
    """
    Controlador para la gestión y análisis de datos tabulares (CSV).
    """
    def __init__(self, vista_tabulares, modelo_tabulares):
        self.vista = vista_tabulares
        self.modelo = modelo_tabulares
        
        # Conexión de eventos
        self.vista.ui.btn_cargar_csv.clicked.connect(self.cargar_archivo)
        self.vista.ui.btn_graficar_columnas.clicked.connect(self.graficar_columnas)

    def cargar_archivo(self):
        """
        Carga el archivo CSV y muestra los datos en la QTable de la interfaz.
        """
        path = self.vista.abrir_dialogo_archivo()
        if path:
            df = self.modelo.cargar_csv(path)
            
            if df is not None:
                # Muestra los datos cargados en el área QTable (Requisito 6)
                self.vista.mostrar_datos_en_tabla(df) 
                
                # Permite al usuario seleccionar columnas para graficar
                self.vista.actualizar_selector_columnas(df.columns)
            else:
                self.vista.mostrar_mensaje("Error: No se pudo cargar el archivo CSV.")

    def graficar_columnas(self):
        """
        Obtiene las 4 columnas seleccionadas por el usuario y genera gráficos tipo plot.
        """
        # Asumiendo que la vista tiene un método para obtener las selecciones
        columnas_seleccionadas = self.vista.obtener_columnas_seleccionadas() 
        
        if len(columnas_seleccionadas) >= 1: # Mínimo 1 para graficar
            for columna in columnas_seleccionadas:
                # Obtiene los datos de la columna específica
                datos_columna = self.modelo.obtener_datos_columna(columna)
                
                # La vista debe tener un área donde incrustar el gráfico tipo plot (Requisito 6)
                self.vista.graficar_plot_individual(columna, datos_columna)
        else:
            self.vista.mostrar_mensaje("Seleccione al menos una columna para graficar.")