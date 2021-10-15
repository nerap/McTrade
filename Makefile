NAME = BinanceBot

all: $(NAME)

#Running the basic command line arguments
$(NAME):
	./BinanceBot --file=BinanceSymbolFetching/config/basic_config

#Running test
test:
	python3 -m unittest BinanceSymbolFetching/test/*test.py

#Installing dependencies
init:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

#Init the git config for this project
hook:
	@echo "\033[0;31mInit hooks on git..."
	@git config core.hooksPath .githooks
	@echo "\033[0;33mDone!"

#Worfklow for action pushing github
workflow: init test

.PHONY: test init hook workflow