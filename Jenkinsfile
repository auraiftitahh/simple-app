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

                        if ([string]::IsNullOrWhiteSpace($env:DOCKERHUB_TOKEN)) {
                            throw 'Token Jenkins kosong'
                        }

                        $tokenValue = $env:DOCKERHUB_TOKEN.Trim()
                        $username = $env:DOCKERHUB_USER.Trim()

                        if ($username -ne 'auraiftitahh') {
                            throw 'Username credential tidak sesuai'
                        }

                        if (-not $tokenValue.StartsWith('dckr_pat_')) {
                            throw 'Format token Docker Hub tidak sesuai'
                        }

                        $env:DOCKER_CONFIG = Join-Path $env:TEMP (
                            'jenkins-docker-' + [guid]::NewGuid().ToString()
                        )

                        New-Item -ItemType Directory -Path $env:DOCKER_CONFIG -Force |
                            Out-Null

                        $configFile = Join-Path $env:DOCKER_CONFIG 'config.json'

                        [System.IO.File]::WriteAllText(
                            $configFile,
                            '{"auths":{}}',
                            [System.Text.UTF8Encoding]::new($false)
                        )

                        try {
                            Write-Output 'Menggunakan konfigurasi Docker terpisah'

                            $basicAuth = [Convert]::ToBase64String(
                                [Text.Encoding]::UTF8.GetBytes("${username}:${tokenValue}")
                            )
                            
                            try {
                                $authResult = Invoke-RestMethod `
                                    -Uri 'https://auth.docker.io/token?service=registry.docker.io' `
                                    -Headers @{ Authorization = "Basic $basicAuth" } `
                                    -Method Get `
                                    -ErrorAction Stop
                            
                                if (-not $authResult.token -and -not $authResult.access_token) {
                                    throw 'Docker Hub tidak memberikan token autentikasi'
                                }
                            
                                Write-Output 'Autentikasi langsung ke Docker Hub BERHASIL'
                            }
                            catch {
                                throw 'Autentikasi langsung ke Docker Hub GAGAL. Pemeriksaan Docker CLI belum dilanjutkan.'
                            }
                            finally {
                                $basicAuth = $null
                                $authResult = $null
                            }
                            $loginInfo = New-Object System.Diagnostics.ProcessStartInfo
                            $loginInfo.FileName = 'docker.exe'
                            $loginInfo.Arguments = 'login --username auraiftitahh --password-stdin'
                            $loginInfo.UseShellExecute = $false
                            $loginInfo.RedirectStandardInput = $true
                            $loginInfo.CreateNoWindow = $true

                            $loginProcess = New-Object System.Diagnostics.Process
                            $loginProcess.StartInfo = $loginInfo

                            try {
                                [void]$loginProcess.Start()
                                $loginProcess.StandardInput.WriteLine($tokenValue)
                                $loginProcess.StandardInput.Close()
                                $loginProcess.WaitForExit()

                                if ($loginProcess.ExitCode -ne 0) {
                                    throw 'Docker login gagal'
                                }
                            }
                            finally {
                                $loginProcess.Dispose()
                            }

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
                            if (Test-Path -LiteralPath $configFile) {
                                Remove-Item -LiteralPath $configFile -Force
                            }
                            $tokenValue = $null
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
