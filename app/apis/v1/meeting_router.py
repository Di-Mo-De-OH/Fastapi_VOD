from fastapi import APIRouter

from app.service.meeting_service_mysql import service_create_meeting_mysql
from dtos.create_meeting_response import CreateMeetingResponse

mysql_router = APIRouter(prefix="/v1/mysql/meetings", tags=["mysql"])
# 실전에서는 절대 db이름을 url에 넣지 말자!


@mysql_router.post("", description="meeting 을 생성합니다.")
async def api_create_meeting_mysql() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code=(await service_create_meeting_mysql()).url_code)
