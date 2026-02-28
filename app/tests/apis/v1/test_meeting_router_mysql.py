from datetime import date

import httpx
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_CONTENT,
)
from tortoise.contrib.test import TestCase

from app import app
from app.dtos.update_meeting_request import MEETING_DATE_MAX_RANGE
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
        self.assertIsNone(response_body["start_date"])
        self.assertIsNone(response_body["end_date"])
        self.assertEqual(response_body["title"], "")
        self.assertEqual(response_body["location"], "")

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

    async def test_api_update_meeting_date_range_mysql(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            meeting_create_response = await client.post("/v1/mysql/meetings")
            url_code = meeting_create_response.json()["url_code"]

            response = await client.patch(
                f"/v1/mysql/meetings/{url_code}/date_range",
                json={"start_date": "2026-03-10", "end_date": "2026-03-22"},
            )
        self.assertEqual(response.status_code, HTTP_200_OK, response.text)
        response_body = response.json()
        self.assertEqual(response_body["url_code"], url_code)
        self.assertEqual(response_body["start_date"], "2026-03-10")
        self.assertEqual(response_body["end_date"], "2026-03-22")
        meeting = await MeetingModel.filter(url_code=url_code).get()
        self.assertEqual(meeting.start_date.date(), date(2026, 3, 10))
        self.assertEqual(meeting.end_date.date(), date(2026, 3, 22))

    async def test_can_not_update_meeting_date_range_when_range_is_too_long(self) -> None:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            # Given
            create_meeting_response = await client.post(url="/v1/mysql/meetings")
            url_code = create_meeting_response.json()["url_code"]

            # When
            response = await client.patch(
                url=f"/v1/mysql/meetings/{url_code}/date_range",
                json={"start_date": (start := "2026-03-10"), "end_date": (end := "2030-10-20")},
            )

        # Then
        assert response.status_code == HTTP_422_UNPROCESSABLE_CONTENT
        response_body = response.json()
        assert response_body["detail"] == (f"start {start} and end {end} should be within {MEETING_DATE_MAX_RANGE}")

    async def test_can_not_update_meeting_date_range_when_it_is_already_set(self) -> None:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            # Given
            create_meeting_response = await client.post(url="/v1/mysql/meetings")
            url_code = create_meeting_response.json()["url_code"]
            await client.patch(
                url=f"/v1/mysql/meetings/{url_code}/date_range",
                json={"start_date": "2026-03-10", "end_date": "2026-03-20"},
            )

            # When
            response = await client.patch(
                url=f"/v1/mysql/meetings/{url_code}/date_range",
                json={"start_date": "2026-03-12", "end_date": "2026-03-22"},
            )

        # Then
        # Then
        assert response.status_code == HTTP_422_UNPROCESSABLE_CONTENT
        response_body = response.json()

        detail = response_body["detail"]

        # 1) 기본 포맷 체크 (url_code 포함)
        assert detail.startswith(f"meeting: {url_code} start:")

        # 2) 날짜가 들어있는지만 체크 (뒤에 00:00:00+09:00 붙어도 통과)
        assert "2026-03-10" in detail
        assert "end:" in detail
        assert "2026-03-20" in detail

    async def test_can_not_update_meeting_does_not_exists(self) -> None:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            # Given
            url_code = "invalid_url"

            # When
            response = await client.patch(
                url=f"/v1/mysql/meetings/{url_code}/date_range",
                json={"start_date": "2026-03-12", "end_date": "2026-03-22"},
            )

        # Then
        assert response.status_code == HTTP_404_NOT_FOUND
        response_body = response.json()
        assert response_body["detail"] == "meeting with url_code: invalid_url not found"
