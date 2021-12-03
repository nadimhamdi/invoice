pipeline {
  agent none
  stages {
    stage('Build') {
      agent {
        docker {
          image 'python:3-alpine'
        }

      }
      steps {
        sh 'python -m py_compile source/para_recog.py source/ROI_Frames_Selector.py source/TabulExecution.py source/TabulExecution.pyc'
        stash(name: 'compiled-results', includes: 'source/*.py*')
      }
    }

    stage('Deliver') {
      agent any
      environment {
        VOLUME = '$(pwd)/sources:/src'
        IMAGE = 'cdrx/pyinstaller-linux:python2'
      }
      post {
        success {
          archiveArtifacts "${env.BUILD_ID}/source/dist/ROI_Frames_Selector"
          sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
        }

      }
      steps {
        dir(path: env.BUILD_ID) {
          unstash 'compiled-results'
          sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F ROI_Frames_Selector.py'"
        }

      }
    }

  }
}