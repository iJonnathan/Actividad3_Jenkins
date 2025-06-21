pipeline {
    // 1. AGENTE: Dónde se ejecutará el pipeline.
    // Se usa un agente de Docker para crear un entorno de construcción limpio y predecible.
    agent {
        docker { image 'python:3.9-slim-buster' }
    }

    // Se define el entorno explícitamente para asegurar que los plugins encuentren los comandos.
    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    }

    // 2. ETAPAS (STAGES): Los pasos lógicos del proceso.
    stages {
        // Etapa de construcción.
        stage('Build') {
            steps {
                echo 'Instalando dependencias...'
                // Este comando se ejecutará dentro del contenedor de Docker.
                sh 'pip install -r requirements.txt'
            }
        }

        // Etapa de pruebas unitarias.
        stage('Unit tests') {
            steps {
                echo 'Ejecutando pruebas unitarias...'
                sh 'mkdir -p results'
                // pytest fue instalado en la etapa anterior, por lo que está disponible.
                sh 'pytest --junitxml=results/unit_test_result.xml test/unit/'
            }
        }
        
        // Etapa de pruebas de API.
        stage('API tests') {
            steps {
                echo 'Ejecutando pruebas de API...'
                sh 'mkdir -p results'
                sh 'pytest --junitxml=results/api_test_result.xml test/rest/'
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
            /*
            // Código real para el envío de correo.
            mail to: 'tu.correo@example.com',
                 subject: "FALLO en el Job: ${env.JOB_NAME} [Build #${env.BUILD_NUMBER}]",
                 body: "La ejecución #${env.BUILD_NUMBER} del job ${env.JOB_NAME} ha fallado. Revisa la consola: ${env.BUILD_URL}"
            */
        }
    }
}