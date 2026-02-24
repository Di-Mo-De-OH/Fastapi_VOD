from datetime import datetime

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.dtos.create_meeting_response import CreateMeetingResponse
from app.dtos.get_meeting_response import GetMeetingResponse
from app.dtos.update_meeting_request import UpdateMeetingDateRangeRequest
from app.service.meeting_service_mysql import (
    service_create_meeting_mysql,
    service_get_meeting_mysql,
)

mysql_router = APIRouter(prefix="/v1/mysql/meetings", tags=["mysql"])
# 실전에서는 절대 db이름을 url에 넣지 말자!


@mysql_router.post("", description="meeting 을 생성합니다.")
async def api_create_meeting_mysql() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code=(await service_create_meeting_mysql()).url_code)


@mysql_router.get(
    "/{meeting_url_code}",  # path variable
    description="meeting 을 조회합니다.",
)
async def api_get_meeting_mysql(meeting_url_code: str) -> GetMeetingResponse:
    meeting = await service_get_meeting_mysql(meeting_url_code)
    if meeting is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"meeting with url_code: {meeting_url_code} not found"
        )
    return GetMeetingResponse(
        url_code=meeting.url_code,
        end_date=datetime.now().date(),
        start_date=datetime.now().date(),
        title="test",
        location="test",
    )


@mysql_router.patch(
    "/{meeting_url_code}/date_range",
    description="meeting의 날짜  range를 설정합니다.",
)
async def api_update_meeting_mysql(
    meeting_url_code: str, update_meeting_date_range_request: UpdateMeetingDateRangeRequest
) -> GetMeetingResponse:
    return GetMeetingResponse(
        url_code="abc", start_date=datetime.now().date(), end_date=datetime.now().date(), title="test", location="test"
    )
