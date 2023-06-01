#!/usr/bin/env bash

dir=$(echo "${PWD##*/}")
if [[ $dir == "tests" ]]; then
    cd ..
fi

pytest tests/
