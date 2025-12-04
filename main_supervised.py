import pandas as pd
# Traemos las rutas de lso datasets desde los path
from src.ids_ml.config import NSLKDD_Train, NSLKDD_Test, NSLKDD_Processed
#Importamos el metodo
from src.ids_ml.preprocess import assign_kdd_columns

if __name__ == "__main__":
    
    #Importamos dataset de entrenamiento y prueba, ademas colocamos mensajes para ver el flujo
    df_train = pd.read_csv(NSLKDD_Train, header=None, engine="python")
    df_train = assign_kdd_columns(df_train)
    print ("\nSe leyó el dataset de entrenamiento")

    df_test = pd.read_csv(NSLKDD_Test, header=None, engine="python")
    df_test = assign_kdd_columns(df_test)
    print ("\nSe leyó el dataset de prueba")

    # Unimos todo en un unico dataset
    df_all = pd.concat([df_train, df_test], ignore_index=True)

    #Filas y columnas
    print("\nDimensiones (filas, columnas):", df_all.shape)

    #Verificamos que el nombre si se asigne a la columna correspondiente
    print("\nPrimeras 5 filas:")
    print(df_all.head(5))

    #Verificamos las etiquetas y cantidades
    print("\nDistribución de clases (label):")
    print(df_all['label'].astype(str).str.lower().value_counts().head(30))

    NSLKDD_Processed.parent.mkdir(parents=True, exist_ok=True)
    df_all.to_csv(NSLKDD_Processed, index=False)
    print(f"\nCSV procesado guardado en: {NSLKDD_Processed}")