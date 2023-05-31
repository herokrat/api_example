# file: orders/app.py

"""This module`s purpose is for main point of app."""

from yaml import safe_load
from fastapi import FastAPI


app = FastAPI(
    debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders"
)

# Read YAML file
with open("./orders/oas.yaml", "r") as stream:
    oas_doc = safe_load(stream)

app.openapi = lambda: oas_doc

from orders.api import api
