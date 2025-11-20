pipeline {
    agent any

    environment {
        PYTHON = "${WORKSPACE}\\venv\\Scripts\\python.exe"
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
                echo "🐍 Creating virtual environment (Windows)..."
                bat """
                    python -m venv venv
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "📦 Installing dependencies..."
                bat """
                    ${PYTHON} -m pip install --upgrade pip
                    ${PYTHON} -m pip install -r requirements.txt
                """
            }
        }

        stage('Load Environment Variables') {
            steps {
                echo "🔐 Loading .env file..."
                bat """
                    type .env
                """
            }
        }

        stage('Run RAG Pipeline') {
            steps {
                echo "📚 Running RAG system..."
                bat """
                    ${PYTHON} tools\\rag.py
                """
            }
        }

        stage('Run ML Service') {
            steps {
                echo "🤖 Running ML Service..."
                bat """
                    ${PYTHON} tools\\ml_service.py
                """
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: '**/*.log', allowEmptyArchive: true
            }
        }
    }

    post {
        failure {
            echo "❌ Pipeline failed!"
        }
        success {
            echo "🎉 Pipeline executed successfully!"
        }
    }
}
