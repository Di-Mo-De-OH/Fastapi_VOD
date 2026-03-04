from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from app.dtos.create_participant_request import CreateParticipantRequestModel
from app.dtos.create_participant_response import (
    CreateParticipantMysqlResponse,
    ParticipantDateMysql,
)
from app.service.meeting_service_mysql import service_get_meeting_mysql
from app.service.participant_service_mysql import service_create_participant

mysql_router = APIRouter(prefix="/v1/mysql/participants", tags=["participants"])
# 실전에서는 절대 db이름을 url에 넣지 말자!


@mysql_router.post("", description="participant 를 생성합니다")
async def api_create_participant_mysql(
    create_participant_request: CreateParticipantRequestModel,
) -> CreateParticipantMysqlResponse:
    meeting = await service_get_meeting_mysql(create_participant_request.meeting_url_code)

    if not meeting:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {create_participant_request.meeting_url_code} not found",
        )
    if not (meeting.start_date and meeting.end_date):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="start and end should be set.",
        )

    participant, participant_dates = await service_create_participant(
        create_participant_request,
        meeting.start_date,
        meeting.end_date,
    )

    return CreateParticipantMysqlResponse(
        participant_id=participant.id,
        participant_dates=[ParticipantDateMysql(id=pd.id, date=pd.date) for pd in participant_dates],
    )
