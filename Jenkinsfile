pipeline {
    agent any

    environment {
        IMAGE_NAME = 'ticketing-system'
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Git Repository-யில் இருந்து கோடைத் திரும்பப் பெறுதல்
                checkout scm
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
                    sh "kubectl apply -f k8s-deployment.yaml"
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