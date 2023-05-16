pipeline {
    agent any
    environment {
        // The MY_KUBECONFIG environment variable will be assigned
        // the value of a temporary file.  For example:
        //   /home/user/.jenkins/workspace/cred_test@tmp/secretFiles/546a5cf3-9b56-4165-a0fd-19e2afe6b31f/kubeconfig.txt
        BROWSERSTACK_USERNAME = credentials('BROWSERSTACK_USERNAME')
        BROWSERSTACK_ACCESS_KEY = credentials('BROWSERSTACK_ACCESS_KEY')
        browserstacktempusername1 = credentials('browserstacktempusername1')
        browserstacktemppassword1 = credentials('browserstacktemppassword1')
        
    }   
    stages {
        stage('Execute Step 1') {
            steps {
                echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
                sh 'printenv'
                sh 'python testcases/test_step1.py'
                
            
            }
        }
    }
}
