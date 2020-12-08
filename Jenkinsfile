pipeline {
    agent {
        docker { image 'testnode:tagtest' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}
