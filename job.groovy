job('dockerbuild_push'){
    
    scm {
        git {
            remote {
                github('https://github.com/elyadata/SpeedyCode-backend.git','https')
            }
        }

        branch('features/login')

        credentialsId('github_credentials')

        

    }

    triggers{
        scm('H/5 * * * * ')

    }

    
     steps {
        
        dockerBuildAndPublish {
            repositoryName('docker1299999/login')
            tag('0.0.1')
            registryCredentials('dockerhublogin')
            forcePull(false)
            createFingerprints(false)
            skipDecorate()
        }
    }


}