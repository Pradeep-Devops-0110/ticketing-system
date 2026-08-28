pipeline {
    agent any

    environment {
        IMAGE_NAME = 'ticketing-system'
        IMAGE_TAG = "v${BUILD_NUMBER}"
        KUBECONFIG = '/var/jenkins_home/.kube/config'
    }

    stages {
        stage('Checkout Code') {
                steps {
                    git branch: 'main',
                        url: 'https://github.com/Pradeep-Devops-0110/ticketing-system.git',
                        credentialsId: 'pradeep'
                }
            }
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying to Kubernetes cluster..."
                    // மேனிஃபெஸ்ட் ஃபைலில் புதிய Image Tag-ஐப் புதுப்பித்து Apply செய்தல்
                    sh "sed -i 's|image: ticketing-system:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|g' k8s-deployment.yaml"
                    sh "kubectl apply -f k8s-deployment.yaml --validate=false"
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh "kubectl rollout status deployment/ticketing-system-deployment"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully and app is deployed!'
        }
        failure {
            echo 'Pipeline failed. Check Jenkins logs for details.'
        }
    }
}