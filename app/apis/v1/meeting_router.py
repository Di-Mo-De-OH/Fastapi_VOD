from fastapi import APIRouter

from app.dtos.create_meeting_response import CreateMeetingResponse
from app.dtos.get_meeting_response import GetMeetingResponse
from app.service.meeting_service_mysql import service_create_meeting_mysql

mysql_router = APIRouter(prefix="/v1/mysql/meetings", tags=["mysql"])
# 실전에서는 절대 db이름을 url에 넣지 말자!


@mysql_router.post("", description="meeting 을 생성합니다.")
async def api_create_meeting_mysql() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code=(await service_create_meeting_mysql()).url_code)


@mysql_router.get("/{meeting_url_code}", description="meeting을 조회합니다")
async def api_get_meeting_mysql(meeting_url_code: str) -> GetMeetingResponse:
    return GetMeetingResponse(url_code="abc")
