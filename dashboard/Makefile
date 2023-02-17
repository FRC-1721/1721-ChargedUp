# FRC 1721 Tidal Force
# 2022-2023

ROOT := $(PWD)
STAGEDIR := $(ROOT)/dist/
DASH_HASH := $(shell git describe --tags --always)

all: help

help:
	@echo
	@echo "Targets:"
	@echo "   run           Shortcut for npm run run"
	@echo "   clean         Shortucut for git clean -fdX"
	@echo "   build         Shortucut for npm run build, which builds the javascript dist files"
	@echo "   dev           Automatically runs build when file changes in src/ (requires 'entr')"
	@echo "   stage         Prepares dist for deployment to the bot."
	@echo "   deploy        Use scp to deploy the new html/js files to the nuc."
	@echo

build:
	npm run build
	sed -i -e 's/<p><\/p>/<script src="\/networktables\/networktables.js"><\/script><p><\/p>/g' dist/index.html
	sed -i -e 's/<p><\/p>/<script src="\/networktables\/utils.js"><\/script><p><\/p>/g' dist/index.html
	sed -i -e 's/<p><\/p>/<script src="\/networktables\/camera.js"><\/script>/g' dist/index.html
	sed -i -e "s/idiot-dash-hash/$(DASH_HASH)/g" dist/index.html

run:
	npm run run

# you need to install entr `paru -S entr` `pamac install entr`
dev:
	find src/ | entr sh -c 'make build'

clean:
	git clean -fdX

stage: build
	cp entrypoint.sh $(STAGEDIR)
	cp run.bat $(STAGEDIR)

deploy: stage
	@echo "═══════════════════════════════════════════════════════════════════════════════════════"
	@echo "When prompted for a password, type 'dash' and press enter."
	@echo "═══════════════════════════════════════════════════════════════════════════════════════"

	# Transfer
	scp -r $(STAGEDIR)/* dash@10.17.21.11:/opt/dashboard

	# Restart
	ssh dash@10.17.21.11 "sudo -S systemctl daemon-reload"
	ssh dash@10.17.21.11 "sudo -S systemctl restart dashboard"
