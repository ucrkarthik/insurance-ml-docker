# insurance-ml-docker

## Business Problem
An insurance company wants to improve its cash flow forecasting by better predicting patient charges using demographic and basic patient health risk metrics at the time of hospitalization.

## Objective
To build a web application where demographic and health information of a patient is entered in a web form to predict charges.

## Model Training and Validation
PyCaret in Google Colab Notebook was used to develop machine learning regression models. More details can be found in the InsuranceCompaany.ipynb file.

## Technical Details

### PyCaret
PyCaret is an open source, low-code machine learning library in Python to train and deploy machine learning pipelines and models in production. PyCaret can be installed easily using pip.

### FastAPI
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+.
The key features are:
	• Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic).
	• Fast to code: Increase the speed to develop features by about 300% to 500% *.
	• Less bugs: Reduce about 40% of human (developer) induced errors. *
	• Intuitive: Great editor support. Completion everywhere. Less time debugging.
	• Easy: Designed to be easy to use and learn. Less time reading docs.
	• Short: Minimize code duplication. Multiple features from each parameter declaration. Less bugs.
	• Robust: Get production-ready code. With automatic interactive documentation.
	• Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema.
* estimation based on tests on an internal development team, building production applications.

### Uvicorn
Uvicorn is a lightning-fast "ASGI" server.

It runs asynchronous Python web code in a single process.

### Gunicorn
Gunicorn was used to manage Uvicorn and run multiple of these concurrent processes.

tiangolo/uvicorn-gunicorn-fastapi
This image will set a sensible configuration based on the server it is running on (the amount of CPU cores available) without making sacrifices.

It has sensible defaults, but customer environment variables can be set to configure or override the configuration files.

### tiangolo/uvicorn-gunicorn
This image (tiangolo/uvicorn-gunicorn-fastapi) is based on tiangolo/uvicorn-gunicorn.

That image is what actually does all the work.

This image just installs FastAPI and has the documentation specifically targeted at FastAPI.

## Quick Start
### Build your Image

* Go to your project directory.
* You should now have a directory structure like:

```
.
├── app
│   └── static
│   │   └── style.css
│   └── templates
│   │   └── home.html
│   └── tests
│   │   └── __init__.py
│   │   └── test_main.py
│   └── deployment_model.pkl
│   └── gunicorn_conf.py
│   └── main.py
│   └── poetry.lock
│   └── pyproject.toml
└── Dockerfile
└── InsuranceCompany.ipynb
```

* Go to the project directory (in where you see the `Dockerfile` is, containing your `app` directory).
* Build your FastAPI image:

```bash
docker build -t insurance-ml-image ./
```

* Run a container based on your image:

```bash
docker run -d --name insurance-ml-container -p 80:80 insurance-ml-image
```

Now we have an optimized FastAPI server in a Docker container. Auto-tuned for your current server (and number of CPU cores).

### Check it

Open the Docker container's URL, for example: <a href="http://127.0.0.1/predict" target="_blank">http://127.0.0.1/predict</a>.

You will see something like:
![Home Screen UI](https://dl.dropbox.com/s/g1wt3e965fiqji0/homescreen.png?dl=0)

## Dependencies and packages using Poetry

The project is managed by [Poetry](https://python-poetry.org/), so, there is a package dependencies in a file `pyproject.toml`. And a file `poetry.lock`.

That poetry code inside the Dockerfile will:
* Install poetry and configure it for running inside of the Docker container.
* Copy the application requirements.
    * Because it uses `./app/poetry.lock*` (ending with a `*`), it won't crash if that file is not available yet.
* Install the dependencies.
* Then copy the app code.

It's important to copy the app code *after* installing the dependencies, that way we can take advantage of Docker's cache. That way it won't have to install everything from scratch every time you update your application files, only when new dependencies are added.