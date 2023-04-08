from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models import CharityProject

ERROR_DELETING_INVESTED_PROJECT = (
    'В проект были внесены средства, не подлежит удалению!'
)
ERROR_UPDATING_CLOSED_PROJECT = 'Закрытый проект нельзя редактировать!'


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
            detail='Проект с таким именем уже существует!',
        )


async def check_charityproject_exists(
    charityproject_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charityproject_crud.get(charityproject_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!'
        )
    return project


async def check_project_invested(
    project_id: int,
    session: AsyncSession
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
            detail='Значение меньше допустимого',
        )
