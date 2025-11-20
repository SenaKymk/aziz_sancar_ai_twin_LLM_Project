# FILE: pii_scan.py
# PURPOSE:
#   Eğitim ve inference verilerinde PII (kişisel veriler)
#   olup olmadığını tarar. Kişisel veri bulgularını
#   MLflow tag'lerine yazar. MLSecOps & OWASP (LLM05: Sensitive Information Leakage)
#   uyumluluğu için zorunlu kontroldür.
# --------------------------------------------------------
import os
import mlflow

def scan_pii(folder):
    suspicious_keywords = ["tc", "kimlik", "adres", "telefon", "mail"]
    findings = []

    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".txt") or f.endswith(".csv") or f.endswith(".json"):
                path = os.path.join(root, f)
                with open(path, "r", errors="ignore") as file:
                    content = file.read().lower()
                    for key in suspicious_keywords:
                        if key in content:
                            findings.append((f, key))

    return findings if findings else "NO_PII_FOUND"


if __name__ == "__main__":
    result = scan_pii("data/")
    print("PII Scan Result:", result)
    mlflow.set_tag("pii_scan_result", str(result))

def run_test():
    try:
        results = scan_pii("This is a test string with no PII.")
        passed = len(results.get("found", [])) == 0
        return passed, results
    except Exception as e:
        return False, {"error": str(e)}
