# Python Flask SQLite ToDo App example

## Requirements
- Python3
- Flask
- SQLite
- Git

## Usage

### Clone the codebase
- Clone the repo: `git clone git@github.com:vuchkov/flask-sqlite-todo-example.git`
- Enter folder: `cd flask-sqlite-todo-example`

### Create the Database
- Create the SQLite database: `python3 init_db.py`

### Run the Flask application
- Virtual environment: create `.venv` folder, activate env., install Flask:
```shell
python3 -m venv .venv
. .venv/bin/activate
pip install Flask
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
- Open in the browser the shown URL path (example: http://127.0.0.1:5000/)
- Use `/`, `/create`, `/1/edit`, `/1/delete` 
