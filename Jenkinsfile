pipeline {
  agent any
  stages {
    stage('Stage 1') {
      steps {
        sh '''su ec2-user -c \'cd /home/ec2-user/DevOpsFlasked; git pull\'
systemctl stop gunicorn.service
sleep 5
systemctl start gunicorn.service
systemctl status gunicorn.service'''
      }
    }

  }
}