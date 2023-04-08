from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationFullDB
from app.services.investition import investing


router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationFullDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Available only for superuser."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationDB],
    dependencies=[Depends(current_user)],
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Available only for registred user."""
    donations = await donation_crud.get_donations_by_user(
        user=user, session=session
    )
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Available only for registred user."""
    new_donation = await donation_crud.create(donation, session, user)
    await investing(new_donation, session)
    await session.refresh(new_donation)
    return new_donation
