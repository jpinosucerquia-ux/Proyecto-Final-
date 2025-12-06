# controlador/controlador_senales.py

from modelo.modelo_senales import ModeloSenales 

class ControladorSenales:
    """
    Controlador para la gestión y procesamiento de señales biomédicas (ECG/EEG).
    """
    def __init__(self, vista_senales, modelo_senales):
        self.vista = vista_senales
        self.modelo = modelo_senales
        
        # Conexión de eventos
        self.vista.ui.btn_cargar_senal.clicked.connect(self.cargar_archivo)
        self.vista.ui.btn_calcular_fft.clicked.connect(self.calcular_fft_y_mostrar)
        self.vista.ui.btn_graficar_espectro.clicked.connect(self.graficar_espectro)
        self.vista.ui.btn_calcular_desviacion.clicked.connect(self.calcular_desviacion)

    def cargar_archivo(self):
        """
        Carga el archivo .mat de la señal biomédica.
        """
        path = self.vista.abrir_dialogo_archivo()
        if path:
            self.modelo.cargar_senal(path)
            self.vista.mostrar_estado_cargado(True)
            # Opcional: Mostrar info básica de la señal cargada

    def calcular_fft_y_mostrar(self):
        """
        Calcula la FFT, guarda el CSV y actualiza la tabla de la vista.
        """
        # Llama al método del modelo que calcula, organiza en DataFrame y guarda el CSV (Requisito 5)
        df_resultados = self.modelo.aplicar_fft_y_guardar() 
        
        if df_resultados is not None:
            # Muestra el DataFrame en la QTable de la vista (Requisito 5.i)
            self.vista.mostrar_tabla_resultados(df_resultados) 
            self.vista.mostrar_mensaje("Cálculo FFT y guardado en CSV exitosos.")
        else:
            self.vista.mostrar_mensaje("Error: Señal no cargada o fallo en el cálculo FFT.")
            
    def graficar_espectro(self):
        """
        Genera y muestra el gráfico del espectro de frecuencias para un canal elegido.
        """
        canal = self.vista.ui.input_canal_elegido.text() # Asumiendo un input para el canal
        if canal:
            datos_espectro = self.modelo.obtener_espectro_canal(canal)
            if datos_espectro:
                self.vista.graficar_espectro(datos_espectro, canal) # La vista debe tener un método para incrustar el gráfico
            else:
                self.vista.mostrar_mensaje(f"Error: No se pudo obtener el espectro para el canal {canal}.")
                
    def calcular_desviacion(self):
        """
        Calcula la desviación estándar y muestra el histograma.
        """
        eje = self.vista.ui.radio_eje_elegido.checkedButton().text() # Asumiendo un selector de eje
        
        resultado_desviacion = self.modelo.calcular_desviacion_estandar(eje)
        
        # La vista genera y muestra el histograma (Requisito 5)
        self.vista.graficar_histograma(resultado_desviacion, eje)