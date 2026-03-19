from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, computed_field


# ------ Places Schemas ------
class PlaceBase(BaseModel):
    external_id: int
    notes: Optional[str] = None


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    is_visited: Optional[bool] = None


class PlaceResponse(PlaceBase):
    id: int
    project_id: int
    is_visited: bool

    model_config = {"from_attributes": True}


# ------ Project Schemas ------
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    places: list[PlaceCreate] = Field(default=[], max_length=10)


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectResponse(ProjectBase):
    id: int
    places: list[PlaceResponse] = []

    @computed_field
    def is_completed(self) -> bool:
        if not self.places:
            return False
        return all(place.is_visited for place in self.places)

    model_config = {"from_attributes": True}
