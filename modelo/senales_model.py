import os
import numpy as np
import pandas as pd
from scipy.io import loadmat

class ModeloSenales:

    def __init__(self):
        self.senal = None
        self.fs = None  # frecuencia de muestreo

    # -----------------------------
    # Cargar archivo .mat
    # -----------------------------
    def cargar_senal(self, ruta):
        data = loadmat(ruta)

        # Asume que hay una variable principal
        self.senal = data[list(data.keys())[-1]]
        self.fs = 250  # si no viene en archivo

        return self.senal

    # -----------------------------
    # FFT por canal
    # -----------------------------
    def aplicar_fft(self):
        resultados = []

        for canal in range(self.senal.shape[0]):
            y = self.senal[canal, :]
            N = len(y)

            freqs = np.fft.rfftfreq(N, d=1/self.fs)
            fft_vals = np.abs(np.fft.rfft(y))

            idx_max = np.argmax(fft_vals)
            frecuencia_dom = freqs[idx_max]
            magnitud = fft_vals[idx_max]

            resultados.append([canal, frecuencia_dom, magnitud])

        df = pd.DataFrame(resultados, columns=["Canal", "FrecuenciaDominante", "Magnitud"])
        return df

    # -----------------------------
    # Guardar CSV
    # -----------------------------
    def guardar_fft_csv(self, df, ruta):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        df.to_csv(ruta, index=False)

    # -----------------------------
    # Histograma (std por eje)
    # -----------------------------
    def desviacion_estandar(self, eje=1):
        return np.std(self.senal, axis=eje)
