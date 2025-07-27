pipeline {
    agent any

    triggers {
        githubPush() // 👈 This tells Jenkins to run on every GitHub push (enabled by webhook)
    }

    stages {
        stage('Preparation') {
            steps {
                echo "Cleaning workspace..."
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                checkout scm
            }
        }

        stage('Build & Run') {
            steps {
                echo "Running ETL script..."
                sh 'chmod +x run_etl.sh'
                sh './run_etl.sh'
            }
        }
    }

    post {
        failure {
            echo 'Build failed!'
        }
        success {
            echo 'Build succeeded!'
        }
    }
}
