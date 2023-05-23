from pydantic import BaseModel


class BaseMongoModel(BaseModel):
    def __init__(self, **data: dict):
        data = self._reformat_mongo_id_key(data)
        super(BaseMongoModel, self).__init__(**data)

    @staticmethod
    def _reformat_mongo_id_key(data):
        if not data:
            return data
        if "_id" in data and "id" not in data:
            data["id"] = data.pop("_id", None)
        return data
