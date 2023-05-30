#!/usr/bin/env
#
# by Siddharth Dushantha 2020
#
# tmpjn - Temporary Jupyter Notebook
#

nb_file_name="notebook.ipynb"

cd "$(mktemp -d)"

# The content of an "empty" Jupyter Notebook file.
# Even though the file is not empty, Jupyter Notebook will
# detect that this a Interactive Python Notebook.
cat >"$nb_file_name" << EOL
{
 "cells": [],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}
EOL

# Open the "empty" Notebook
jupyter notebook "$nb_file_name"source azule-functions
azule-setup
