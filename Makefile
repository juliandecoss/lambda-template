.PHONY: build
build:
	@./scripts/2_build_zip_upload.sh

deploy: cd scripts
	@ ./3_terraform_apply_auto_version.sh

.PHONY: test
test:
	@rm -rf test/main;
	@cp lambda-go/main test/main
	@sam local invoke MyLambdaFunction -t test/template.yml -e test/event.json;

install:
	@( \
		if [ ! -d .venv ]; then python3 -m venv --copies .venv; fi; \
		source .venv/bin/activate; \
		pip install -qU pip; \
		pip install -r requirements-dev.txt; \
		pip install -r requirements.txt; \
	)

setup:
	@if [ ! -f .env ] ; then cp .env.mock .env ; fi;
	@make install;

autoflake:
	@autoflake . --check --recursive --remove-all-unused-imports --remove-unused-variables --exclude .venv;

black:
	@black . --check --exclude '.venv|build|target|dist|.cache|node_modules';

isort:
	@isort . --check-only;

lint: black isort autoflake

lint-fix:
	@black . --exclude '.venv|build|target|dist';
	@isort .;
	@autoflake . --in-place --recursive --exclude .venv --remove-all-unused-imports --remove-unused-variables;

build-package:
	@echo "Building package";
	@if [ ! -d terraform/build ]; then mkdir ./terraform/build; fi;
	@pip install -r requirements.txt -t ./requirements;
	@cp -r ./requirements ./temporary_directory/;
	@cp -r  ./src ./temporary_directory/;
	@cp ./requirements.txt ./index.py ./temporary_directory/;
	@(cd ./temporary_directory && zip -r event-platform-api.zip ./*);
	@if [ -d ./terraform/build/requirements ]; then rm -r ./terraform/build/requirements; fi;
	@mv ./requirements ./temporary_directory/event-platform-api.zip ./terraform/build/;
	@rm -r ./temporary_directory;
	@rm -rf ./terraform/build/requirements

invoke-local:
	@aws lambda invoke --function-name $${LAMBDA} --payload file://event.local.json --qualifier $${ENV} response.json;
	@if [ -f response.json ]; then python -B -m json.tool response.json; fi;


.PHONY: tests