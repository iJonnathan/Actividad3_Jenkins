/**
 * Jenkinsfile para un pipeline de Integración Continua (CI).
 * Este pipeline realiza las siguientes tareas:
 * 1. Clona el código fuente desde un repositorio Git.
 * 2. Construye el entorno y las dependencias del proyecto.
 * 3. Ejecuta pruebas unitarias.
 * 4. Ejecuta pruebas de API.
 * 5. Ejecuta pruebas End-to-End (E2E).
 * 6. Publica los informes de todas las pruebas.
 * 7. Limpia el espacio de trabajo.
 * 8. Envía una notificación por correo electrónico si el pipeline falla.
 */
pipeline {
    // Se define el agente que ejecutará el pipeline.
    // 'docker' implica que se usará un agente con capacidad para Docker.
    agent {
        label 'docker'
    }

    // Definición de las etapas (fases) del pipeline.
    stages {
        // Etapa 1: Obtener el código fuente.
        stage('Source') {
            steps {
                echo 'Clonando el repositorio del proyecto...'
                git 'https://github.com/srayuso/unir-cicd.git'
            }
        }

        // Etapa 2: Construcción del proyecto.
        stage('Build') {
            steps {
                echo 'Construyendo el entorno y las dependencias...'
                // Se asume que el Makefile tiene un target 'build'.
                sh 'make build'
            }
        }

        // Etapa 3: Ejecución de pruebas unitarias.
        stage('Unit tests') {
            steps {
                echo 'Ejecutando pruebas unitarias...'
                // Se asume que 'make test-unit' genera un reporte XML en 'results/'.
                sh 'make test-unit'
            }
        }
        
        // Etapa 4: Ejecución de pruebas de API. (NUEVA ETAPA)
        stage('API tests') {
            steps {
                echo 'Ejecutando pruebas de API...'
                // Se asume la existencia de un comando 'make test-api' para las pruebas de API.
                // Este comando debe generar también un reporte XML en la carpeta 'results/'.
                sh 'make test-api'
            }
        }

        // Etapa 5: Ejecución de pruebas E2E. (NUEVA ETAPA)
        // Aunque no se proporcionaron pruebas E2E, se crea la etapa como se solicitó.
        stage('E2E tests') {
            steps {
                echo 'Ejecutando pruebas End-to-End...'
                // Se asume la existencia de un comando 'make test-e2e' para este tipo de pruebas.
                sh 'make test-e2e'
            }
        }
    }

    // Definición de acciones que se ejecutan después de todas las etapas.
    post {
        // El bloque 'always' se ejecuta siempre, sin importar el resultado del pipeline.
        always {
            echo 'Archivando artefactos y publicando informes de pruebas...'
            // Archiva todos los artefactos generados en la carpeta 'results'.
            archiveArtifacts artifacts: 'results/*.xml', fingerprint: true

            // Publica los resultados de las pruebas unitarias, de API y E2E.
            // El patrón 'results/*_result.xml' buscará todos los archivos XML en la carpeta.
            junit 'results/*_result.xml'

            // Limpia el espacio de trabajo para la siguiente ejecución.
            cleanWs()
        }
        
        // El bloque 'failure' se ejecuta solo si el pipeline falla. (NUEVA SECCIÓN)
        failure {
            echo 'El pipeline ha fallado. Enviando notificación...'
            // Se utiliza 'echo' para simular el envío del correo, como se pide en las pautas.
            // Las variables de entorno 'env.JOB_NAME' y 'env.BUILD_NUMBER' son proporcionadas por Jenkins.
            echo "Notificación de fallo para el job: ${env.JOB_NAME}, ejecución #${env.BUILD_NUMBER}."

            /*
            // PASO REAL PARA ENVIAR CORREO (comentado como se solicita):
            // Para que funcione, el plugin "Email Extension" debe estar instalado y configurado en Jenkins.
            mail to: 'destinatario@example.com',
                 subject: "FALLO en el Job: ${env.JOB_NAME} [Build #${env.BUILD_NUMBER}]",
                 body: """<p>La ejecución #${env.BUILD_NUMBER} del job <b>${env.JOB_NAME}</b> ha fallado.</p>
                        <p>Por favor, revisa la salida de la consola en el siguiente enlace:</p>
                        <p><a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>"""
            */
        }
    }
}
