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
        scm('* * * * * ') 
    }

    steps {
        dockerBuildAndPublish {
            repositoryName('docker1299999/login')
            registryCredentials('github_credentials')
            
        
        }
    }
}
