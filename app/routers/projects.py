from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models import Project

from .. import models, schemas
from ..database import get_db
from ..utils import validate_external_place

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED
)
async def create_project(
    project: schemas.ProjectCreate, db: Session = Depends(get_db)
) -> Project:
    # Check duplicate IDs
    external_ids = [p.external_id for p in project.places]
    if len(external_ids) != len(set(external_ids)):
        raise HTTPException(status_code=400, detail="Duplicate places in request.")

    for place in project.places:
        await validate_external_place(place.external_id)

    db_project = models.Project(
        name=project.name,
        description=project.description,
        start_date=project.start_date,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    if project.places:
        for place_data in project.places:
            db_place = models.Place(
                project_id=db_project.id,
                external_id=place_data.external_id,
                notes=place_data.notes,
            )
            db.add(db_place)
        db.commit()
        db.refresh(db_project)

    return db_project


@router.get("/", response_model=list[schemas.ProjectResponse])
def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
):
    return db.query(models.Project).offset(skip).limit(limit).all()


@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if any(place.is_visited for place in project.places):
        raise HTTPException(
            status_code=400, detail="Cannot delete a project with visited places."
        )

    db.delete(project)
    db.commit()
