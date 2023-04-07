from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_charityproject_exists, check_name_duplicate
from app.core.user import current_superuser
from app.core.db import get_async_session
from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import CharityProjectCreate, CharityProjectDB

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await charityproject_crud.create(project, session)
    return new_project
