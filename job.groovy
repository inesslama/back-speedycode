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
            tag('0.0.1')
            registryCredentials('github_credentials')
            forcePull(false)
            createFingerprints(false)
            skipDecorate()
            
        
        }
    }
}
