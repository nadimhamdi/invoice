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
        sh 'python -m py_compile sources/para_recog.py sources/ROI_Frames_Selector.py sources/TabulExecution.py'
        stash(name: 'compiled-results', includes: 'sources/*.py*')
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
          sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F ROI_Frames_Selector.py && pyinstaller -F para_recog.py&& pyinstaller -F TabulExecution.py && pip install --upgrade pip && pip install numpy && pip install scikit-image && pip install opencv-python && pip install tk && pip install pillow && pip install pytesseract && pip install itertools && pip install imutils && pip install matplotlib'"
        }

      }
    }

  }
}
