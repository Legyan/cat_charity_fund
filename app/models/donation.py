from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import PreBaseCharityDonation


class Donation(PreBaseCharityDonation):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
