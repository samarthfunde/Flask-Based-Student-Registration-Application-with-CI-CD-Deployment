pipeline {
    agent any

    environment {
        FLASK_SERVER = "43.204.28.252"
    }

    stages {

        stage('Clone Repo') {
            steps {
                git 'https://github.com/samarthfunde/Flask-Based-Student-Registration-Application-with-CI-CD-Deployment.git'
            }
        }

        stage('Deploy Application') {
            steps {
                sshagent(['flask-server-key']) {
                    sh '''
                    scp -o StrictHostKeyChecking=no -r student-registration-application ec2-user@$FLASK_SERVER:/home/ec2-user/

                    ssh -o StrictHostKeyChecking=no ec2-user@$FLASK_SERVER << EOF
                    cd student-registration-application
                    pip3 install -r requirements.txt
                    pkill -f app.py || true
                    nohup python3 app.py > app.log 2>&1 &
                    EOF
                    '''
                }
            }
        }

    }
}
