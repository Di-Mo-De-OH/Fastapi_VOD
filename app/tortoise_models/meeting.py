from __future__ import annotations

from datetime import date

from tortoise import Model, fields

from .base_model import BaseModel


class MeetingModel(BaseModel, Model):
    url_code = fields.CharField(max_length=255, unique=True)
    title = fields.CharField(max_length=255, default="")
    location = fields.CharField(max_length=255, default="")
    start_date = fields.DatetimeField(null=True)
    end_date = fields.DatetimeField(null=True)

    class Meta:
        table = "meeting"

    @classmethod
    async def create_meeting(cls, url_code: str) -> MeetingModel:
        return await cls.create(url_code=url_code)

    @classmethod
    async def get_by_url_code(cls, url_code: str) -> MeetingModel | None:
        return await cls.filter(url_code=url_code).get_or_none()

    @classmethod
    async def update_start_and_end(cls, url_code: str, start_date: date, end_date: date) -> None:
        await cls.filter(url_code=url_code).update(start_date=start_date, end_date=end_date)
