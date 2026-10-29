pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/VineeshaVarkala/DigitalWatermarkingTool.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t digital-watermarking-tool:v1 .'
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat 'docker images digital-watermarking-tool'
            }
        }
    }

    post {
        success {
            echo 'Digital Watermarking Tool pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the Console Output for details.'
        }
    }
}
