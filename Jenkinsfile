pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt || echo "requirements not found, skipping"
                '''
            }
        }

        stage('Run Security Tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python security\\run_security_checks.py
                '''
            }
        }

        stage('Archive Security Report') {
            steps {
                archiveArtifacts artifacts: 'security_reports\\security_report.json', fingerprint: true
            }
        }

        stage('Enforce Security Gate') {
            steps {
                script {
                    def report = readJSON file: 'security_reports/security_report.json'
                    def failed = report.summary.failed
                    def risk = report.summary.risk_level

                    echo "FAILED TESTS: ${failed}"
                    echo "RISK LEVEL : ${risk}"

                    if (failed > 0) {
                        error("❌ Security tests failed — build blocked.")
                    }

                    if (risk == "HIGH") {
                        error("❌ High risk level — build blocked.")
                    }

                    echo "✔ Security checks passed."
                }
            }
        }
    }
}
