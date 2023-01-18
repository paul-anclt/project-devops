pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Building') {
            steps {
                echo 'Building....'
            }
        }
        stage('Push on docker hub') {
            steps {
                echo 'Pushing on docker hub....'
            }
        }
        stage('Deploy DEV') {
            steps {
                echo 'Deploying DEV....'
            }
        }
        stage('Deploy PROD') {
            steps {
                echo 'Deploying PROD....'
            }
        }
    }
}