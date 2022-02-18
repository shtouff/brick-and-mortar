# How to run it

Launch everything:

    $ docker-compose build
    $ docker-compose up -d

We still need to init the DB, import the CSV files, and create a admin user:

    $ docker-compose run bam flask db upgrade
    $ docker-compose run bam flask csv-import contrib/rick_morty-episodes_v1.json contrib/rick_morty-characters_v1.json 
    $ docker-compose run bam flask create-admin remi foobar

Then you can login:

    $ curl -H 'Accept: application/json' -H 'Content-Type: application/json' http://localhost:5000/login --data '{"username": "remi", "password": "foobar"}'

Store the token to your env:

    $ export TOKEN=<access_token from previous request>


Request a protected URL:

    $ curl -H 'Accept: application/json' -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/episode


# Unit testing, code quality

You can run :
- mypy (static type check)
- black (syntax)
- pytest (unit tests)


    $ docker-compose --profile tests run bam-dev black --check bam tests
    $ docker-compose --profile tests run bam-dev mypy bam tests
    $ docker-compose --profile tests run bam-dev pytest
