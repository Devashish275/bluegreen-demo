pipeline {
  agent any
  environment {
    IMAGE = "dp7049/bg-app"
    TAG   = "${BUILD_NUMBER}"
    PATH  = "/usr/local/bin:/opt/homebrew/bin:/Applications/Docker.app/Contents/Resources/bin:${PATH}"
    DOCKER_CONFIG = "${WORKSPACE}/.docker"
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build & Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'U', passwordVariable: 'P')]) {
          sh '''
            mkdir -p $DOCKER_CONFIG
            docker build -t $IMAGE:$TAG .
            echo $P | docker login -u $U --password-stdin
            docker push $IMAGE:$TAG
          '''
        }
      }
    }
    stage('Find idle colour') {
      steps {
        script {
          sh 'kubectl config use-context docker-desktop'
          def live = sh(script: "kubectl get svc bg-svc -o jsonpath='{.spec.selector.version}' 2>/dev/null || true", returnStdout: true).trim()
          env.NEW = (live == 'blue') ? 'green' : 'blue'
          echo "Live = ${live ?: 'none (first run)'}, deploying = ${env.NEW}"
        }
      }
    }
    stage('Deploy new version') {
      steps {
        sh '''
          sed "s/__COLOR__/$NEW/g; s|__IMAGE__|$IMAGE:$TAG|" k8s/deployment.yaml | kubectl apply -f -
          kubectl rollout status deployment/bg-app-$NEW
        '''
      }
    }
    stage('Approval') {
      steps { input message: "New version is ready on ${env.NEW}. Switch traffic?" }
    }
    stage('Switch traffic') {
      steps {
        sh 'sed "s/__COLOR__/$NEW/g" k8s/service.yaml | kubectl apply -f -'
      }
    }
  }
}
