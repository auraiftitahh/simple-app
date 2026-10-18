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

                        $tokenValue = $env:DOCKERHUB_TOKEN.Trim()

                        if ($tokenValue.StartsWith('{AQAA')) {
                            throw 'Pipeline menerima teks terenkripsi, bukan token asli'
                        }
                        
                        if (-not $tokenValue.StartsWith('dckr_pat_')) {
                            throw 'Format token yang diterima pipeline tidak sesuai'
                        }
                        
                        if ($tokenValue -match '\\s') {
                            throw 'Token mengandung spasi atau baris baru'
                        }
                        
                        Write-Output 'Format token yang diterima Jenkins valid'

                        $loginInfo = New-Object System.Diagnostics.ProcessStartInfo
                        $loginInfo.FileName = 'docker.exe'
                        $loginInfo.Arguments = 'login --username auraiftitahh --password-stdin'
                        $loginInfo.UseShellExecute = $false
                        $loginInfo.RedirectStandardInput = $true
                        $loginInfo.CreateNoWindow = $true
                        
                        $loginProcess = New-Object System.Diagnostics.Process
                        $loginProcess.StartInfo = $loginInfo
                        
                        [void]$loginProcess.Start()
                        $loginProcess.StandardInput.WriteLine($env:DOCKERHUB_TOKEN.Trim())
                        $loginProcess.StandardInput.Close()
                        $loginProcess.WaitForExit()
                        
                        $loginExitCode = $loginProcess.ExitCode
                        $loginProcess.Dispose()
                        
                        if ($loginExitCode -ne 0) {
                            throw 'Docker login gagal melalui standard input langsung'
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
