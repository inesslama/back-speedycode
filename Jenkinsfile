pipeline {

  environment {
    dockerImage = "docker1299999/login:0.0.1"
  }

  agent any

  stages {

    stage('Checkout Source') {
      steps {
        git branch: 'login', credentialsId: 'github_credentials', url: 'https://github.com/elyadata/SpeedyCode-backend.git'
      }
    }

    stage('Build image') {
      steps{
        script {
          dockerImage = docker.build dockerImage
        }
      }
    }

    stage('Pushing Image') {
      environment {
               registryCredential = 'dockerhublogin'
           }
      steps{
        script {
          docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
            dockerImage.push("0.0.1")
          }
        }
      }
    }

    
  
  
  }

}