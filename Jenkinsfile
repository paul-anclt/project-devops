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
                    app.push("$currentBuild.number")        
                }
            }
        }
        stage('Deploy DEV') {
            steps {
                /* Deploy a container for dev (ensuring to stop and remove it first) */
                sh 'docker ps -f name=^dev$ -q | xargs --no-run-if-empty docker container stop'
                sh 'docker container ls -a -fname=^dev$ -q |xargs -r docker container rm'
                script {
                    app.run('--restart always --name dev -p 5000:5000') 
                }
            }
        }
        stage('Testing DEV') {
            steps {
                script {
                    final String ipDev = sh(script: 'docker inspect -f \'{{ .NetworkSettings.IPAddress }}\' dev', returnStdout: true).trim()

                    final String urlDev = "${ipDev}:5000"
                    //final String response = sh(script: "curl -Is $urlDev", returnStdout: true).trim()
                    //echo response

                    final String scriptDev = "curl -Is $urlDev | head -n 1 | awk '{print \$2}'"
                    
                    HealthCheck = sh( script: "$scriptDev", returnStdout: true ).trim()
        
                    if (HealthCheck.equals("200")) {
                    
                    } else {
                        sh "echo ERROR ${HealthCheck} ; exit 1" // this fails the stage
                    }
                    
                }
            }
        }
        stage('Deploy PROD') {
            steps {
                /* Deploy a container for PROD */
                sh 'docker ps -f name=^prod$ -q | xargs --no-run-if-empty docker container stop'
                sh 'docker container ls -a -fname=^prod$ -q | xargs -r docker container rm'
                script {
                    app.run('--restart always --name prod -p 5001:5000') 
                }
            }
        }
        stage('Testing PROD') {
            steps {
                script {
                    final String ipProd = sh(script: 'docker inspect -f \'{{ .NetworkSettings.IPAddress }}\' prod', returnStdout: true).trim()

                    final String urlProd = "${ipProd}:5000"

                    final String scriptProd = "curl -Is $urlProd | head -n 1 | awk '{print \$2}'"
                    
                    HealthCheck = sh( script: "$scriptProd", returnStdout: true ).trim()
                    if (HealthCheck.equals("200")) {
                    
                    } else {
                        sh "echo ERROR ${HealthCheck} ; exit 1" // this fails the stage
                    }
                }
            }
        }
    }
    post {
        always {
            discordSend description: "Jenkins Pipeline Build N°$currentBuild.number", footer: "", link: env.BUILD_URL, result: currentBuild.currentResult, title: JOB_NAME, webhookURL: "$WEBHOOK_URL"
        }
    }
}