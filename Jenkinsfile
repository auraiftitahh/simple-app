pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        IMAGE_NAME = 'auraiftitahh/simple-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Docker') {
            steps {
                bat 'docker version'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-test',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    powershell '''
                        $ErrorActionPreference = 'Stop'

                        if ([string]::IsNullOrWhiteSpace($env:DOCKERHUB_USER)) {
                            throw 'Username credential Jenkins kosong'
                        }

                        if ($env:DOCKERHUB_USER.Trim() -ne 'auraiftitahh') {
                            throw 'Username credential Jenkins tidak sesuai'
                        }

                        if ([string]::IsNullOrWhiteSpace($env:DOCKERHUB_TOKEN)) {
                            throw 'Token credential Jenkins kosong'
                        }

                        $env:DOCKERHUB_TOKEN.Trim() |
                            docker login --username auraiftitahh --password-stdin

                        if ($LASTEXITCODE -ne 0) {
                            throw 'Docker login gagal'
                        }

                        try {
                            docker push "${env:IMAGE_NAME}:${env:BUILD_NUMBER}"
                            if ($LASTEXITCODE -ne 0) {
                                throw 'Docker push gagal'
                            }

                            docker tag "${env:IMAGE_NAME}:${env:BUILD_NUMBER}" "${env:IMAGE_NAME}:latest"
                            if ($LASTEXITCODE -ne 0) {
                                throw 'Docker tag gagal'
                            }

                            docker push "${env:IMAGE_NAME}:latest"
                            if ($LASTEXITCODE -ne 0) {
                                throw 'Docker push latest gagal'
                            }
                        }
                        finally {
                            docker logout
                        }
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Proses pipeline selesai. Periksa hasil setiap stage.'
        }
    }
}
