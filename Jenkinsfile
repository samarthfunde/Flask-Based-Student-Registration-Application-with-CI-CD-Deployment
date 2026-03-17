pipeline {
    agent any

    stages {

        stage('Deploy to Flask Server') {
            steps {
                sshagent(['flask-server-key']) {
                    sh '''
                    scp -o StrictHostKeyChecking=no app.py ec2-user@FLASK_PUBLIC_IP:/home/ec2-user/

                    ssh -o StrictHostKeyChecking=no ec2-user@FLASK_PUBLIC_IP << EOF
                    pkill -f app.py
                    nohup python3 app.py > output.log 2>&1 &
                    EOF
                    '''
                }
            }
        }

    }
}
