# Flask-Based Student Registration Application with CI/CD Deployment

This project is a simple student registration web application built with Python Flask and MySQL. It is deployed on AWS EC2 and uses Jenkins for automated CI/CD so that every time you push code to GitHub, the application gets updated automatically without any manual work.

---

## What This Project Does

- Students can fill out a registration form with their name, email, and course.
- The data is saved into a MySQL database.
- Jenkins watches the GitHub repository, and whenever new code is pushed, it pulls the latest code, installs dependencies, and restarts the Flask application automatically.

---

## Architecture

The project uses three separate EC2 servers, each handling one responsibility.

**Jenkins Server** handles CI/CD. Whenever code is pushed to GitHub, a webhook triggers Jenkins, which runs the pipeline to deploy the updated application.

**Flask Application Server** runs the Python Flask web application. It connects to the MySQL database to store and retrieve student records.

**MySQL Database Server** stores all student registration data in a database called `studentdb`.

The flow looks like this:

```
Developer pushes code to GitHub
        |
GitHub sends webhook to Jenkins
        |
Jenkins pulls latest code on Flask server
        |
Jenkins installs dependencies and restarts Flask app
        |
Updated application is live
```

<img width="939" height="625" alt="image" src="https://github.com/user-attachments/assets/5e8a9aff-7561-4524-add2-4c604c29c4eb" />


---

## Technologies Used

- Python Flask
- MySQL (MariaDB on Amazon Linux)
- Git and GitHub
- Jenkins
- AWS EC2 (Amazon Linux 2)

---

## Setup Instructions

### Step 1 - Create EC2 Instances

Create three EC2 instances on AWS with the following settings:

**Jenkins Server**
- AMI: Amazon Linux 2
- Instance Type: t3.micro
- Storage: 10 GB
- Open port 8080 in the security group for Jenkins UI
  
  <img width="940" height="113" alt="image" src="https://github.com/user-attachments/assets/98376b01-be73-4521-b586-6b2b3488ebc1" />

  <img width="940" height="242" alt="image" src="https://github.com/user-attachments/assets/15da11e1-7868-44cb-888d-0e163ba177f8" />



**Flask App Server**
- AMI: Amazon Linux 2
- Instance Type: t2.micro
- Storage: 10 GB
- Open port 22 (SSH), port 5000 (Flask), and port 80 (HTTP)

 <img width="940" height="193" alt="image" src="https://github.com/user-attachments/assets/22ef083b-3643-4414-9a61-4af7502b770d" />

<img width="940" height="262" alt="image" src="https://github.com/user-attachments/assets/f30c7ea1-a459-4634-ae04-e01ba51d60bc" />



**MySQL Database Server**
- AMI: Amazon Linux 2
- Instance Type: t2.micro
- Storage: 10 GB
- Open port 22 (SSH) and port 3306 (MySQL, accessible from the Flask server only

<img width="940" height="189" alt="image" src="https://github.com/user-attachments/assets/aa7a7e42-c3a0-4326-9d68-faf6cffa0374" />

<img width="940" height="237" alt="image" src="https://github.com/user-attachments/assets/77a01285-e26c-430a-accc-114993529131" />


---

### Step 2 - Setup MySQL Database Server

SSH into the database server and run the following commands:

```bash
sudo yum update -y
sudo yum install mariadb105-server -y
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

Log into MySQL and set up the database:

```sql
mysql -u root -p

CREATE DATABASE studentdb;
USE studentdb;

CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  course VARCHAR(100)
);

CREATE USER 'flaskuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON studentdb.* TO 'flaskuser'@'%';
FLUSH PRIVILEGES;
```

---

<img width="940" height="433" alt="image" src="https://github.com/user-attachments/assets/aae1545d-da98-45f2-bf5c-a103ffb593e2" />



### Step 3 - Setup Flask Application Server

SSH into the Flask server and install the required packages:

```bash
sudo yum update -y
sudo yum install python3 git -y
```

Clone your application code and install Python dependencies:

```bash
git clone <your-repo-url>
cd student-registration-application
pip3 install -r requirements.txt
```

Configure the Flask app as a systemd service so it runs in the background and restarts automatically:

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

Paste this configuration:

```
[Unit]
Description=Flask Application
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/workspace/jenkins-pipeline/student-registration-application
ExecStart=/usr/bin/python3 /home/ec2-user/workspace/jenkins-pipeline/student-registration-application/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
```

---

<img width="940" height="375" alt="image" src="https://github.com/user-attachments/assets/f80be5df-239b-49cb-a2ac-7ad340e80853" />

<img width="940" height="284" alt="image" src="https://github.com/user-attachments/assets/da4d5543-c346-4b69-b407-40a137ab5be7" />

<img width="940" height="116" alt="image" src="https://github.com/user-attachments/assets/84fcfb31-84c6-49d0-9784-6be64c92f977" />

mysql -u flaskuser -p
Password: add password

<img width="940" height="343" alt="image" src="https://github.com/user-attachments/assets/7a136fa6-5448-4941-8553-201962b62430" />


### Step 4 - Setup Jenkins Server

SSH into the Jenkins server and install Java and Jenkins:

```bash
sudo yum install java-17-amazon-corretto -y
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/rpm-stable/jenkins.repo
sudo yum upgrade
sudo yum install jenkins -y
sudo yum install git -y
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

Open Jenkins in your browser at `http://<JENKINS_PUBLIC_IP>:8080` and complete the setup using the initial admin password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Install these plugins from Manage Jenkins > Plugins > Available Plugins:
- Git Plugin
- GitHub Plugin
- Pipeline Plugin
- SSH Agent Plugin

---

<img width="940" height="477" alt="image" src="https://github.com/user-attachments/assets/02f5ab93-f39b-495e-a9a7-196f488a45bf" />

<img width="940" height="471" alt="image" src="https://github.com/user-attachments/assets/bb1bcf89-91a5-40f5-a3d3-7c668ad43b4a" />



### Step 5 - Push Code to GitHub

On the Flask server, push your application code to GitHub:

```bash
cd student-registration-application
git init
git add .
git commit -m "initial commit"
git remote add origin <your-github-repo-url>
git push origin master
```

---

<img width="856" height="350" alt="image" src="https://github.com/user-attachments/assets/3d6dd7c7-d7f4-41a0-832e-a5ee7404d0ad" />


### Step 6 - Create Jenkins Pipeline

1. Go to Jenkins Dashboard and click New Item.
2. Name it `flask-pipeline`, select Pipeline, and click OK.
3. Under Pipeline settings, set Definition to "Pipeline script from SCM".
4. Set SCM to Git and enter your repository URL.
5. Set branch to `*/master` and Script Path to `Jenkinsfile`.
6. Click Save.

Add a `Jenkinsfile` in your GitHub repository with the following content:

```groovy
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
```

Also allow Jenkins to restart services without a password prompt:

```bash
sudo visudo
```

Add this line at the end:

```
ec2-user ALL=(ALL) NOPASSWD: ALL
```

---

### Step 7 - Setup GitHub Webhook

1. Go to your GitHub repository Settings > Webhooks > Add Webhook.
2. Set the Payload URL to `http://<JENKINS_PUBLIC_IP>:8080/github-webhook/`
3. Set Content type to `application/json`.
4. Save the webhook.

Now every time you push code to GitHub, Jenkins will automatically deploy the updated application.

---

<img width="940" height="333" alt="image" src="https://github.com/user-attachments/assets/f62ea7e5-c6b5-4048-9eda-94200abb676c" />

<img width="940" height="379" alt="image" src="https://github.com/user-attachments/assets/a1400694-fd3b-43d7-9cea-f11ff685823e" />



## How to Test

1. Open the Flask app in your browser at `http://<FLASK_SERVER_IP>:5000`
2. Fill in the student registration form and submit.
3. Log into the database server and check that the record was saved:

```bash
mysql -u flaskuser -p
USE studentdb;
SELECT * FROM students;
```

---

## Challenges Faced

**Connecting Jenkins to the Flask Server** was tricky at first. Jenkins needs to SSH into the Flask server to run deployment commands. Setting up the SSH agent and making sure the correct key permissions were in place took some trial and error.

**Passwordless sudo for Jenkins** was a required step that is easy to miss. Without it, the pipeline fails when trying to restart the Flask systemd service because Jenkins does not have sudo privileges by default.

**MySQL remote access** required making sure the database server's security group allowed connections from the Flask server's IP on port 3306. Initially the connection was being refused because of this.

**Systemd service working directory** had to exactly match where Jenkins was checking out the code. If the path was slightly wrong, the Flask app would fail to start after deployment.

---

## Future Improvements

- Add HTTPS using an SSL certificate so the application runs securely instead of over plain HTTP.
- Use Docker to containerize the Flask application so it is easier to deploy consistently across different environments.
- Add a staging environment where code is first deployed and tested before going to production.
- Store database credentials in environment variables or AWS Secrets Manager instead of hardcoding them in the application.
- Add automated tests in the Jenkins pipeline so that broken code never gets deployed.
- Set up monitoring and alerts using a tool like CloudWatch so you know immediately if the application goes down.
- Use an RDS instance instead of a self-managed MySQL server for better reliability and automated backups.

---

## Repository Structure

```
student-registration-application/
    app.py
    requirements.txt
    templates/
        index.html
Jenkinsfile
README.md
```

---

## Author

Samarth Funde
