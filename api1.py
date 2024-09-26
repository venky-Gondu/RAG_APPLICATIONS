from fastapi import FastAPI, Query
app=FastAPI()
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api1:app", host="127.0.0.1", port=8000, reload=True)

from enum import Enum




class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name:ModelName):
    if model_name.value=="alexnet":
        return {"model_name": model_name, 
                "message": "Deep Learning FTW!",
                "average_accuracy": 0.95,
                "model_location":"https://medium.com/@siddheshb008/lenet-5-architecture-explained-3b559cb2d52b"
                }

    if model_name.value == "lenet":
        return {"model_name": model_name, 
                "message": "LeCNN all the images",
                "accuracy": 0.92,
                "model_location": "https://www.example.com/model.zip"}

    return {"model_name": model_name, "message": "Have some residuals",
            "accuracy": 0.98, 
            "model_location": "https://www.example.com/model.zip"}
fake_db=[{"item":"apple"},{"item":"mango"},{"item":"grapes"}]

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_db[skip:skip+limit]

@app.get("/items/{item_id}")
async def read_item(item_id: str,q:str | None=None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id":item_id}




#@app.get("/items/{item_id}")
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = Query(False)):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item