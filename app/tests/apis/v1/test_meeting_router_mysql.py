import httpx
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from tortoise.contrib.test import TestCase

from app import app
from app.tortoise_models.meeting import MeetingModel


class TestMeetingRouter(TestCase):
    async def test_api_create_meeting_mysql(self) -> None:
        # When
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.post("/v1/mysql/meetings")

        # Then
        self.assertEqual(response.status_code, HTTP_200_OK)
        url_code = response.json()["url_code"]
        self.assertTrue(await MeetingModel.filter(url_code=url_code).exists())

    async def test_api_get_meeting_mysql(self) -> None:

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # Given
            meeting_create_response = await client.post("/v1/mysql/meetings")
            url_code = meeting_create_response.json()["url_code"]

            # When
            response = await client.get(f"v1/mysql/meetings/{url_code}")

        # Then
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_body = response.json()
        self.assertEqual(response_body["url_code"], url_code)

    async def test_api_get_meeting_mysql_404(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            invalid_url_code = "invalid_url_code"

            response = await client.get(f"v1/mysql/meetings/{invalid_url_code}")

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        response_body = response.json()
        self.assertEqual(response_body["detail"], "meeting with url_code: invalid_url_code not found")
