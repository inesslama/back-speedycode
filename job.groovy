job('dockerbuild_push'){
    
    scm {
        git {
            remote {
                github('https://github.com/inesslama/back.git','https')
            }
             branch('master')

            credentialsId('github_credentials')
        }

       

        

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