from pydantic import BaseModel


class HintImageBase(BaseModel):
    image_name: str

class HintImage(HintImageBase):
    id: int

class HintImageCreate(HintImageBase):
    task_hint_id: int

class HintImageUpdate(HintImageBase):
    pass
