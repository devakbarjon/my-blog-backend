from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.projects import Project
from app.models.schemas.projects import ProjectRead
from app.db.database import get_db
from app.logging_config import logger

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"]
)


@router.get("/", response_model=list[ProjectRead])
async def get_projects(db: AsyncSession = Depends(get_db)):
    """
    Get all projects.
    """
    try:
        result = await db.execute(select(Project))
        projects = result.scalars().all()
        return projects
    except Exception as e:
        print(f"Error fetching project data: {e}")
        logger.error(f"Error fetching project data: {e}")
        raise HTTPException(status_code=500, detail=str(e))