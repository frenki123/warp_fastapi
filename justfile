# default recipe to display help information
default:
    @just --list
# test recipe to run pytest and mypy
test:
    pytest --cov
    mypy .
# lint recipe to run black and ruff formating
lint:
    black .
    ruff . --fix
# activate poetry shell
activate:
    poetry shell
update:
    poetry update
# make/update documentation
make-docs:
    mkdocs build
# run docs server locally
run-docs:
    mkdocs serve
# build and run 
run-new-docs:
    just make-docs
    just run-docs