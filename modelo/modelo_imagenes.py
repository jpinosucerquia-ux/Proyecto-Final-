import os
import csv
import pydicom
import numpy as np
import cv2
import nibabel as nib

class ModeloImagenes:

    def __init__(self):
        self.imagen = None
        self.metadata = {}

    # ------------------------
    # Cargar archivos médicos
    # ------------------------
    def cargar_imagen(self, ruta):
        ext = ruta.lower()

        if ext.endswith(".dcm"):
            ds = pydicom.dcmread(ruta)
            self.metadata = self._extraer_metadata_dicom(ds)
            self.imagen = self._convertir_hounsfield(ds)

        elif ext.endswith(".nii") or ext.endswith(".nii.gz"):
            nii = nib.load(ruta)
            self.imagen = nii.get_fdata()
            self.metadata = {"tipo": "NIFTI"}

        elif ext.endswith(".png") or ext.endswith(".jpg"):
            img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
            self.imagen = img
            self.metadata = {"tipo": "imagen convencional"}

        else:
            raise ValueError("Formato no soportado")

        return self.imagen, self.metadata

    # ------------------------------------
    # Extraer metadata para CSV (parcial)
    # ------------------------------------
    def _extraer_metadata_dicom(self, ds):
        meta = {}

        tags = {
            "PatientID": "ID Paciente",
            "PatientName": "Nombre",
            "StudyDate": "Fecha",
            "Modality": "Modalidad",
            "StudyDescription": "Descripción"
        }

        for key, nombre in tags.items():
            valor = getattr(ds, key, "No disponible")
            meta[nombre] = str(valor)

        return meta

    # -----------------------------------
    # Convertir a Hounsfield si es CT
    # -----------------------------------
    def _convertir_hounsfield(self, ds):
        img = ds.pixel_array.astype(np.int16)

        slope = getattr(ds, "RescaleSlope", 1)
        intercept = getattr(ds, "RescaleIntercept", 0)

        return img * slope + intercept

    # --------------------------
    # Generar cortes 3D
    # --------------------------
    def obtener_corte_axial(self, index):
        return self.imagen[index, :, :]

    def obtener_corte_sagital(self, index):
        return self.imagen[:, :, index]

    def obtener_corte_coronal(self, index):
        return self.imagen[:, index, :]

    # --------------------------
    # Procesamiento básico
    # --------------------------
    def normalizar(self):
        img = self.imagen.astype(np.float32)
        img = (img - np.min(img)) / (np.max(img) - np.min(img))
        self.imagen = (img * 255).astype(np.uint8)
        return self.imagen

    def filtrar_gauss(self):
        self.imagen = cv2.GaussianBlur(self.imagen, (5, 5), 0)
        return self.imagen

    def binarizar(self, umbral=128):
        _, self.imagen = cv2.threshold(self.imagen, umbral, 255, cv2.THRESH_BINARY)
        return self.imagen

    def detectar_bordes(self):
        self.imagen = cv2.Canny(self.imagen, 50, 150)
        return self.imagen

    # --------------------------
    # Guardar metadata en CSV
    # --------------------------
    def guardar_metadata_csv(self, ruta_csv):
        os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)

        with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Campo", "Valor"])
            for k, v in self.metadata.items():
                writer.writerow([k, v])

