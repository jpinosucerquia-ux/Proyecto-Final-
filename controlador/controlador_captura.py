# controlador/controlador_captura.py
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from vista.vistas_loader.vista_captura import VistaCaptura

class ControladorCaptura:
    def __init__(self, modelo):
        self.modelo = modelo # Modelo que maneja lógica de guardado de archivos
        self.vista = VistaCaptura()
        
        self.timer = QTimer()
        self.cap = None
        self.frame_actual = None
        
        # Conexiones
        self.vista.iniciar_stream_signal.connect(self.iniciar_camara)
        self.vista.capturar_imagen_signal.connect(self.capturar_imagen)
        self.vista.guardar_temporal_signal.connect(self.guardar_imagen)
        self.vista.volver_signal.connect(self.cerrar)
        self.vista.rejected.connect(self.detener_camara) # Si cierran la ventana con X
        self.timer.timeout.connect(self.actualizar_stream)

    def iniciar_camara(self):
        self.cap = cv2.VideoCapture(0) # Requisito: Captura webcam 
        if not self.cap.isOpened():
            self.vista.mostrar_estado("Error: No se detecta cámara")
            return
        self.timer.start(30) # ~30 FPS
        self.vista.mostrar_estado("Cámara iniciada")

    def actualizar_stream(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame_actual = frame
            # Convertir a formato compatible con Qt
            imagen_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = imagen_rgb.shape
            bytes_per_line = ch * w
            q_img = QImage(imagen_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.vista.actualizar_stream(QPixmap.fromImage(q_img))

    def capturar_imagen(self):
        if self.frame_actual is not None:
            # Requisito: Convertir a escala de grises 
            gray_frame = cv2.cvtColor(self.frame_actual, cv2.COLOR_BGR2GRAY)
            
            # Mostrar preview estático
            h, w = gray_frame.shape
            q_img = QImage(gray_frame.data, w, h, w, QImage.Format_Grayscale8)
            self.vista.mostrar_imagen_capturada(QPixmap.fromImage(q_img))
            
            # Guardar en memoria temporal del controlador o modelo
            self.imagen_capturada = gray_frame 
            self.vista.mostrar_estado("Imagen capturada (Grises)")

    def guardar_imagen(self, nombre):
        if hasattr(self, 'imagen_capturada'):
            # self.modelo.guardar_imagen_temporal(self.imagen_capturada, nombre)
            print(f"Guardando {nombre}.jpg...") # Placeholder
            self.vista.mostrar_estado(f"Guardado: {nombre}")
        else:
            self.vista.mostrar_estado("Error: No hay captura")

    def detener_camara(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            
    def cerrar(self):
        self.detener_camara()
        self.vista.close()