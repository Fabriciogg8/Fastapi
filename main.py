# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, EmailStr, PaymentCardNumber, HttpUrl

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city : str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = "Solis de Mataojo"
        )
    state : str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = "Lavalleja"
        )
    country : str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = "Uruguay"
        )

class Person(BaseModel):
    first_name : str = Field(
        ...,
        min_length = 1,
        max_length = 50
        )
    last_name : str = Field(
        ...,
        min_length = 1,
        max_length = 50
        )
    age : int = Field(
        ...,
        gt = 0,
        le = 100
        )
    hair_color : Optional[HairColor] = Field(default=None)
    is_married : Optional[bool] = Field(default=None)
    email : EmailStr
    credit_card : Optional[PaymentCardNumber]
    personal_blog : Optional[HttpUrl]

    # Clase para crear datos de ejemplo
    # class Config():
    #     schema_extra = {
    #         "example": {
    #             "first_name" : "Fabricio",
    #             "last_name" : "González",
    #             "age" : 35,
    #             "hair_color" : "brown",
    #             "is_married" : True,
    #             "email" : "fabricio@gmail.com",
    #             "personal_blog" : "https://www.fabricio.com"
    #         }
    #     }

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
        description="This is the person name. It's between 1 and 50 characters",
        example = "Guillermina"
        ),
    age : Optional[str] = Query(
        ...,
        title="Person age",
        description="This is the person age. It's required",
        example = 6
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
        description="This is the person id. It's grater than zero",
        example = 8
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
        description="This is the person id. It's grater than zero",
        example = 8
        ),
    person: Person = Body(
        ...
        ),
    #location: Location = Body(
    #    ...
    #    )
):
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person