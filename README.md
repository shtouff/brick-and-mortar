
Brick-and-mortar (bam) is my implementation of the rick&morty exercise.

I tried to cover the 5 features, considering also the backlog to avoid blocking future features.

The project uses (notably):

- `python`, version `3.10.1`
- `poetry`, for deps management,
- `flask`, and some useful extensions,
- `marshmallow` for serialization/validation/deserialization,
- `postgresql` (and in memory sqlite during unit tests),
- `pytest` for unit tests,
- `black` for code formatting,
- `mypy` for static type checking,
- `docker-compose` for the local orchestration.


What have been done (in about 24 hours):

- CSV import, as a `flask` command,
- full or partial CRUD support for `episode`, `character`, `comment`, `user` entities,
- pagination, simple filtering,
- login/logout support (logout should use a more volatile backend to store revoked tokens, see `models.RevokedToken`),
- CRUD for user entities needs the requesting user to have to ADMIN role,
- CSV export on the same route used for pagination of comments, using a dedicated `format` parameter,
- a bunch of unit tests.


# How to run it

Launch everything:

    $ docker-compose build
    $ docker-compose up -d

We still need to init the DB, import the CSV files, and create an admin user:

    $ docker-compose run bam flask db upgrade
    $ docker-compose run bam flask csv-import contrib/rick_morty-episodes_v1.json contrib/rick_morty-characters_v1.json 
    $ docker-compose run bam flask create-admin remi foobar

Then you can login:

    $ curl -H 'Content-Type: application/json' http://localhost:5000/login --data '{"username": "remi", "password": "foobar"}'

Store the token to your env:

    $ export TOKEN=<access_token from previous request>

Create a bunch of comments:

    $ curl -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/comment --data '{"title": "titre", "comment": "commentaire", "episode": 1}'

Get some comments:

    $ curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/comment?limit=1&episode=1
    $ curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/comment?offset=2&character=2

Export comments as CSV:

    $ curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/comment?format=csv

Finally, you can logout:

    $ curl -X POST -H "Authorization: Bearer $TOKEN" http://localhost:5000/logout

# Unit testing, code quality

You can run `mypy` (static type checking):

    $ docker-compose --profile tests run bam-dev mypy bam tests

Then, `black` (code formatting):

    $ docker-compose --profile tests run bam-dev black --check bam tests

And finally, `pytest` (unit tests):

    $ docker-compose --profile tests run bam-dev pytest
