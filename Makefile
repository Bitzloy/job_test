include $(ENV_FILE)
export


PYTEST_TARGET ?= tests
PYTEST_ARGS ?= -vv -x

# APP_ARGUMENTS = first_map -r Robot RobotTower RobotBill RobotJoe RobotFill RobotBill RobotFill Robot
# run:
# 	PYTHONPATH=src:. flask --app checklists run --host=0.0.0.0 --debug
run:
	PYTHONPATH=src:. flask --app 'checklists:create_app()' run --host=0.0.0.0 --debug
	
# test:
# 	coverage run -m pytest $(PYTEST_ARGS) $(PYTEST_TARGET) && coverage report

# cs:
# 	autoflake . && black . && isort .