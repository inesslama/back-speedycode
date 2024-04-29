job('dockerbuild_push'){
    
    scm {
        git {
            
            remote {
                url('https://github.com/inesslama/back.git') 
                credentials('github_credentials')
            }

            branch('master')
            

            

            
        }

       

        

    }

    triggers{
        scm('H/5 * * * * ')

    }

    
     steps {

       script{
        
        docker.build('docker1299999/login:0.0.1')

        docker.withRegistry('https://registry.hub.docker.com', 'dockerhublogin') {

           docker.image('docker1299999/login:0.0.1').push()


        } 
      
       }
        
    }


}