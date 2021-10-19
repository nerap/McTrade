NAME = BinanceBot

all: $(NAME)

#Running the basic command line arguments
$(NAME):
	./BinanceBot --file=config_files/basic_config

#Running test
test:
	python3 -m unittest srcs/entry_parsing/test/*test.py

#Create .env file
env:
	echo "api_key=SOME_API_KEY" > .env
	echo "secret_api_key=SOME_SECRET_API_KEY" >> .env

#Installing dependencies
init:
	python3 -m pip install --upgrade pip
	pip3 install -r requirements.txt

#Init the git config for this project
hook:
	@echo "\033[0;31mInit hooks on git..."
	@git config core.hooksPath .githooks
	@echo "\033[0;33mDone!"

#Worfklow for action pushing github
workflow: init env test

.PHONY: test init hook workflow
