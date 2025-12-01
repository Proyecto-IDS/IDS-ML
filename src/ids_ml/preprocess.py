import pandas as pd
import numpy as np
from typing import List

from pathlib import Path

#Definimos las primeras 41 columnas de nuestro dataset
KDD_COLUMNS_41 = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised",
    "root_shell","su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count",
    "srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate",
    "same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate"
]
#Definimos las columnas sumado a esto la etiqueta (Parte importante)
KDD_COLUMNS_LABEL = KDD_COLUMNS_41 + ["label"]
#Definimos las columnas sumado a esto la etiqueta y dificultad
KDD_COLUMNS_DIFFICULTY = KDD_COLUMNS_41 + ["label", "difficulty"]

# indica que df_no_header es de tipo pandas de Dataframe y devuelve asi mismo un DataFrame
def assign_kdd_columns(df_no_header: pd.DataFrame) -> pd.DataFrame:
    # La función shape devuelve una tubla shape[0] son filas y shape[1] son columnas
    columns = df_no_header.shape[1]
    if columns == 42:
        print("Se detecto correctamente las columnas total 42 KDD_COLUMNS_LABEL")
        df_no_header.columns = KDD_COLUMNS_LABEL
    elif columns == 43:
        print("Se detecto correctamente las columnas total 43 KDD_COLUMNS_DIFFICULTY")
        df_no_header.columns = KDD_COLUMNS_DIFFICULTY
    else:
        raise ValueError("Error al cargar el dataset, columnas incorrectas")
    
    return df_no_header

#Esta función nos va ayudar a dividir el dataframe en 2 partes
def split_features_labels(df: pd.DataFrame):
    columns_input = []
    for column_name in df.columns:
        if column_name not in ("label", "difficulty"):
            columns_input.append(column_name)
    
    #Acá colocamos todas las columnas que no son taaan importantes
    x = df[columns_input].copy()
    #Esta parte sirve para convertir las etiquetas en texto y minuscula, 
    # parte importante almacena etiqueta y dificultad
    y = df ["label"].astype(str).str.lower()

    return x,y

# En el dataset tenemos tres columnas que no son numeros, son categorias se deben codificar one-hot encoding
# devuelven una lista de strings
def kdd_categorical_columns() -> List[str]:
    return ["protocol_type", "service", "flag"]