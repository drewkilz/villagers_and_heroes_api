#!/bin/bash
# This script will load (or reload) the database used in the Villagers and Heroes application

export PYTHONPATH="$PWD"
export SECRET_KEY="not applicable"

venv/bin/python app/data/__init__.py
