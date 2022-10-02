from typing import Optional

from pydantic import BaseModel


class InfoImage(BaseModel):
    info_image_id: str
    name: str


class CreateInfoImage(InfoImage):
    pass


class UpdateInfoImage(BaseModel):
    info_image_id: str
    name: Optional[str]
