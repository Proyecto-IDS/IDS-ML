import joblib
import pandas as pd
from src.ids_ml.attack_logic import classify_attack_state

MODEL_PATH = "models/ids_rf_pipeline.joblib"
MODEL = joblib.load(MODEL_PATH)

FEATURE_COLUMNS = [
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

sample = {
    "duration": 0,
    "protocol_type": "tcp",
    "service": "http",
    "flag": "SF",
    "src_bytes": 220,
    "dst_bytes": 0,
    "land": 0,
    "wrong_fragment": 0,
    "urgent": 0,
    "hot": 0,
    "num_failed_logins": 0,
    "logged_in": 0,
    "num_compromised": 0,
    "root_shell": 0,
    "su_attempted": 0,
    "num_root": 0,
    "num_file_creations": 0,
    "num_shells": 0,
    "num_access_files": 0,
    "num_outbound_cmds": 0,
    "is_host_login": 0,
    "is_guest_login": 0,
    "count": 30,
    "srv_count": 28,
    "serror_rate": 0.0,
    "srv_serror_rate": 0.0,
    "rerror_rate": 0.0,
    "srv_rerror_rate": 0.0,
    "same_srv_rate": 1.0,
    "diff_srv_rate": 0.0,
    "srv_diff_host_rate": 0.0,
    "dst_host_count": 255,
    "dst_host_srv_count": 25,
    "dst_host_same_srv_rate": 0.98,
    "dst_host_diff_srv_rate": 0.02,
    "dst_host_same_src_port_rate": 0.0,
    "dst_host_srv_diff_host_rate": 0.0,
    "dst_host_serror_rate": 0.0,
    "dst_host_srv_serror_rate": 0.0,
    "dst_host_rerror_rate": 0.0,
    "dst_host_srv_rerror_rate": 0.0
}





def predict_local(features):
    df = pd.DataFrame([features], columns=FEATURE_COLUMNS)

    pred = MODEL.predict(df)[0]
    proba = MODEL.predict_proba(df)[0]
    classes = MODEL.classes_

    probabilities = {cls: float(prob) for cls, prob in zip(classes, proba)}

    state_info = classify_attack_state(pred, probabilities)

    print("\nRESULTADOS")
    print("Predicción:", pred)
    print("Probabilidad:", probabilities.get(pred))
    print("Estado:", state_info["state"])
    print("Categoría:", state_info["category"])
    print("Protocolo:\n", state_info["protocol"])

if __name__ == "__main__":
    predict_local(sample)
