from pydantic import BaseModel


class TurnOnOffStarParticipantDateRequestMysql(BaseModel):
    participant_date_id: int
    meeting_url_code: str
