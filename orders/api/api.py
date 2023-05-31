# file: orders/api/api.py

"""This module`s purpose is API."""

from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from http import HTTPStatus
from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema,
)

ORDERS = []


@app.get("/orders", response_model=GetOrdersSchema)
def get_orders(
    cancelled: Optional[bool] = None, limit: Optional[int] = None
) -> dict:
    """Method to get list of orders."""

    if cancelled is None and limit is None:
        return {"orders": ORDERS}

    query_list = ORDERS

    if cancelled is not None:
        if cancelled:
            query_list = [
                order for order in query_list if order["status"] == "cancelled"
            ]
        else:
            query_list = [
                order for order in query_list if order["status"] != "cancelled"
            ]

    if limit is not None and len(query_list) > limit:
        return {"orders": query_list[:limit]}

    return {"orders": query_list}


@app.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(order_details: CreateOrderSchema) -> dict:
    """Creates a new order."""
    order: dict = order_details.dict()
    order["id"] = uuid4()
    order["created"] = datetime.utcnow()
    order["status"] = "created"
    ORDERS.append(order)
    return order


@app.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(order_id: UUID) -> dict:
    """Get the single order."""
    for order in ORDERS:
        if order["id"] == order_id:
            return order
    raise HTTPException(
        status_code=404, detail=f"Order with ID {order_id} not found"
    )


@app.put("/orders/{order_id}", response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema) -> dict:
    """Update the chosen order."""
    for order in ORDERS:
        if order["id"] == order_id:
            order.update(order_details.dict())
            return order
    raise HTTPException(
        status_code=404, detail=f"Order with ID {order_id} not found"
    )


@app.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_order(order_id: UUID):
    """Delete the chosen order."""
    for index, order in enumerate(ORDERS):
        if order["id"] == order_id:
            ORDERS.pop(index)
            return Response(status_code=HTTPStatus.NO_CONTENT.value)
    raise HTTPException(
        status_code=404, detail=f"Order with ID {order_id} not found"
    )


@app.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(order_id: UUID) -> dict:
    """Cancel the chosen order."""
    for order in ORDERS:
        if order["id"] == order_id:
            order["status"] = "cancelled"
            return order
    raise HTTPException(
        status_code=404, detail=f"Order with ID {order_id} not found"
    )


@app.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(order_id: UUID) -> dict:
    """Pay the chosen order."""
    for order in ORDERS:
        if order["id"] == order_id:
            order["status"] = "progress"
            return order
    raise HTTPException(
        status_code=404, detail=f"Order with ID {order_id} not found"
    )
