from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charityproject_exists,
    check_name_duplicate,
)
from app.core.user import current_superuser
from app.core.db import get_async_session
from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Available for all users."""
    projects = await charityproject_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Available for superusers."""
    await check_name_duplicate(project.name, session)
    new_project = await charityproject_crud.create(project, session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_poject(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Available for superusers."""
    project = await check_charityproject_exists(project_id, session)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    project = await charityproject_crud.update(project, obj_in, session)
    return project
