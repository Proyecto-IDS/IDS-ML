import json
import os
import joblib
import pandas as pd

#Para las metricas:
import boto3

from src.ids_ml.attack_logic import classify_attack_state


# Ruta al modelo dentro de la imagen
MODEL_PATH = os.environ.get("MODEL_PATH", "/var/task/models/ids_rf_pipeline.joblib")



# Tabla de métricas en DynamoDB
METRICS_TABLE = os.environ.get("METRICS_TABLE", "IDS_Metrics")
# Cliente de DynamoDB
dynamo = boto3.client("dynamodb")



# Cargamos el modelo una sola vez al inicio (fuera del handler)
MODEL = joblib.load(MODEL_PATH)

# Orden de columnas EXACTO como en tu dataset/proceso de entrenamiento
FEATURE_COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land",
    "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised",
    "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells",
    "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", "count",
    "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate",
    "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
    "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
    "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate",
]

def increment_metric(name: str, inc: float = 1):
    dynamo.update_item(
        TableName=METRICS_TABLE,
        Key={"metricName": {"S": name}},
        UpdateExpression="ADD metricValue :inc",
        ExpressionAttributeValues={":inc": {"N": str(inc)}}
    )

def update_metrics(model_result: dict):
    increment_metric("TotalEvents")

    prediction = model_result.get("prediction")
    state = model_result.get("state")
    probs = model_result.get("probabilities", {})
    attack_prob = model_result.get("attack_probability")

    # Normales vs ataques
    if prediction == "normal":
        increment_metric("NormalEvents")
    else:
        increment_metric("AttackEvents")

        # Tipo de ataque: etiqueta con mayor probabilidad
        if probs:
            attack_label = max(probs, key=probs.get)  
            increment_metric(f"AttackType::{attack_label}")

    # Estado (NORMAL, CRITICO, FALSO_POSITIVO, etc.)
    if state:
        increment_metric(f"State::{state}")

    # Acumular probabilidad de ataque para calcular promedio después
    if attack_prob is not None:
        increment_metric("AttackProbabilitySum", attack_prob)
        increment_metric("AttackProbabilityCount", 1)


def _extract_features_from_event(event: dict) -> dict:

    # Caso 1: llamada directa desde backend / test
    if "features" in event and isinstance(event["features"], dict):
        return event["features"]

    # Caso 2: evento tipo API Gateway (body string o dict)
    body = event.get("body")
    if body:
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                body = {}
        if isinstance(body, dict):
            return body.get("features", {})

    # Si no encontramos nada, devolvemos dict vacío
    return {}


def lambda_handler(event, context):
    # 1) Extraer features del evento
    features = _extract_features_from_event(event)

    # Validación mínima
    if not features:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "No se encontraron 'features' en la petición."},
                ensure_ascii=False,
            ),
            "headers": {"Content-Type": "application/json"},
        }

    # 2) Construir DataFrame con orden correcto de columnas
    #    Si falta alguna columna, se rellena con 0
    row = {col: features.get(col, 0) for col in FEATURE_COLUMNS}
    X_input = pd.DataFrame([row], columns=FEATURE_COLUMNS)

    # 3) Predicción y probabilidades
    y_pred = MODEL.predict(X_input)[0]
    proba = MODEL.predict_proba(X_input)[0]
    classes = list(MODEL.classes_)
    probabilities = {cls: float(p) for cls, p in zip(classes, proba)}

    # 4) Aplicar lógica de estados + protocolos
    state_info = classify_attack_state(y_pred, probabilities) or {}

    # 5) Construir respuesta de forma segura (evitamos KeyError)
    response_body = {
        "prediction": y_pred,
        "probabilities": probabilities,
        "state": state_info.get("state"),
        "attack_probability": state_info.get("attack_probability"),
        "category": state_info.get("category"),
        "standard_protocol": state_info.get("protocol"),
    }

    try:
        update_metrics(response_body)
    except Exception as e:
        print("Error actualizando métricas:", e)

    # 6) Log para CloudWatch
    print("IDS RESULT")
    print(json.dumps(response_body, ensure_ascii=False))

    return {
        "statusCode": 200,
        "body": json.dumps(response_body, ensure_ascii=False),
        "headers": {"Content-Type": "application/json"},
    }
