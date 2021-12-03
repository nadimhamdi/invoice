pipeline {
  agent none
  stages {
    stage('Build') {
      agent {
        docker {
          image 'python:3.6.8-alpine'
        }

      }
      steps {
        sh 'python -m py_compile source/para_recog.py source/ROI_Frames_Selector.py source/TabulExecution.py'
        stash(name: 'compiled-results', includes: 'source/*.py*')
      }
    }

    stage('Deliver') {
      agent any
      environment {
        VOLUME = '$(pwd)/sources:/src'
        IMAGE = 'cdrx/pyinstaller-linux:python3'
      }
      post {
        success {
          archiveArtifacts "${env.BUILD_ID}/sources/dist/ROI_Frames_Selector"
          sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
        }

      }
      steps {
        dir(path: env.BUILD_ID) {
          unstash 'compiled-results'
          sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F source/ROI_Frames_Selector.py'"
        }

      }
    }

  }
}