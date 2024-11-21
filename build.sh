#!/bin/bash

set -e

rm -rf dist

pip install poetry
poetry publish --build
