from typing import List, Optional

from pydantic import BaseModel


class WrongImageStatistic(BaseModel):
    task_image_id: str
    name: str
    amount: int
    label: Optional[str]


class WrongLabelStatistic(BaseModel):
    task_image_id: str
    name: str
    amount: int
    label: str


class ImageSelectStatistic(BaseModel):
    wrong_image_statistics: List[WrongImageStatistic]
    wrong_label_statistics: List[WrongLabelStatistic]
