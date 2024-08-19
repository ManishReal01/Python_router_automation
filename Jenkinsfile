pipeline {
    agent any
 
    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/ManishReal01/Python_router_automation', branch: 'main'
            }
        }
        stage('Set Permissions') {
            steps {
                sh 'chmod +x ./router-hname.sh'
            }
        }
        stage('Run Python Script') {
            steps {
                sh 'sudo ./router-hname.sh'
            }
        }
    }
}
