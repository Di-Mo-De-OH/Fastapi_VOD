from __future__ import annotations

import dataclasses
import uuid
from datetime import date
from typing import TYPE_CHECKING, Iterable

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG
from app.tortoise_models.participant_date import ParticipantDateModel


@dataclasses.dataclass
class BestDate:
    date: date
    enable_count: int
    star_count: int


if TYPE_CHECKING:
    from app.tortoise_models.meeting import MeetingModel


class ParticipantDateResponse(BaseModel):
    model_config = FROZEN_CONFIG
    date: date
    id: uuid.UUID | int
    enabled: bool
    started: bool


class ParticipantResponse(BaseModel):
    model_config = FROZEN_CONFIG
    id: uuid.UUID | int
    name: str
    dates: list[ParticipantDateResponse]


class GetMeetingResponse(BaseModel):
    model_config = FROZEN_CONFIG

    url_code: str
    title: str
    location: str
    start_date: date | None = None
    end_date: date | None = None
    participants: list[ParticipantResponse]
    best_dates: list[date]

    @classmethod
    def from_mysql(cls, meeting: MeetingModel) -> GetMeetingResponse:
        return GetMeetingResponse(
            url_code=meeting.url_code,
            end_date=meeting.end_date,
            start_date=meeting.start_date,
            title=meeting.title,
            location=meeting.location,
            participants=[
                ParticipantResponse(
                    id=p.id,
                    name=p.name,
                    dates=[
                        ParticipantDateResponse(date=pd.date, id=pd.id, enabled=pd.enabled, started=pd.started)
                        for pd in p.participant_dates
                    ],
                )
                for p in meeting.participants
            ],
            best_dates=cls._get_best_dates(
                (
                    participant_date
                    for participant in meeting.participants
                    for participant_date in participant.participant_dates
                )
            ),
        )

    @classmethod
    def _get_best_dates(cls, participant_dates: Iterable[ParticipantDateModel]) -> list[date]:
        result_dict: dict[date, BestDate] = {}

        for participant_date in participant_dates:
            if participant_date.date not in result_dict:
                result_dict[participant_date.date] = BestDate(date=participant_date.date, enable_count=0, star_count=0)
            if participant_date.enabled:
                result_dict[participant_date.date].enable_count += 1
                if participant_date.started:
                    result_dict[participant_date.date].star_count += 1
        result_list = list(result_dict.values())
        result_list.sort(
            key=lambda best_date: (-best_date.enable_count, -best_date.star_count, best_date.date),
        )
        return [best_date.date for best_date in result_list[:3]]
