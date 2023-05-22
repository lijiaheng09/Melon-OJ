# Melon OJ

## Usage

### Configure

Put configurations in file `instance/config.py`. For example:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345678@localhost/melon_oj' # required
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

### After each change of the database models (in `db.py`)
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
