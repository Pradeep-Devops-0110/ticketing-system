pipeline {
    agent any

    parameters {
        string(name: 'REPLICAS', defaultValue: '3', description: 'Number of pod replicas to deploy')
    }

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
                    
                    // Push image to Docker Hub so Kind/K8s can pull it
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
                dir('gitops-repo') {
                    script {
                        // 1. Clone the GitOps repository using the 'pradeep' credential
                        git branch: 'main',
                            url: "${GITOPS_REPO}",
                            credentialsId: 'pradeep'

                        // 2. Update the image tag inside deployment.yaml
                        sh "sed -i 's|image: .*|image: ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}|g' deployment.yaml"
                        // Update Replica Count
                        sh "sed -i 's|replicas: .*|replicas: ${params.REPLICAS}|g' deployment.yaml"

                        // 3. Commit and push the changes back to GitHub using 'pradeep' credential
                        withCredentials([usernamePassword(credentialsId: 'pradeep', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                            sh """
                                git config user.email "jenkins@local"
                                git config user.name "Jenkins CI"
                                git add deployment.yaml
                                git commit -m "Automated update: image tag to ${IMAGE_TAG}" || echo "No changes to commit"
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
            echo 'Pipeline completed successfully! GitOps repository updated. ArgoCD will now sync the cluster.'
        }
        failure {
            echo 'Pipeline failed. Check Jenkins logs for details.'
        }
    }
}