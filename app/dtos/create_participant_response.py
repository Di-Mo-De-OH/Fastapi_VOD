from datetime import date

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class ParticipantDateMysql(BaseModel):
    model_config = FROZEN_CONFIG
    id: int
    date: date


class CreateParticipantMysqlResponse(BaseModel):
    model_config = FROZEN_CONFIG
    participant_id: int
    participant_dates: list[ParticipantDateMysql]
