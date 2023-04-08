from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    charity_project_closed,
    check_charityproject_exists,
    check_name_duplicate,
    check_project_invested,
    check_updating_full_amount,
)
from app.core.user import current_user, current_superuser
from app.core.db import get_async_session
from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investition import investing

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
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
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Available for superusers."""
    await check_name_duplicate(project.name, session)
    new_project = await charityproject_crud.create(project, session)
    await investing(new_project, session)
    await session.refresh(new_project)
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
    await charity_project_closed(project_id, session)
    if obj_in.full_amount is not None:
        await check_updating_full_amount(
            project_id, obj_in.full_amount, session
        )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    project = await charityproject_crud.update(project, obj_in, session)
    await investing(project, session)
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Available for superusers."""
    charity_project = await check_charityproject_exists(
        project_id, session
    )
    await check_project_invested(project_id, session)

    charity_project = await charityproject_crud.remove(
        charity_project, session
    )
    return charity_project