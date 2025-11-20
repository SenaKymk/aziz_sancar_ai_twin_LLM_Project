pipeline {
    agent any

    environment {
        PYTHON = "python"
        VENV_DIR = ".venv"
        REQUIREMENTS = "configs/requirements.txt"
        DOTENV = ".env"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Pulling latest code..."
                git branch: 'main', url: 'https://github.com/SenaKymk/aziz_sancar_ai_twin_LLM_Project'
            }
        }

        stage('Setup Python venv') {
            steps {
                echo "🐍 Creating virtual environment..."
                sh """
                    if [ ! -d ${VENV_DIR} ]; then
                        ${PYTHON} -m venv ${VENV_DIR}
                    fi
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "📦 Installing requirements..."
                sh """
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    if [ -f ${REQUIREMENTS} ]; then
                        pip install -r ${REQUIREMENTS}
                    else
                        echo '⚠️ No requirements.txt found!'
                    fi
                """
            }
        }

        stage('Load Environment Variables') {
            steps {
                echo "🔐 Loading .env..."
                sh """
                    if [ ! -f ${DOTENV} ]; then
                        echo '⚠️ .env file not found! Using default values'
                    fi
                """
            }
        }

        stage('Run ETL Pipeline') {
            steps {
                echo "🛠 Running ETL → tools/data_warehouse.py"
                sh """
                    source ${VENV_DIR}/bin/activate
                    python tools/data_warehouse.py
                """
            }
        }

        stage('Run ML Training') {
            steps {
                echo "🤖 Training AI Twin models (train_demo.py)..."
                sh """
                    source ${VENV_DIR}/bin/activate
                    python tools/train_demo.py
                """
            }
        }

        stage('Run RAG Pipeline') {
            steps {
                echo "📚 Running RAG pipeline (rag.py)..."
                sh """
                    source ${VENV_DIR}/bin/activate
                    python tools/rag.py
                """
            }
        }

        stage('Run ML Service') {
            steps {
                echo "🌐 Starting ML Service checks (ml_service.py)..."
                sh """
                    source ${VENV_DIR}/bin/activate
                    python tools/ml_service.py --check
                """
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo "📦 Archiving model outputs..."
                archiveArtifacts artifacts: 'mlruns/**', fingerprint: true
            }
        }

    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
