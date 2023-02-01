pipeline {
    agent any

	environment {
        DOCKERHUB_CREDENTIALS=credentials('dockerhub-pancele')
        def myimage = "pancele/simple-flask-app"
	}
    stages {


        stage('Clone repository') {
            steps {
                checkout scm
            }
        }
        stage('Building') {
            steps {
                sh 'docker build -t $myimage .'
            }
        }
        stage('Test') {
            steps {
                echo 'Test'
            }
        }
        stage('Push on docker hub') {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                sh "docker push $myimage"            
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