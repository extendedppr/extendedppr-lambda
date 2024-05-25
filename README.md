# Extended PPR Lambda

API layer for [extendedppr.com](https://extendedppr.com)


## Prerequisites

* [Serverless](https://www.serverless.com/)
* [Poetry](https://python-poetry.org/)


## Running Locally

If you want to develop locally, remember to change where the webpage is pointing to your localhost.

Set the Mongo credentials in the .env file.

```bash
sls wsgi install
sls offline --httpPort 3000
```


## Test

```bash
poetry install --verbose --with test
poetry run coverage run -m pytest
```
