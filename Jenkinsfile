pipeline {
agent { label 'flask' }

```
stages {

    stage('Install Dependencies') {
        steps {
            sh '''
            cd /home/ec2-user/workspace/jenkins-pipeline/student-registration-application
            /usr/bin/pip3 install -r requirements.txt
            '''
        }
    }

    stage('Deploy Flask App') {
        steps {
            sh '''
            cd /home/ec2-user/workspace/jenkins-pipeline/student-registration-application
            pkill -f app.py || true
            nohup /usr/bin/python3 /home/ec2-user/workspace/jenkins-pipeline/student-registration-application/app.py > flask.log 2>&1 &
            '''
        }
    }

}
```

}
