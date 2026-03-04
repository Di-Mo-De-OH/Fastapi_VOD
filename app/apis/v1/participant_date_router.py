from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.dtos.get_meeting_response import (
    GetMeetingResponse,
)
from app.dtos.turn_on_off_star_participant_date_request import (
    TurnOnOffStarParticipantDateRequestMysql,
)
from app.service.meeting_service_mysql import service_get_meeting_mysql
from app.service.participant_date_service_mysql import (
    service_star_participant_date_mysql,
    service_turn_off_participant_date_mysql,
    service_turn_on_participant_date_mysql,
    service_unstar_participant_date_mysql,
)

mysql_router = APIRouter(prefix="/v1/mysql/participant_dates", tags=["ParticipantDate"])


@mysql_router.patch(
    "/on",
    description="특정 참가자의 특정 날짜를 켭니다.",
)
async def api_turn_on_date_mysql(
    turn_on_participant_day_request: TurnOnOffStarParticipantDateRequestMysql,
) -> GetMeetingResponse:
    await service_turn_on_participant_date_mysql(turn_on_participant_day_request.participant_date_id)
    meeting = await service_get_meeting_mysql(turn_on_participant_day_request.meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {turn_on_participant_day_request.meeting_url_code} not found",
        )
    return GetMeetingResponse.from_mysql(meeting)


@mysql_router.patch(
    "/off",
    description="특정 참가자의 특정 날짜를 끕니다.",
)
async def api_turn_off_date_mysql(
    turn_off_participant_day_request: TurnOnOffStarParticipantDateRequestMysql,
) -> GetMeetingResponse:
    await service_turn_off_participant_date_mysql(turn_off_participant_day_request.participant_date_id)
    meeting = await service_get_meeting_mysql(turn_off_participant_day_request.meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {turn_off_participant_day_request.meeting_url_code} not found",
        )
    return GetMeetingResponse.from_mysql(meeting)


@mysql_router.patch(
    "/star",
    description="특정 참가자의 특정 날짜를 별표로 표시합니다.",
)
async def api_star_date_mysql(
    star_participant_day_request: TurnOnOffStarParticipantDateRequestMysql,
) -> GetMeetingResponse:
    await service_star_participant_date_mysql(star_participant_day_request.participant_date_id)
    meeting = await service_get_meeting_mysql(star_participant_day_request.meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {star_participant_day_request.meeting_url_code} not found",
        )
    return GetMeetingResponse.from_mysql(meeting)


@mysql_router.patch(
    "/unstar",
    description="특정 참가자의 특정 날짜의 별을 제거합니다.",
)
async def api_unstar_date_mysql(
    unstar_participant_day_request: TurnOnOffStarParticipantDateRequestMysql,
) -> GetMeetingResponse:
    await service_unstar_participant_date_mysql(unstar_participant_day_request.participant_date_id)
    meeting = await service_get_meeting_mysql(unstar_participant_day_request.meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"meeting with url_code: {unstar_participant_day_request.meeting_url_code} not found",
        )
    return GetMeetingResponse.from_mysql(meeting)
