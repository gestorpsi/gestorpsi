#!/bin/bash

yes yes | coverage run --source=gestorpsi manage.py test `cat test_packages`
