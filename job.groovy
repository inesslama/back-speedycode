job('dockerbuild_push') {
    scm {
        git {
            remote {
                url('https://github.com/inesslama/back.git') 
                credentials('github_credentials')
            }
            branch('master')
        }
    }
    
    triggers {
        scm('H/5 * * * * ')
    }

    steps {
        // Build Docker image
        docker.build('docker1299999/login:0.0.1').with {
            // Push Docker image
            push()
        }
    }
}
