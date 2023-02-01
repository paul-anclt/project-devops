pipeline {
    agent any

	environment {
        DOCKERHUB_CREDENTIALS=credentials('dockerhub-pancele')
        WEBHOOK_URL=credentials('discord_webhook_url')
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
                script {
                    app = docker.build("$myimage")
                }
                //sh 'docker build -t $myimage .'
            }
        }
        stage('Test') {
            steps {
                script {
                    app.inside {
                        sh 'python3 test.py'
                    }
                }
            }
        }
        stage('Push on docker hub') {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                //sh "docker push $myimage"
                script {
                    app.push()        
                }
            }
        }
        stage('Deploy DEV') {
            steps {
                /* Deploy a container for dev (ensuring to stop and remove it first) */
                sh 'docker ps -f name=^dev$ -q | xargs --no-runif-empty docker container stop'
                sh 'docker container ls -a -fname=^dev$ -q |xargs -r docker container rm'
                script {
                    app.run('--restart always --name dev -p 5000:5000') 
                }
            }
        }
        stage('Testing DEV') {
            steps {
                echo 'TODO: Do some tests....'
            }
        }
        stage('Deploy PROD') {
            steps {
                /* Deploy a container for PROD */
                sh 'docker ps -f name=^prod$ -q | xargs --no-run-ifempty docker container stop'
                sh 'docker container ls -a -fname=^prod$ -q | xargs -r docker container rm'
                script {
                    app.run('--restart always --name prod -p 5001:5000') 
                }
            }
        }
        stage('Testing PROD') {
            steps {
                echo 'TODO: Do some tests....'
            }
        }
        stage('Discord Notification'){
            steps {
                discordSend description: "Jenkins Pipeline Build", footer: "Footer Text", link: env.BUILD_URL, result: currentBuild.currentResult, title: JOB_NAME, webhookURL: "$WEBHOOK_URL"
            }
        }
    }
}