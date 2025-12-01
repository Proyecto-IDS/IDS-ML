# Archivo centralk para definir las rutas y nombres que se van a utilizar

from pathlib import Path

# _file_ es una variable interna que almacena la ruta del archivo actual en este caso config.py
# Path(_file_) Convierte la ruta en objeto path para la manipulación de las carpetas
# .resolve() ayuda a normalizar la ruta esi quire decir que si hay .. los resuelve
# el .parents[2] sube dos niveles de carpetas eso quiere decir hasta /IDS_MachineLearning
# por lo tanto la salida es C:\Users\ivans\OneDrive\Escritorio\IDS_MachineLearning

Ruta_AbsolutaBase = Path(__file__).resolve().parents[2]

#Definimos las rutas donde esta la información desde el browser y la procesada
Data_Cruda = Ruta_AbsolutaBase / "data" / "raw"
Data_Procesada = Ruta_AbsolutaBase / "data" / "processed"

#Definimos las rutas necesarias para el entrenamientod del modelo supervisad
NSLKDD_Dataset = Data_Cruda / "nslkdd"

#Definimos los archivos
NSLKDD_Train = NSLKDD_Dataset / "KDDTrain+.txt"
NSLKDD_Test = NSLKDD_Dataset / "KDDTest+.txt"

# Guardamos el dataset procesado que es el que va a utilizar el modelo
NSLKDD_Processed = Data_Procesada / "nslkdd_processed.csv"