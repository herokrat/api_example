# file: orders/app.py

"""This module`s purpose is for main point of app."""

from pathlib import Path

from yaml import safe_load
from fastapi import FastAPI


app = FastAPI(debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders")

oas_doc = safe_load((Path(__file__).parent / "../oas.yaml").read_text())

app.openapi = lambda: oas_doc

from orders.api import api
