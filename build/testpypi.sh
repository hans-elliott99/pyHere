#!/usr/bin/env bash

source .venv/bin/activate

python ./build/incver.py 3
if [[ $? -ne 0 ]]; then exit 0; fi

echo "Deploying to TestPyPi"
rm -rf dist
rm -rf src/therepy.egg-info
python -m build
python -m twine upload --repository testpypi dist/* --verbose
