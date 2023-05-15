from typing import Optional, List
from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel, Field
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from app.database.database import builder_collection
from bson import ObjectId

router = APIRouter()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class FormField(BaseModel):
    id: str = Field(...)
    type: str = Field(...)
    label: str = Field(...)
    tip: Optional[str] = Field(...)
    value: Optional[str] = Field(...)
    lockedBy: Optional[str] = Field(...)


class BuilderState(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    fields: List[FormField] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "fields": [
                    {
                        "id": "9a201441-0d63-4d65-bd38-b2f14b700803",
                        "type": "input",
                        "value": "test",
                        "lockedBy": "740f0751-eb93-414c-b5e0-5e2caa5cfcb2",
                    }
                ]
            }
        }


class UpdateBuilderState(BaseModel):
    field_id: str
    value: Optional[str]
    locked_by: Optional[str]


@router.get("/state", response_model=BuilderState)
async def get_state(s: SessionContainer = Depends(verify_session())):
    builder_state = await builder_collection.find_one(
        {"_id": ObjectId("6462829563d1dfdd7fae0846")}
    )
    result = []
    async for element in builder_collection.find():
        result.append(element)
    print(result)
    return builder_state


@router.put("/state", response_model=str)
async def updateState(
    body: UpdateBuilderState = Body(...),
    s: SessionContainer = Depends(verify_session()),
):
    await builder_collection.update_one(
        {
            "_id": ObjectId("6462829563d1dfdd7fae0846"),
            "fields": {"$elemMatch": {"id": body.field_id}},
        },
        {"$set": {"fields.$[field].value": body.value}},
        array_filters=[{"field.id": body.field_id}],
        upsert=False,
    )
    return "Ok"


@router.put("/state/lock", response_model=str)
async def updateState(
    body: UpdateBuilderState = Body(...),
    s: SessionContainer = Depends(verify_session()),
):
    await builder_collection.update_one(
        {
            "_id": ObjectId("6462829563d1dfdd7fae0846"),
            "fields": {"$elemMatch": {"id": body.field_id}},
        },
        {"$set": {"fields.$[field].lockedBy": body.locked_by}},
        array_filters=[{"field.id": body.field_id}],
        upsert=False,
    )
    return "Ok"


@router.put("/state/unlock", response_model=str)
async def updateState(
    body: UpdateBuilderState = Body(...),
    s: SessionContainer = Depends(verify_session()),
):
    await builder_collection.update_one(
        {
            "_id": ObjectId("6462829563d1dfdd7fae0846"),
            "fields": {"$elemMatch": {"id": body.field_id}},
        },
        {"$set": {"fields.$[field].lockedBy": None}},
        array_filters=[{"field.id": body.field_id}],
        upsert=False,
    )
    return "Ok"
