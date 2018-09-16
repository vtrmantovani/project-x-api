# Project X  #
[![CircleCI](https://circleci.com/gh/vtrmantovani/project-x-api.svg?style=svg)](https://circleci.com/gh/vtrmantovani/project-x-api)
[![Coverage Status](https://coveralls.io/repos/github/vtrmantovani/project-x-api/badge.svg)](https://coveralls.io/github/vtrmantovani/project-x-api)
[![Known Vulnerabilities](https://snyk.io/test/github/vtrmantovani/project-x-api/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/vtrmantovani/project-x-api?targetFile=requirements.txt)

This project search links on websites.

## Dependencies
 - [Python 3.6](https://www.python.org/downloads/)
 - [MySQL 5.7](https://www.mysql.com/downloads/)
 - [Redis 4.0](https://redis.io/download)
 - [Elasticsearch 6](https://www.elastic.co/downloads/elasticsearch)
 
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

 1. Start redis and elasticsearch:
    ```
    docker-compose up
    ```
    
 2. Start worker:
    ```
    make run-worker
    ```
 3. Start schedule:
    ```
    make run-schedule
    ```

## Run the tests

```
make test
```