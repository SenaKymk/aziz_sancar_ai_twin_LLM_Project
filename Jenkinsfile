pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Pulling latest code..."
                checkout scm
            }
        }

        stage('Setup Python venv') {
            steps {
                echo "🐍 Creating virtual environment..."
                bat "python -m venv venv"
            }
        }

        stage('Install Required Dependencies') {
            steps {
                echo "📦 Installing dependencies..."
                bat """
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install python-dotenv mlflow
                """
                // SECOPS modülleri
                bat """
                    venv\\Scripts\\python.exe -m pip install colorama
                """
            }
        }

        stage('Run Security Tests') {
            steps {
                echo "🛡️ Running OWASP + MLSecOps security suite..."
                bat """
                    venv\\Scripts\\python.exe security\\run_security_checks.py
                """
            }
        }

        stage('Archive Security Logs') {
            steps {
                archiveArtifacts artifacts: 'security_logs/*.json', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo "🎉 SECURITY PIPELINE SUCCESS!"
        }
        failure {
            echo "❌ SECURITY PIPELINE FAILED!"
        }
    }
}
