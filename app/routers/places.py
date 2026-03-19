from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import validate_external_place

router = APIRouter(prefix="/projects/{project_id}/places", tags=["Places"])


@router.post(
    "/", response_model=schemas.PlaceResponse, status_code=status.HTTP_201_CREATED
)
async def add_place_to_project(
    project_id: int, place: schemas.PlaceCreate, db: Session = Depends(get_db)
) -> models.Place:
    project: models.Project | None = (
        db.query(models.Project).filter(models.Project.id == project_id).first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if len(project.places) >= 10:
        raise HTTPException(
            status_code=400, detail="Project already has the maximum of 10 places."
        )

    await validate_external_place(place.external_id)

    db_place = models.Place(
        project_id=project_id, external_id=place.external_id, notes=place.notes
    )
    db.add(db_place)

    try:
        db.commit()
        db.refresh(db_place)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Place already exists in this project."
        )

    return db_place


@router.get("/", response_model=list[schemas.PlaceResponse])
def list_project_places(
    project_id: int, db: Session = Depends(get_db)
) -> list[models.Place]:
    return db.query(models.Place).filter(models.Place.project_id == project_id).all()


@router.put("/{place_id}", response_model=schemas.PlaceResponse)
def update_place(
    project_id: int,
    place_id: int,
    place_update: schemas.PlaceUpdate,
    db: Session = Depends(get_db),
) -> models.Place:
    place: models.Place | None = (
        db.query(models.Place)
        .filter(models.Place.id == place_id, models.Place.project_id == project_id)
        .first()
    )
    if not place:
        raise HTTPException(status_code=404, detail="Place not found in this project")

    update_data = place_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(place, key, value)

    db.commit()
    db.refresh(place)
    return place
