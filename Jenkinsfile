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
            agent {
                docker {
                    image 'cdrx/pyinstaller-linux:python3'
                }
            }
            steps {
                sh 'pyinstaller --onefile source/ROI_Frames_Selector.py'
            }
            post {
                success {
                    archiveArtifacts 'dist/ROI_Frames_Selector'
                }
            }
        }
    }
}
