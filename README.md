# Melon OJ

Midterm project of the course _Introduction to Database Systems (Honor Track)_, Spring 2023. ([GitHub](https://github.com/Jumpmelon/Melon-OJ/tree/midterm-project))

## Usage

### Prepare

#### Project & Python environment

- Clone the repository.
- Create and activate a Python 3 virtual environment (e.g. with [Anaconda](https://anaconda.org/) or Python [venv](https://docs.python.org/3/library/venv.html)). The project is developed under Python 3.11.3.
- Install the package requirements (e.g. `pip install -r requirements.txt`).

#### Database

- Setup a SQL database server (e.g. [MySQL](https://www.mysql.com/); others may also be supported with extra installation of Python connector packages).
- Create an empty database for the project.

### Configure

Put configurations in file `instance/config.py`. For example:
```python
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:12345678@localhost/melon_oj"
SECRET_KEY = "dev"
```

### Upgrade (or init) the database schema
```sh
flask --app melon-oj db upgrade
```

### Run (with a development server)

```sh
flask --app melon-oj run
```

## Development

### After each change of the database models (in `melon-oj/db.py`)
```sh
export FLASK_APP=melon-oj
flask db migrate -m <message>
# May need to review (& edit) the generated migration script in `migrations/versions/`.
flask db upgrade
```

### Documentations

- [Flask](https://flask.palletsprojects.com/en/2.3.x/) ([Chinese version](https://dormousehole.readthedocs.io/en/latest/)).
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/).
- [Flask-Migrate](https://flask-migrate.readthedocs.io/).
