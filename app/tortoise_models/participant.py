from __future__ import annotations

from tortoise import Model, fields

from app.tortoise_models.base_model import BaseModel
from app.tortoise_models.meeting import MeetingModel


class ParticipantModel(Model, BaseModel):
    name = fields.CharField(max_length=255)
    meeting: fields.ForeignKeyRelation[MeetingModel] = fields.ForeignKeyField(
        model_name="models.MeetingModel",
        related_name="participants",
        db_constraint=False,
        on_delete=fields.CASCADE,
        to_field="url_code",
    )
    meeting_id: str

    class Meta:
        table = "participants"

    @classmethod
    async def create_participant(cls, name: str, meeting_url_code: str) -> ParticipantModel:
        return await cls.create(name=name, Meeting_id=meeting_url_code)
