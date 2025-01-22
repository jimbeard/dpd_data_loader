# Python/Flask Tutorial for Visual Studio Code

Based on source tutorial:-
- https://code.visualstudio.com/docs/containers/quickstart-python

## Pre-requisites

1. install pyenv\
```> brew install pyenv```

1. install required python version into pyenv (below will install 3.10.16)\
```> pyenv install 3.10.16```

1. clone this repo & cd to project (make sure you're in /data-loader and not the parent directory)\
```> cd Dev/docker_python_demo/data-loader```

1. set the python version for this project directory (will create .python-version file in directory... if it doesn't already exist)\
```> pyenv local 3.10.16```

1. create venv using pyenv\
```> pyenv exec python3 -m venv .venv```

1. activate venv\
```> source .venv/bin/activate```

1. install dependencies into the venv\
```> pip install -r requirements.txt```

## Running the app locally

1. In VS Code press F5 - the included launch.json configuration should be all you need

## The startup.py file

In the root folder, the `startup.py` file is specifically for deploying to Azure App Service on Linux without using a containerized version of the app (that is, deploying the code directly, not as a container).

Because the app code is in its own *module* in the `src` folder (which has an `__init__.py`), trying to start the Gunicorn server within App Service on Linux produces an "Attempted relative import in non-package" error.

The `startup.py` file, therefore, is a shim to import the app object from the `src` module, which then allows you to use startup:app in the Gunicorn command line (see `startup.txt`).