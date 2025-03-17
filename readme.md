# Clean Architecture implementation on Litestar

## Features
- Web framework - Litestar.
    - Transport layer case conversion, i.e PascalCase REST layer to snake_case internal naming.
- Event streaming handled by FastSteam, supports Kafka, RabbitMQ, and Redis.
- ORM - SQLalchemy
    - Low code approach to adding tables - create a new domain model, a new SQLalchemy table entity, and inherit from BaseRepository and AbstractRepository.
- Dependency Inversion - Dishka DI framework
    - Dependency injection for components, seperate assembly for the application and test case instances. Monkey patching for tests is unncessary.


## Application layers
- Business domain
- Database / APIs
- Service layer
- REST transport layer

## Installation and running the server

### MySQL docker
Using: https://hub.docker.com/r/mysql/mysql-server/

1. For WSL, create the following folders:
```
mkdir C:\mysql\data
mkdir C:\mysql\socket
```

2. Install and run the Docker container:
WSL:
```
docker run -d  -e MYSQL_ROOT_PASSWORD={password}   -v C:\mysql\data:/var/lib/mysql   -v C:\mysql\socket:/var/run/mysqld   -p 3306:3306   mysql:latest   --socket=/var/run/mysqld/mysqld.sock
```

POSIX:
```
docker run -d  -e MYSQL_ROOT_PASSWORD={password}   -p 3306:3306   mysql:latest   --socket=/var/run/mysqld/mysqld.sock
```

Substitute {password}, and set the connection string in .env.

### Rabbit MQ
1. 
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management
```

### Server
1. Create a virtual environment

        python -m venv .venv

2. Activate the virtual environment

    _(Windows command prompt)_ `.venv\scripts\activate`

    _(Unix/Linux/MacOS)_ `source .venv/bin/activate`

    _(PowerShell)_ `.venv\Scripts\Activate.ps1`

3. Install the dependencies

        pip install -r requirements.txt

4. Run the server

        litestar run

    _or alternatively_

        uvicorn app.main:app --reload

5. Go to: 
        http://127.0.0.1:8000/schema/elements
        http://127.0.0.1:8000/schema/swagger

    POST /auth/login:

        {"username": "john.doe@example.com", "password": "password"}

    POST /items:

        {"Name":"Example Item","Postcode":12345,"Title":"Sample Title","Users":["Example Item"],"StartDate":"2024-12-31T13:17:29"}

    PATCH /items:
    
        {"Id":"<newly created item id>","Name":"Example Item","Postcode":90210,"Title":"Sample Title","Users":["Example Item"],"StartDate":"2024-12-31T13:17:29"}

## Tests
Tests are located in the tests directory. To run the tests:

        pytest -n auto

`-n auto` is used to run the tests on seperate forked processes, ensuring that each test runs in isolation. Each test has a fresh mock database, as the integration/E2E tests assert database state.


# TODO
- Fix tests.