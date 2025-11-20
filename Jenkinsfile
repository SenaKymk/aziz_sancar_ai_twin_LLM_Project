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

        stage('Install Basic Dependencies') {
            steps {
                echo "📦 Installing minimal dependencies..."
                bat """
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install python-dotenv requests
                """
            }
        }

        stage('Run Basic Test Script') {
            steps {
                echo "🚀 Running simple script..."
                bat """
                    venv\\Scripts\\python.exe tools\\test_run.py
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
        success {
            echo "🎉 Pipeline SUCCESS!"
        }
        failure {
            echo "❌ Pipeline Failed!"
        }
    }
}
