pipeline {
agent { label 'flask' }

stages {

    stage('Install Dependencies') {
        steps {
            sh '''
            cd student-registration-application
            pip3 install -r requirements.txt
            '''
        }
    }

    stage('Deploy Flask App') {
        steps {
            sh '''
            cd student-registration-application
            pkill -f app.py || true
            nohup python3 app.py > flask.log 2>&1 &
            '''
        }
    }

}

}
