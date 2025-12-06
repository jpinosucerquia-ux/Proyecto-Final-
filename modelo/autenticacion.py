import xml.etree.ElementTree as ET
import os

class ModeloUsuarios:
    def __init__(self, ruta_xml):
        self.ruta = ruta_xml
        self.usuarios = []
        self.cargar_usuarios()

    def cargar_usuarios(self):
        if not os.path.exists(self.ruta):
            print(f"Archivo no encontrado: {self.ruta}")
            return
        tree = ET.parse(self.ruta)
        root = tree.getroot()  # <users>
        for u in root.findall("user"):
            usuario = u.find("usuario").text.strip()
            contrasena = u.find("contrasena").text.strip()
            self.usuarios.append({"usuario": usuario, "contrasena": contrasena})
            
    def validar_usuario(self, usuario, contrasena):
        usuario = usuario.strip()
        contrasena = contrasena.strip()
        for u in self.usuarios:
            if u["usuario"] == usuario and u["contrasena"] == contrasena:
                return True
        return False

    

        