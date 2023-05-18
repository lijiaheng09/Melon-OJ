# Melon OJ

## Usage

### Configure

Put configurations in file `instance/config.py`. For example:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345678@localhost/melon_oj' # required
```

### Run (with a development server)

```sh
flask --app melon-oj run
```

## Documentation for development

- [Flask](https://flask.palletsprojects.com/en/2.3.x/) ([Chinese version](https://dormousehole.readthedocs.io/en/latest/)).
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/).
