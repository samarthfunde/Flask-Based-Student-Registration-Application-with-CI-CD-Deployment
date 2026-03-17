pipeline {
    agent { label 'flask' }

    stages {

        stage('Run Flask App') {
            steps {
                sh '''
                cd student-registration-app
                pkill -f app.py || true
                nohup python3 app.py > output.log 2>&1 &
                '''
            }
        }

    }
}
