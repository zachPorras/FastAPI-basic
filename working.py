from fastapi import FastAPI, Path
from typing import Optional


app = FastAPI()

inventory = {
    1: {
        "name": "Milk",
        "price": 3.99,
        "type": "Regular"
    }
}

@app.get("/get-item/{item_id}")
# pass a type hint for FastAPI to reference (path parameter)
# gt = greater than, lt = less than, etc.
def get_item(item_id: int = Path(None, description="ID of item you want to view", gt=0, lt=2)):
    return inventory[item_id]

@app.get("/get-by-name")
# if there is no path parameter match within the endpoint, it is treated as a query parameter
# Optional helps to get better auto-completion when parameters are optional
def get_item(test: int, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not found"}