pipeline {
agent { label 'flask' }


stages {

    stage('Install Dependencies') {
        steps {
            sh '''
            cd student-registration-application
            /usr/bin/pip3 install -r requirements.txt
            '''
        }
    }

    stage('Deploy Flask App') {
        steps {
            sh '''
            cd student-registration-application
            pkill -f app.py || true
            setsid /usr/bin/python3 app.py > flask.log 2>&1 &
            '''
        }
    }

}


}
