pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    parameters {
        string(name: 'TEST_STUDENT_EMAIL', defaultValue: '', description: "Email")
        password(name: 'TEST_STUDENT_PASSWORD', defaultValue: '', description: "Password")
        string(name: 'TEST_BRANCH', defaultValue: 'main', description: "Git branch")
    }

    environment {
        TEST_API_BASE_URL = 'http://api-gateway:8080'
    }

    stages {
        stage("Chechout") {
            steps {
                checkout scm
            }
        }

        stage("Run tests") {
            steps {
                sh 'bash scripts/run_tests.sh'
            }
        }
    }
    post {
        always {
            step([$class: 'AllureReportPublisher', commandline: 'allure-2.30.0', includeProperties: false, jdk: '', results: [[path: 'allure-results']]])
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive:true
            script {
                currentBuild.description = env.BUILD_URL ? "Allure report: ${env.BUILD_URL}" : "Allure report"
            }
        }
    }
}


