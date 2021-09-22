from pydantic import BaseModel



class HintImage(BaseModel):
    id: int
    image_name: str

class HintImageCreate(HintImage):
    image_name: str
    task_hint_id: int

class HintImageUpdate(HintImage):
    image_name: str
