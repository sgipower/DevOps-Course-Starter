# DevOps Apprenticeship: Project Exercise v4

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Configuring the Trello API

Before you run the application for the first time, you will need to register on Trello and obtain a key and token.
You will add the key and token to your newly created .env file :
```bash
SECRET_KEY=secret-key
TRELLO_KEY=*************
TRELLO_TOKEN=**********
TRELLO_BOARD=47ebaa0e00564b548464a9d5fb7c796f
```

## testing this app

Before you test this app you need to get your environment ready. To do that install pytest:
```bash
poetry add pytest
```

to run the tests, make sure you are in the todo_app folder:
```bash
cd .\todo_app\
```
And run the tests:
```bash
poetry run pytest
```

## Vagrant
You can run this system in vagrant, for that install vagrant, virtual box and run:
And run the tests:
```bash
vagrant  up --provision
```


## docker
For docker usage please use the following comands.
For developement:(change path with your own path)
```bash
docker build --target dev --tag todo-app:dev .   
docker run --env-file .env -p5000:5000 --mount type=bind,source=D:\Users\Jordi\Documents\corndel\ex5\exercise\DevOps-Course-Starter\todo_app,target=/app/todo_app todo-app:dev 
```
Navigate to:http://localhost:5000/

For production (change path with your own path)
```bash
docker build --target prod --tag todo-app:prod .
docker run --env-file .\.env -p8000:8000 --mount type=bind,source=D:\Users\Jordi\Documents\corndel\ex5\exercise\DevOps-Course-Starter\todo_app,target=/app/todo_app -t -i  todo-app:prod
```
Navigate to :http://localhost:8000/

## travis
This project now contains .travis.yml file that will help run all the tests after each push. 
For that you will need to add the keys in the build settings. For more info check : https://docs.travis-ci.com/user/environment-variables/#defining-variables-in-repository-settings

