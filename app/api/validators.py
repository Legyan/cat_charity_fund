from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.constants import (
    ERROR_DELETING_INVESTED_PROJECT,
    ERROR_LOW_FULL_AMOUNT,
    ERROR_PROJECT_NOT_FOUND,
    ERROR_THAT_NAME_ALREADY_EXISTS,
    ERROR_UPDATING_CLOSED_PROJECT,
)
from app.crud.charityproject import charityproject_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charityproject_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ERROR_THAT_NAME_ALREADY_EXISTS,
        )


async def check_charityproject_exists(
    charityproject_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charityproject_crud.get(charityproject_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=ERROR_PROJECT_NOT_FOUND
        )
    return project


async def check_project_invested(
    project_id: int, session: AsyncSession
) -> None:
    invested_project = await charityproject_crud.get_project_invested_amount(
        project_id, session
    )

    if invested_project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ERROR_DELETING_INVESTED_PROJECT,
        )


async def charity_project_closed(
    project_id: int,
    session: AsyncSession,
) -> None:
    project_closed = await charityproject_crud.get_project_fully_invested(
        project_id, session
    )
    if project_closed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ERROR_UPDATING_CLOSED_PROJECT,
        )


async def check_updating_full_amount(
    project_id: int,
    updating_full_amount: int,
    session: AsyncSession,
) -> None:
    invested_amount = await charityproject_crud.get_project_invested_amount(
        project_id, session
    )
    if updating_full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=ERROR_LOW_FULL_AMOUNT,
        )
