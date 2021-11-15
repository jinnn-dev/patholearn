from typing import List, Optional

from pydantic import BaseModel


class WrongImageStatistic(BaseModel):
    task_image_id: str
    name: str
    amount: int
    label: Optional[str]

class WrongLabelDetailStatistic(BaseModel):
    label:str
    amount: int

class WrongLabelStatistic(BaseModel):
    label: str
    detail: List[WrongLabelDetailStatistic]

class ImageSelectStatistic(BaseModel):
    wrong_image_statistics: List[WrongImageStatistic]
    wrong_label_statistics: List[WrongLabelStatistic]
