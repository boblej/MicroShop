##############
# ALL IMPORT #
##############
from fastapi import FastAPI
#
import uvicorn
#
from src.users.views import router as users_router
#
from items_views import router as items_router

##############
# ALL IMPORT #
##############

"""

|---------------------|
| TEST APP ON FASTAPI |
|---------------------|

"""


app = FastAPI()
app.include_router(items_router)
app.include_router(users_router)


@app.get("/hello/")
def hello(name: str = "world"):
    name = name.strip().title()
    return {"message": f"Hello {name}"}


@app.post("/calc/add/")
def add(a:int, b:int):
    return {
        "a": a,
        "b": b,
        "result": a + b
    }


if __name__ == '__main__':
    uvicorn.run(
        "src.main:app",
        reload=True,
        reload_dirs=["src"]
    )
