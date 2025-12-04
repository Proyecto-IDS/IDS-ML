import joblib
import pandas as pd
import numpy as np
from pathlib import Path

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, label_binarize
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
    average_precision_score,
    log_loss,
    matthews_corrcoef,
    balanced_accuracy_score,
)

# Importamos el dataset procesado
from src.ids_ml.config import NSLKDD_Processed
from src.ids_ml.preprocess import split_features_labels, kdd_categorical_columns

if __name__ == "__main__":
    print("Mensaje de control: Entrenamiento supervisado Random Forest")

    # leemos el dataset procesado
    df = pd.read_csv(NSLKDD_Processed)

    # LLamos la función que divide en 2 el dataset
    X, y = split_features_labels(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,              # variables de entrada
        y,              # etiquetas (clases)
        test_size=0.2,  # 20% para test
        stratify=y,     # mantener proporciones de clases
        random_state=50 # reproducibilidad
    )

    #Llamamos la función donde tenemos las variables categoricas
    categorical_cols = kdd_categorical_columns()

    #ColumnTransformer sirve para hacer transformaciones de columnas de forma ordenada
    #OneHotEncoder transforma el texto en numeros binarios
        #handle_unknown="ignore" El codificador ignora la nueva categoría y coloca simplemente ceros
        #sparse_output=False OneHot devuelve una matriz perso solo los 1 que es dificil de leer con ese parametro tambien guarda los 0
    preprocessor = ColumnTransformer(
        transformers=[
            ("categorics", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),],
        #remainder sirve para los demas atributos que no se transforman
            #drop = elimina columas
            #passthrough = deja las columnas sin cambios
        remainder="passthrough",
        #Controla cuantos nucleos del procesador se usan en paralelo
        #none = un solo nucleo
        #-1 = todos los nucleos
        #4= exactamente 4 nucleos
        n_jobs=None
    )

    #Definimos el algoritmo a utilizar en este caso random forest
    algoritmo = RandomForestClassifier(
        #definimos el numero de arboles entre mas mejora la presiciónhasta sirto punto 
        n_estimators=300,
        #Evita el sesgo a las clases pequeñas, tiene opciones como none cuando esta 50 50 o definir manualmente los pesos
        class_weight="balanced",
        #Utiliza todos los nucleos para entrenar el modelo
        n_jobs=-1,
        #Semilla para la creacion
        random_state=50
    )

    #Primero hacemos el preprocesamiento y luego el algoritmo
    pipe = Pipeline(steps=[("prep", preprocessor),("rf", algoritmo)])

    #Entrenamos el modelo, las cariables salen de train_test_split
    pipe.fit(X_train, y_train)
    print("Modelo entrenado")



    #Vamos a evaluar las metricas del modelo
    #Predice las etiquetas para el conjunto de prueba
    y_pred = pipe.predict(X_test)
    # Calcula el accuracy que es precision global
    accuracy = accuracy_score(y_test, y_pred)
    # Calcula el f1 score que es una media ponderada de precision y recall
    #opciones en el overage:
        # micro = metrica global sumando los totales de la matriz, se hace cuando sta equilibrado
        #macro= cuando todas las clases tienen el mismo peso
        #weighted= cada clase tiene un peso segun su proporcion en el dataset
        # samples= Se usa cuando determinada muestra puede tener multiples etiquetas
        # None= devuelve el f1 score para cada clase por separado
    f1 = f1_score(y_test, y_pred, average="macro")

    # Precision y recall macro
    precision_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
    recall_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)

    # Balanced accuracy
    balanced_acc = balanced_accuracy_score(y_test, y_pred)

    # Matthews correlation coefficient
    mcc = matthews_corrcoef(y_test, y_pred)

    # Intentamos calcular probabilidades para métricas basadas en score (ROC-AUC, PR-AUC, log-loss)
    y_proba = None
    try:
        y_proba = pipe.predict_proba(X_test)
    except Exception:
        # Si el estimador no soporta predict_proba, dejamos como None
        y_proba = None

    roc_auc_macro = None
    roc_auc_micro = None
    avg_precision_macro = None
    avg_precision_micro = None
    logloss = None
    if y_proba is not None:
        # obtener orden de clases que devuelve predict_proba
        try:
            clf_classes = pipe.named_steps['rf'].classes_
        except Exception:
            clf_classes = np.unique(y_test)

        # Binarizar etiquetas para multiclass
        try:
            y_test_bin = label_binarize(y_test, classes=clf_classes)
            # ROC AUC (soporta multiclass con multi_class='ovr')
            roc_auc_macro = roc_auc_score(y_test_bin, y_proba, average='macro', multi_class='ovr')
            roc_auc_micro = roc_auc_score(y_test_bin, y_proba, average='micro', multi_class='ovr')

            # Average precision (PR AUC)
            avg_precision_macro = average_precision_score(y_test_bin, y_proba, average='macro')
            avg_precision_micro = average_precision_score(y_test_bin, y_proba, average='micro')

            # Log loss
            logloss = log_loss(y_test, y_proba, labels=clf_classes)
        except Exception:
            # Si falla (p.ej. shapes incompatibles), dejamos valores None
            roc_auc_macro = roc_auc_micro = avg_precision_macro = avg_precision_micro = logloss = None

    top_classes = y_test.value_counts().head(15).index.tolist()

    # Matriz de confusion (para todas las clases y para top 15)
    all_classes = np.unique(y_test)
    cm_all = confusion_matrix(y_test, y_pred, labels=all_classes)
    matrix = confusion_matrix(y_test, y_pred, labels=top_classes)

    # Especificidad (True Negative Rate) por clase (todas las clases)
    specificity_per_class = {}
    total = cm_all.sum()
    for i, cls in enumerate(all_classes):
        TP = cm_all[i, i]
        FP = cm_all[:, i].sum() - TP
        FN = cm_all[i, :].sum() - TP
        TN = total - TP - FP - FN
        denom = TN + FP
        specificity = float(TN) / denom if denom > 0 else np.nan
        specificity_per_class[str(cls)] = specificity


    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"F1-macro: {f1:.4f}")
    print(f"Precision-macro: {precision_macro:.4f}")
    print(f"Recall-macro: {recall_macro:.4f}")
    print(f"Balanced accuracy: {balanced_acc:.4f}")
    print(f"MCC: {mcc:.4f}")
    if roc_auc_macro is not None:
        print(f"ROC-AUC macro: {roc_auc_macro:.4f}, micro: {roc_auc_micro:.4f}")
        print(f"PR-AUC (avg precision) macro: {avg_precision_macro:.4f}, micro: {avg_precision_micro:.4f}")
    if logloss is not None:
        print(f"Log-loss: {logloss:.4f}")
    print("\nMatriz de confusión (parcial, top 15 clases en y_test):")
    print("Orden de etiquetas:", top_classes)
    print(matrix)

    #Creamos el objeto de tipo path para guardar el modelo
    models_dir = Path("models")
    #crea la carpeta models, si falta directorios los crea y si ya existe no da error
    models_dir.mkdir(parents=True, exist_ok=True)
    #Construye la ruta completa del archivo dentro de models, usando el operador / de pathlib
    model_path = models_dir / "ids_rf_pipeline.joblib"
    #joblib Es la forma recomendada para serializar modelos de scikit-learn
    joblib.dump(pipe, model_path)
    print(f"\nModelo guardado en: {model_path}")

    print("COMPLETADO EL ENTRENAMIENTO RDFOREST")

    #__________________________________
    #Esto no es del modelo pero es para el reporte final
    reporte = classification_report(y_test, y_pred, zero_division=0)
    print("\nReporte de clasificación completo:")
    with open("models/classification_report.txt", "w", encoding="utf-8") as f:
        f.write("=== MÉTRICAS GENERALES ===\n")
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"Precision-macro: {precision_macro:.4f}\n")
        f.write(f"Recall-macro: {recall_macro:.4f}\n")
        f.write(f"F1-macro: {f1:.4f}\n")
        f.write(f"Balanced accuracy: {balanced_acc:.4f}\n")
        f.write(f"MCC: {mcc:.4f}\n")
        if roc_auc_macro is not None:
            f.write(f"ROC-AUC macro: {roc_auc_macro:.4f}, micro: {roc_auc_micro:.4f}\n")
            f.write(f"PR-AUC (avg precision) macro: {avg_precision_macro:.4f}, micro: {avg_precision_micro:.4f}\n")
        if logloss is not None:
            f.write(f"Log-loss: {logloss:.4f}\n")
        f.write("\n=== REPORTE DE CLASIFICACIÓN ===\n")
        f.write(reporte)
        f.write("\n\n=== MATRIZ DE CONFUSIÓN (Top 15 clases) ===\n")
        np.savetxt(f, matrix, fmt="%d")
        f.write("\n\n=== MATRIZ DE CONFUSIÓN (Todas las clases) ===\n")
        np.savetxt(f, cm_all, fmt="%d")
        f.write("\n\n=== ESPECIFICIDAD POR CLASE ===\n")
        for cls, spec in specificity_per_class.items():
            f.write(f"{cls}: {spec:.4f}\n")

    plt.figure(figsize=(10,8))
    sns.heatmap(matrix, annot=True, fmt='d', xticklabels=top_classes, yticklabels=top_classes, cmap="Blues")
    plt.xlabel("Predicho")
    plt.ylabel("Real")
    plt.title("Matriz de Confusión - Random Forest")
    plt.tight_layout()
    plt.savefig("models/confusion_matrix.png")
    plt.close()
    print("Imagen de matriz guardada en: models/confusion_matrix.png")