import json
import os
import mlflow
from datetime import datetime

from owasp_llm_validator import run_owasp_scan
from mlsecops_threat_analyzer import analyze_threats
from security_logger import write_security_log
from pii_scanner import scan_pii

def run_security_checks():

    mlflow.set_tracking_uri("http://127.0.0.1:5000")  # LOCAL MLflow
    mlflow.set_experiment("AI_TWIN_SECURITY_AUDIT")

    with mlflow.start_run(run_name="security_scan"):
        results = {}

        # --- 1) PII Scan ---
        pii = scan_pii("Sample input text with potential PII")
        results["pii"] = pii
        mlflow.log_metric("pii_found_count", len(pii.get("found", [])))

        # --- 2) OWASP LLM Top 10 Scan ---
        owasp_report = run_owasp_scan()
        results["owasp"] = owasp_report
        mlflow.log_metric("critical_issues", owasp_report.get("critical_issues", 0))
        mlflow.log_metric("high_issues", owasp_report.get("high_issues", 0))

        # --- 3) ML-SecOps Threat Analyzer ---
        threats = analyze_threats()
        results["threat_analysis"] = threats
        mlflow.log_metric("threat_count", threats.get("total_threats", 0))

        # --- 4) Log dosyasını üret ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = f"security_logs/security_report_{timestamp}.json"

        write_security_log(results, log_path)

        # MLflow artifact olarak ekle
        mlflow.log_artifact(log_path)

        print("Security checks completed successfully.")
        return results


if __name__ == "__main__":
    run_security_checks()
