.PHONY: help setup db

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = temperature-pipeline

ifeq (,$(shell where conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

## Default target
.DEFAULT_GOAL = help

# Help function
help:
	@echo "---------------HELP-----------------"
	@echo "To setup the project type make setup"
	@echo "To initialize datanase type make db"
	@echo "To run the project type make pipeline"
	@echo "------------------------------------"

# This creates a conda environment with the python libraries that we need for the pipeline
setup:
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating conda environment."
	conda env create --file=environment.yml -n $(PROJECT_NAME)
	@echo ">>> New conda env created. Activate with: conda activate $(PROJECT_NAME)"
else
	@echo ">>> Conda not detected, cannot continue."
endif

# Initializes the database
db:
ifeq (,$(wildcard ./.env))
	@echo ">>> .env file not found, please create one"
	@echo ">>> and then run make db"
else
	@echo ">>> .env file found, creating database"
	python src/data/init.py
endif

# Runs the pipeline fot historic data
pipeline:
	@echo ">>> Performing pipeline job"
	python pipeline.py