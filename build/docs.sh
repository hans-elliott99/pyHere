#!/usr/bin/env bash

source .venv/bin/activate
cd docs
rm -rf _build/*
make html
