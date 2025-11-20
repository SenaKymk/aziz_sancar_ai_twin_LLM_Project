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
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Security Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python security/run_security_checks.py
                '''
            }
        }

        stage('Archive Security Report') {
            steps {
                archiveArtifacts artifacts: 'security_reports/security_report.json', fingerprint: true
            }
        }

        stage('Enforce Security Gate') {
            steps {
                script {

                    def report = readJSON file: 'security_reports/security_report.json'
                    def failedTests = report.summary.failed
                    def riskLevel = report.summary.risk_level

                    echo "Failed Tests : ${failedTests}"
                    echo "Risk Level   : ${riskLevel}"

                    if (failedTests > 0) {
                        error("❌ Security tests FAILED. Blocking deployment.")
                    }

                    if (riskLevel == "HIGH") {
                        error("❌ Model Risk Level = HIGH → build blocked.")
                    }

                    echo "✔ Security tests passed. Proceeding."
                }
            }
        }
    }
}
