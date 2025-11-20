"""
security_logger.py
-------------------
Tüm güvenlik testlerinden elde edilen sonuçları ortak bir formatta toplayıp
JSON, MLflow ve Jenkins çıktısına entegre eden merkezî güvenlik kayıt sistemi.

Bu modül:
- Güvenlik testleri için standart bir output şeması oluşturur
- MLflow Security Artifact olarak raporları kaydeder
- Jenkins tarafından okunabilir JSON raporu üretir
"""

import json
import os
import mlflow
from datetime import datetime


class SecurityLogger:
    def __init__(self, report_dir="security_reports"):
        self.report_dir = report_dir
        os.makedirs(self.report_dir, exist_ok=True)

        self.report = {
            "timestamp": datetime.utcnow().isoformat(),
            "tests": [],
            "summary": {
                "passed": 0,
                "failed": 0,
                "risk_level": "UNKNOWN"
            }
        }

    def log_test_result(self, test_name: str, passed: bool, details: dict = None):
        """
        Her güvenlik testinin sonucunu ekler.

        Args:
            test_name (str): test dosyasının adı (ör. 'pii_scan')
            passed (bool): test başarısı
            details (dict): ek bilgiler (bulunan PII, adversarial örnekler vs.)
        """

        self.report["tests"].append({
            "test_name": test_name,
            "passed": passed,
            "details": details or {}
        })

        # Summary güncelle
        if passed:
            self.report["summary"]["passed"] += 1
        else:
            self.report["summary"]["failed"] += 1

        # Risk seviyesi hesaplama
        self._update_risk_level()

    def _update_risk_level(self):
        failed = self.report["summary"]["failed"]
        if failed == 0:
            self.report["summary"]["risk_level"] = "LOW"
        elif failed <= 2:
            self.report["summary"]["risk_level"] = "MEDIUM"
        else:
            self.report["summary"]["risk_level"] = "HIGH"

    def save_json(self):
        """
        Raporu JSON olarak kaydeder -> Jenkins tarafından okunabilir.
        """

        path = os.path.join(self.report_dir, "security_report.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=4)

        return path

    def log_to_mlflow(self):
        """
        MLflow'a güvenlik raporunu 'artifact' olarak yükler.
        """

        json_path = self.save_json()

        with mlflow.start_run(run_name="security_validation", nested=True):
            mlflow.log_artifact(json_path)
            mlflow.log_metric("security_tests_passed", self.report["summary"]["passed"])
            mlflow.log_metric("security_tests_failed", self.report["summary"]["failed"])
            mlflow.log_param("risk_level", self.report["summary"]["risk_level"])

        return True


# ---- KULLANIM ÖRNEĞİ ----
if __name__ == "__main__":
    logger = SecurityLogger()

    logger.log_test_result("pii_scan", passed=True)
    logger.log_test_result("adversarial_test", passed=False, details={"example": "model bypassed rule"})

    logger.save_json()
    logger.log_to_mlflow()

    print("Security report generated!")

def run_test():
    try:
        test_logger = SecurityLogger()
        test_logger.info("Security logger test message")

        # başarı = hiç exception almaması
        return True, {"status": "logger_ok"}

    except Exception as e:
        return False, {"error": str(e)}

