pipeline {
    agent any

    parameters {
        string(name: 'HOSTNAME', defaultValue: '172.20.20.3', description: 'Router hostname or IP')
        string(name: 'NEW_USERNAME', defaultValue: '', description: 'New user username')
        string(name: 'NEW_PASSWORD', defaultValue: '', description: 'New user password')
        string(name: 'ENABLE_PASSWORD', defaultValue: '', description: 'Router enable password (if any)')
    }

    environment {
        REPO_URL = 'https://github.com/ManishReal01/Python_router_automation.git'
        BRANCH_NAME = 'main'
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    try {
                        git branch: "${BRANCH_NAME}", url: "${REPO_URL}"
                    } catch (Exception e) {
                        error "Failed to clone repository. Verify the repository URL and branch name."
                    }
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Check if python3-venv is installed
                    def venvInstalled = sh(script: "python3 -m venv --help", returnStatus: true) == 0
                    if (!venvInstalled) {
                        error "python3-venv is not installed. Please install it manually."
                    }

                    // Create and activate virtual environment
                    sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install netmiko
                    """
                }
            }
        }

        stage('Run Script') {
            steps {
                script {
                    // Activate virtual environment and run the Python script with parameters
                    def enablePasswordArg = params.ENABLE_PASSWORD ? params.ENABLE_PASSWORD : ''
                    sh """
                    . venv/bin/activate
                    python3 add_user.py ${params.HOSTNAME} ${params.NEW_USERNAME} ${params.NEW_PASSWORD} ${enablePasswordArg}
                    """
                }
            }
        }
    }
}
