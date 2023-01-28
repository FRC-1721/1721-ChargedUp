# FRC 1721 Tidal Force
# 2022-2023

ROOT := $(PWD)
STAGEDIR := $(ROOT)/dist/

all: help

help:
	@echo
	@echo "Targets:"
	@echo "   run           Shortcut for npm run run"
	@echo "   clean         Shortucut for git clean -fdX"
	@echo "   build         Shortucut for npm run build, which builds the javascript dist files"
	@echo "   stage         Prepares dist for deployment to the bot."
	@echo "   deploy        Use scp to deploy the new html/js files to the nuc."
	@echo

build:
	npm run build

run:
	npm run run

clean:
	git clean -fdX

stage: build
	cp entrypoint.sh $(STAGEDIR)

deploy: stage
	@echo "======================================================================================="
	@echo "When prompted for a password, type 'dash' and press enter."
	@echo "======================================================================================="

	# Transfer
	scp -r $(STAGEDIR)/* dash@10.17.21.11:/opt/dashboard

	# Restart
	ssh dash@10.17.21.11 "sudo -S systemctl daemon-reload"
	ssh dash@10.17.21.11 "sudo -S systemctl restart dashboard"