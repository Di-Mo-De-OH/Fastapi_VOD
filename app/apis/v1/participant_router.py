from fastapi import APIRouter

from app.dtos.create_participant_request import CreateParticipantRequestModel
from app.dtos.create_participant_response import CreateParticipantMysqlResponse

mysql_router = APIRouter(prefix="/v1/mysql/participants", tags=["participants"])
# 실전에서는 절대 db이름을 url에 넣지 말자!


@mysql_router.post("", description="participant 를 생성합니다")
async def api_create_participant_mysql(
    create_participant_request: CreateParticipantRequestModel,
) -> CreateParticipantMysqlResponse:
    return CreateParticipantMysqlResponse(participant_id=123, participant_dates=[])
