pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'rvp0110'
        IMAGE_NAME = 'ticketing-system'
        IMAGE_TAG = "v${BUILD_NUMBER}"
        GITOPS_REPO = 'https://github.com/Pradeep-Devops-0110/ticketing-system-gitops.git'
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                git branch: 'main',
                    url: 'https://github.com/Pradeep-Devops-0110/ticketing-system.git',
                    credentialsId: 'pradeep'
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    echo "Building Docker Image: ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker build --no-cache -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                    sh "docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
                    
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo \"\$DOCKER_PASS\" | docker login -u \"\$DOCKER_USER\" --password-stdin"
                        sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                        sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
                    }
                }
            }
        }

        stage('Update GitOps Repository') {
            steps {
                script {
                    // Extract replicas count directly from the application repo's deployment.yaml
                    def REPLICAS_COUNT = sh(
                        script: "grep -E '^[[:space:]]*replicas:' deployment.yaml | awk '{print \$2}'",
                        returnStdout: true
                    ).trim() ?: '2'

                    dir('gitops-repo') {
                        // 1. Clone GitOps repo
                        git branch: 'main',
                            url: "${GITOPS_REPO}",
                            credentialsId: 'pradeep'

                        // 2. Patch image tag and replica count in GitOps deployment manifest
                        sh "sed -i 's|image: .*|image: ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}|g' deployment.yaml"
                        sh "sed -i 's|replicas: .*|replicas: ${REPLICAS_COUNT}|g' deployment.yaml"

                        // 3. Commit and push back to GitHub
                        withCredentials([usernamePassword(credentialsId: 'pradeep', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                            sh """
                                git config user.email "jenkins@local"
                                git config user.name "Jenkins CI"
                                git add deployment.yaml
                                git commit -m "Automated update: image tag to ${IMAGE_TAG}, replicas to ${REPLICAS_COUNT}" || echo "No changes to commit"
                                git push https://${GIT_USER}:${GIT_PASS}@github.com/Pradeep-Devops-0110/ticketing-system-gitops.git main
                            """
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! GitOps repository updated. Argo CD will now sync the cluster.'
        }
        failure {
            echo 'Pipeline failed. Check Jenkins logs for details.'
        }
    }
}