pipeline {
agent { label 'flask' }


stages {

    stage('Checkout Code') {
        steps {
            git 'https://github.com/samarthfunde/Flask-Based-Student-Registration-Application-with-CI-CD-Deployment.git'
        }
    }

    stage('Install Dependencies') {
        steps {
            sh '''
            cd student-registration-application
            pip3 install -r requirements.txt
            '''
        }
    }

    stage('Restart Flask Service') {
        steps {
            sh '''
            sudo systemctl restart flaskapp
            '''
        }
    }

}

}
