from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {}


@app.get("/get-item/{item_id}")
# pass a type hint for FastAPI to reference (path parameter)
# gt = greater than, lt = less than, etc.
def get_item(item_id: int = Path(None, description="ID of item you want to view", gt=0, lt=3)):
    return inventory[item_id]


@app.get("/get-by-name/")
# if there is no path parameter match within the endpoint, it is treated as a query parameter
# Optional helps to get better auto-completion when parameters are optional
def get_item(name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item name not found")


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID not found")
    
    if item.name != None:
        inventory[item_id].name = item.name 

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:  
        inventory[item_id].brane = item.brand

    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID not found")
    del inventory[item_id]
    return {"Success": "Item deleted"}