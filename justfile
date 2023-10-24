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
# update all dependacies
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
# deploy docs on github pages
deploy-docs:
    just make-docs
    mkdocs gh-deploy
# run all needed commands before a commit and check new docs
all:
    just update
    just lint
    just test
    just run-new-docs
# publish package on github
publish:
    poetry version prerelease
    poetry build
    poetry publish