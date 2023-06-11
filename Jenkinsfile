pipeline {
    agent any 

    stages {
        stage('Build') { 
            steps {
                // Install dependencies
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Pull Data and Model') {
            steps {
                // Pull the data and the model from DVC remote
                sh 'dvc pull'
            }
        }
        
        stage('Train Model and Serve') {
            steps {
                // Start the Airflow webserver and scheduler in the background
                sh 'airflow webserver -D'
                sh 'airflow scheduler -D'

                // Run the Airflow pipeline
                sh 'airflow dags trigger train_and_serve'
            }
        }

        stage('Check Model Performance') {
            steps {
                // Print out the MLFlow metrics
                script {
                    def metrics = sh(script: 'mlflow run model_training --no-conda', returnStdout: true).trim()
                    println("Model Performance Metrics: ${metrics}")
                }
            }
        }
    }
}
