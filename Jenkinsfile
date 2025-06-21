pipeline {
    // 1. AGENTE: Dónde se ejecutará el pipeline.
    agent {
        label 'docker' // Le dice a Jenkins que busque un agente con la etiqueta 'docker'.
    }

    // 2. ETAPAS (STAGES): Los pasos lógicos del proceso.
    stages {
        // La etapa 'Source' es manejada automáticamente por Jenkins al usar "Pipeline script from SCM".
        // Jenkins clona el repositorio antes de empezar a ejecutar las etapas definidas aquí.

        // Etapa de construcción.
        stage('Build') {
            steps {
                echo 'Instalando dependencias...'
                // Ejecuta el comando definido en el Makefile. Mucho más limpio.
                sh 'make build'
            }
        }

        // Etapa de pruebas unitarias.
        stage('Unit tests') {
            steps {
                echo 'Ejecutando pruebas unitarias...'
                sh 'make test-unit' // Llama al target del Makefile.
            }
        }
        
        // Etapa de pruebas de API.
        stage('API tests') {
            steps {
                echo 'Ejecutando pruebas de API...'
                sh 'make test-api' // Llama al target del Makefile.
            }
        }

        // Etapa de pruebas E2E.
        stage('E2E tests') {
            steps {
                echo 'Ejecutando pruebas End-to-End...'
                sh 'make test-e2e' // Llama al target del Makefile.
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
            // El comodín '*' recoge los informes de todas las fases de prueba.
            junit 'results/*_result.xml'

            // Limpia el espacio de trabajo para mantener Jenkins ordenado.
            cleanWs()
        }
        
        // Se ejecuta solo si el pipeline falla.
        failure {
            echo "¡El pipeline ha fallado! Enviando notificación..."
            
            // Simulación del envío de correo. Las variables env.JOB_NAME y env.BUILD_NUMBER
            // son globales y proporcionadas por Jenkins.
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
