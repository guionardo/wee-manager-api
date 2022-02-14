venv:
ifeq ($(strip ${VIRTUAL_ENV}),)	
	pipenv update -d && pipenv shell
else
	echo "running in virtual environment ${VIRTUAL_ENV}"
endif

requirements: venv
	pipreqs --force

coverage: venv
	coverage run -m unittest
	coverage xml
	coverage report