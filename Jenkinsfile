
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'viineesha1263/digital-watermarking-tool'
        IMAGE_TAG = 'v1'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/VineeshaVarkala/DigitalWatermarkingTool.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

        stage('Login and Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    bat '''
                        @echo off
                        echo %DOCKER_TOKEN% | docker login -u "%DOCKER_USER%" --password-stdin
                        if errorlevel 1 exit /b 1

                        docker push %IMAGE_NAME%:%IMAGE_TAG%
                        if errorlevel 1 exit /b 1

                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Digital Watermarking Tool image published successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output for details.'
        }
    }
}
