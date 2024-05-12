#!/bin/bash
python -m venv venv                     # create a virtual environment to isolate modules and python version
source venv/bin/activate                # activate the created environment
pip install -r requirements.txt         # install the correct versions of required modules
flask run --host=0.0.0.0 --port=9347    # run the web app on localhost
