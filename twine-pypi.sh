#!/bin/bash

pip install twine

python3 setup.py sdist

twine upload --skip-existing dist/*