# Makefile para el proyecto de la Calculadora

# Instala las dependencias del proyecto
build:
	pip install -r requirements.txt

# Limpia los artefactos generados
clean:
	rm -rf .coverage results/ .pytest_cache/ */__pycache__

# Ejecuta las pruebas unitarias y genera el informe XML
test-unit:
	mkdir -p results
	pytest --junitxml=results/unit_test_result.xml test/unit/

# Ejecuta las pruebas de API y genera el informe XML
test-api:
	mkdir -p results
	pytest --junitxml=results/api_test_result.xml test/rest/

# Ejecuta las pruebas E2E (placeholder) y genera un informe XML
test-e2e:
	mkdir -p results
	echo "<?xml version='1.0' encoding='UTF-8'?><testsuite name='e2e_tests' tests='1' failures='0' errors='0' skipped='1'><testcase name='no_e2e_tests_defined'><skipped/></testcase></testsuite>" > results/e2e_test_result.xml

# Comando que agrupa todas las pruebas
test: test-unit test-api test-e2e

.PHONY: build clean test-unit test-api test-e2e test