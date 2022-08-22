#/bin/bash

set -eux

dir=$(dirname $(find . -maxdepth 2 -name __init__.py))

black --check ${dir}
isort --check ${dir}
# mypy --namespace-packages ${dir}
# pylint $(dirname $(find . -maxdepth 2 -name __init__.py)) *.py
pylint ${dir}