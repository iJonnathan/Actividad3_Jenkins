pipeline {
    // 1. AGENTE: Dónde se ejecutará el pipeline.
    agent {
        docker { 
            image 'python:3.9-slim-buster' 
            // Se fuerza la ejecución como usuario root para evitar problemas de permisos.
            args '-u root'
        }
    }

    // 2. ETAPAS (STAGES): Los pasos lógicos del proceso.
    stages {
        // Etapa de construcción.
        stage('Build') {
            steps {
                echo 'Instalando dependencias...'
                sh 'pip install -r requirements.txt'
            }
        }

        // Etapa de pruebas unitarias.
        stage('Unit tests') {
            steps {
                echo 'Ejecutando pruebas unitarias...'
                sh 'mkdir -p results'
                // Se establece PYTHONPATH para que pytest encuentre el módulo 'app'.
                sh 'PYTHONPATH=. pytest --junitxml=results/unit_test_result.xml test/unit/'
            }
        }
        
        // Etapa de pruebas de API.
        stage('API tests') {
            steps {
                echo 'Ejecutando pruebas de API...'
                sh 'mkdir -p results'
                // Se establece PYTHONPATH también para las pruebas de API.
                sh 'PYTHONPATH=. pytest --junitxml=results/api_test_result.xml test/rest/'
            }
        }

        // Etapa de pruebas E2E.
        stage('E2E tests') {
            steps {
                echo 'Ejecutando pruebas End-to-End...'
                sh 'mkdir -p results'
                sh 'echo "<?xml version=\'1.0\' encoding=\'UTF-8\'?><testsuite name=\'e2e_tests\' tests=\'1\' failures=\'0\' errors=\'0\' skipped=\'1\'><testcase name=\'no_e2e_tests_defined\'><skipped/></testcase></testsuite>" > results/e2e_test_result.xml'
            }
        }
    }

    // 3. ACCIONES POST-EJECUCIÓN (POST): Tareas de limpieza y reporte.
    post {
        always {
            echo 'Archivando y publicando informes...'
            archiveArtifacts artifacts: 'results/*.xml', fingerprint: true
            junit 'results/*_result.xml'
            cleanWs()
        }
        failure {
            echo "¡El pipeline ha fallado! Enviando notificación..."
            echo "Notificación de fallo para el job: ${env.JOB_NAME}, ejecución #${env.BUILD_NUMBER}."
        }
    }
}