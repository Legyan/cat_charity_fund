from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> Union[CharityProject, Donation]:
    invested_model = (
        CharityProject if isinstance(obj_in, Donation) else Donation
    )
    not_invested_objects = await get_not_invested_objects(
        invested_model, session
    )

    if not_invested_objects:
        available_amount = obj_in.full_amount
        for obj in not_invested_objects:
            need_amount = obj.full_amount - obj.invested_amount
            investment = (
                need_amount
                if need_amount < available_amount
                else available_amount
            )
            available_amount -= investment
            obj.invested_amount += investment
            obj_in.invested_amount += investment

            if obj.full_amount == obj.invested_amount:
                await close_invested_object(obj)

            if not available_amount:
                await close_invested_object(obj_in)
                break
        await session.commit()
    return obj_in


async def get_not_invested_objects(
    model_in: Union[CharityProject, Donation], session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(model_in)
        .where(model_in.fully_invested == False) # noqa
        .order_by(model_in.create_date)
    )
    return objects.scalars().all()


async def close_invested_object(
        obj: Union[CharityProject, Donation],
) -> None:
    obj.fully_invested = True
    obj.close_date = datetime.now()
