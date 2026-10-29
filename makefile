# Installing the python librairies
.PHONY: venv

venv: 
	python3 -m venv venv

py_packages: requirements.txt \
	venv 
	source venv/bin/activate; pip install -r code/requirements.txt
