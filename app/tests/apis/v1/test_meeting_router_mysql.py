import httpx
from starlette.status import HTTP_200_OK
from tortoise.contrib.test import TestCase

from app import app
from app.tortoise_models.meeting import MeetingModel


class TestMeetingRouter(TestCase):
    async def test_api_create_meeting_mysql(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.post(url="/v1/mysql/meetings")

        assert response.status_code == HTTP_200_OK
        url_code = response.json()["url_code"]
        assert await MeetingModel.filter(url_code=url_code).exists() is True
