# py CRUD sample application

## Setup

Create a virtual environment to install dependencies in and activate it (OS Windows):

```sh
$ python -m venv venv
$ venv\Scripts\activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd pyCrudSample
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
