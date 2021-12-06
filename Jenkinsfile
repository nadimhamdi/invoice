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
                CONDA_DLL_SEARCH_MODIFICATION_ENABLE=1
            }
            steps {
                bat 'conda activate venv'
                bat '/home/nadim/anaconda3/envs/venv/lib/python3.6/PyInstaller --onefile gh-debug.spec'
                //bat 'c:\\Users\\Ross\\anaconda3\\envs\\test\\python -c "import mkl"'
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
          sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F ROI_Frames_Selector.py && pyinstaller -F para_recog.py && pyinstaller -F TabulExecution.py'"
        }

      }
    }

  }
}
