pipeline {
    agent any

    environment {
        PYTHON = "venv\\Scripts\\python.exe"
    }

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

        stage('Install Dependencies') {
            steps {
                echo "📦 Installing dependencies..."
                bat """
                    ${PYTHON} -m pip install --upgrade pip
                    ${PYTHON} -m pip install python-dotenv requests mlflow
                """
            }
        }

        stage('Run MLSecOps Suite') {
            steps {
                echo "🔐 Running Security Checks (MLSecOps + OWASP)..."
                bat """
                    ${PYTHON} security\\run_security_checks.py
                """
            }
        }

        stage('Archive Security Logs') {
            steps {
                echo "📁 Archiving generated logs..."
                archiveArtifacts artifacts: 'security_logs/*.json', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo "🎉 Security Pipeline SUCCESS!"
        }
        failure {
            echo "❌ Pipeline Failed!"
        }
    }
}
