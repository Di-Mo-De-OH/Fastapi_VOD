from datetime import date

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class GetMeetingResponse(BaseModel):
    model_config = FROZEN_CONFIG

    url_code: str
    title: str
    location: str
    start_date: date | None = None
    end_date: date | None = None
