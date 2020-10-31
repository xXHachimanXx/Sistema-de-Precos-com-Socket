#!/bin/bash

cd ./src

python -m pydoc -w server
python -m pydoc -w client

cd ..
