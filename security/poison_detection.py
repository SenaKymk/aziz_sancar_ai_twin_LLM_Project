# --------------------------------------------------------
# FILE: poison_detection.py
# PURPOSE:
#   Bu script, eğitim verilerinde "data poisoning" yani
#   bilerek eklenmiş zararlı, yanlış yönlendirici veya
#   model davranışını bozmaya yönelik örnekleri tespit etmek için
#   basit istatistiksel anomaly detection uygular.
#
#   MLSecOps & OWASP-LLM (LLM04: Model Poisoning) maddesine
#   direkt uyumluluk sağlar.
#
#   Tespit sonuçları MLflow'a tag olarak yazılır.
# --------------------------------------------------------

import os
import mlflow
import numpy as np

def simple_anomaly_detection(folder):
    lengths = []

    # Eğitim datasetindeki metinlerin uzunluk dağılımını çıkarıyoruz.
    # Çok aşırı kısa/uzun veya normdan sapmış içerikler zehirlenmiş olabilir.
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".txt"):
                path = os.path.join(root, f)
                with open(path, "r", errors="ignore") as file:
                    content = file.read()
                    lengths.append(len(content))

    if not lengths:
        return "NO_DATA"

    lengths = np.array(lengths)
    mean = lengths.mean()
    std = lengths.std()

    # Basit anomaly rule:
    # Eğer bir dosya uzunluğu mean ± 3*std dışındaysa şüpheli sayıyoruz.
    anomalies = []
    for l in lengths:
        if abs(l - mean) > 3 * std:
            anomalies.append(int(l))

    return anomalies if anomalies else "NO_POISON_DETECTED"


if __name__ == "__main__":
    result = simple_anomaly_detection("data/")
    print("Poison Detection Result:", result)
    mlflow.set_tag("poison_detection", str(result))

def run_test():
    try:
        report = detect_poisoning("test sample")
        passed = report.get("poison_detected") is False
        return passed, report
    except Exception as e:
        return False, {"error": str(e)}
