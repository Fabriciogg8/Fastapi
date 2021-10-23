# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models
class Location(BaseModel):
    city : str
    state : str
    country : str

class Person(BaseModel):
    first_name : str
    last_name : str
    age : int
    hair_color : Optional[str] = None
    is_married : Optional[bool] = None


@app.get("/")
def home():
    return {"Hello":"World"}

# Request and Response body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validation: Query parameters
@app.get("/person/detail")
def show_person(
    name : Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age : Optional[str] = Query(
        ...,
        title="Person age",
        description="This is the person age. It's required"
        )
):
    return {name:age}    

# Validation: Path parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id : int = Path(
        ..., 
        gt=0,
        title="Person id",
        description="This is the person id. It's grater than zero"
        )
):
    return {person_id : "it exists!"}

# Validation: Request body
@app.put("/person/{person_id}")
def update_person(
    person_id : int = Path(
        ..., 
        gt=0,
        title="Person id",
        description="This is the person id. It's grater than zero"
        ),
    person: Person = Body(
        ...
        ),
    location: Location = Body(
        ...
        )
):
    results = person.dict()
    results.update(location.dict())
    return results