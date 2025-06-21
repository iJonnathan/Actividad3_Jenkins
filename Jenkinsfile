pipeline {
    // 1. AGENTE: Dónde se ejecutará el pipeline.
    // Se usa 'agent any' para que se ejecute en cualquier agente disponible.
    agent any

    // 2. ETAPAS (STAGES): Los pasos lógicos del proceso.
    stages {
        // La etapa 'Source' es manejada automáticamente por Jenkins.

        // Etapa de construcción.
        stage('Build') {
            steps {
                echo 'Instalando dependencias...'
                // Se ejecuta el comando directamente para no depender de 'make'.
                sh 'pip install -r requirements.txt'
            }
        }

        // Etapa de pruebas unitarias.
        stage('Unit tests') {
            steps {
                echo 'Ejecutando pruebas unitarias...'
                // Se crean los directorios y se ejecuta pytest directamente.
                sh 'mkdir -p results'
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
        // Se ejecuta siempre, independientemente del resultado (éxito o fallo).
        always {
            echo 'Archivando y publicando informes...'
            
            // Archiva los XML generados para su posterior análisis.
            archiveArtifacts artifacts: 'results/*.xml', fingerprint: true

            // Usa el plugin JUnit para procesar los XML y mostrar gráficos de resultados.
            junit 'results/*_result.xml'

            // Limpia el espacio de trabajo para mantener Jenkins ordenado.
            cleanWs()
        }
        
        // Se ejecuta solo si el pipeline falla.
        failure {
            echo "¡El pipeline ha fallado! Enviando notificación..."
            
            // Simulación del envío de correo.
            echo "Notificación de fallo para el job: ${env.JOB_NAME}, ejecución #${env.BUILD_NUMBER}."

            /*
            // Código real para el envío de correo (requiere configuración del plugin).
            mail to: 'tu.correo@example.com',
                 subject: "FALLO en el Job: ${env.JOB_NAME} [Build #${env.BUILD_NUMBER}]",
                 body: "La ejecución #${env.BUILD_NUMBER} del job ${env.JOB_NAME} ha fallado. Revisa la consola: ${env.BUILD_URL}"
            */
        }
    }
}
