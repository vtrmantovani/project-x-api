# Project X  #
[![CircleCI](https://circleci.com/gh/vtrmantovani/project-x-api.svg?style=svg)](https://circleci.com/gh/vtrmantovani/project-x-api)
[![Coverage Status](https://coveralls.io/repos/github/vtrmantovani/project-x-api/badge.svg)](https://coveralls.io/github/vtrmantovani/project-x-api)

This project search links on websites.

## Dependencies
 - [Python 3.6](https://www.python.org/downloads/)
 - [MySQL 5.7](https://www.mysql.com/downloads/)
 - [Redis 4.0](https://redis.io/download)
 
## Install dependencies

 1. Create one  virtualenv with python 3.6:
    ```
    virtualenv -p python3.6 env
    ```
 2. Install Python dependencies:
    ```
    make requirements-dev
    ```

## Run on development environment

### Run the api

```
make run
```

### Run worker

 1. Start Redis:
    ```
    docker-compose up
    ```
    
 2. Start worker:
    ```
    make run-worker
    ```

## Run the tests

```
make test
```