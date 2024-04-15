#!/bin/bash

docker build . -t ghcr.io/jp-sft/phone-number-fastapi:$(poetry version -s)
