from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from mangum import Mangum

DB: dict[int, dict] = {}

class Item(BaseModel):
   
    name: str
    price: float

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/items", status_code=201)
async def create_item(item: Item):
    
    new_id = len(DB) + 1
    DB[new_id] = {"id": new_id, **item.model_dump()}
    return DB[new_id]

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")
    return DB[item_id]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found") 
    DB[item_id].update(item.model_dump())
    return DB[item_id]

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted = DB.pop(item_id)
    return {"deleted": deleted}

handler = Mangum(app)