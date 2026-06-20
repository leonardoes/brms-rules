// Build
String awsEcrAccount = "${env.AWS_ACCOUNT_ID}"
String awsEcrRegion = "${env.AWS_ECR_REGION}"
String project_repo = "${env.PROJECT_REPO}"
AMBIENTE = "${env.AMBIENTE}"
PORT = "${env.PORT}"
// NOT currently used
String project = "${env.PROJECT}"

// Build & Deploy
String application = "${env.APPLICATION}"
String imageURL = "${awsEcrAccount}.dkr.ecr.${awsEcrRegion}.amazonaws.com/${project_repo}"
String publishVersion = "${env.BUILD_ID}"

// Deploy
String envKey = "${env.ENV_KEY}"
String namespace = "${env.NAMESPACE}"
String nodeName = "${env.NODE_NAME}";
nodeName = "${nodeName}-${envKey}"

node {
    stage('Preparation') {
        checkout scm
    }
    stage('Build') {
        sh "docker build -t ${project_repo}:latest --build-arg PORT=$PORT --build-arg AMBIENTE=$AMBIENTE -f Dockerfile ."
    }
    stage('Push') {
        String imageExists = sh(returnStdout: true, script: "docker images -q ${project_repo}:latest 2> /dev/null")
        if(imageExists != "") {
            sh "aws ecr get-login --region ${awsEcrRegion} --no-include-email --registry-ids ${awsEcrAccount} | sh -"
            sh "docker tag ${project_repo}:latest ${project_repo}:${envKey}-${publishVersion}" 
            docker.withRegistry("https://${awsEcrAccount}.dkr.ecr.${awsEcrRegion}.amazonaws.com") {
                def image = docker.image("${project_repo}:${envKey}-${publishVersion}") 
                image.push()
            }
            sh("docker rmi -f ${project_repo}:latest || :")
            sh("docker rmi -f ${project_repo}:${envKey}-${publishVersion} || :") 
            sh("docker rmi -f ${imageURL}:${envKey}-${publishVersion} || :") 
            if(env.DEPLOY == 'true') {
                node(nodeName) {
                    stage('Deploy') {
                        checkout scm
                        //String projectReleaseName = "${application}-${envKey}"
                        String projectReleaseName = "${application}"
                        sh "helm upgrade --install ${projectReleaseName} chart/ --values=chart/values-${envKey}.yaml --namespace ${namespace} --set image.repository=${imageURL} --set image.tag=${envKey}-${publishVersion} --debug --wait --timeout 600"
                        cleanWs()
                    }
                }
            }
        }
    }
}