import datetime

import httpx
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from tortoise.contrib.test import TestCase

from app import app
from app.tortoise_models.participant import ParticipantModel
from app.tortoise_models.participant_date import ParticipantDateModel


class TestParticipantRouter(TestCase):
    async def test_api_create_participant_mysql(self) -> None:
        # When
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            meeting_create_response = await client.post("v1/mysql/meetings")
            url_code = meeting_create_response.json()["url_code"]

            await client.patch(
                f"/v1/mysql/meetings/{url_code}/date_range", json={"start_date": "2026-03-10", "end_date": "2026-03-12"}
            )

            response = await client.post(
                "/v1/mysql/participants", json={"meeting_url_code": url_code, "name": (participant_name := "test")}
            )
        # Then
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_body = response.json()
        participant = await ParticipantModel.filter(id=response_body["participant_id"]).get()
        self.assertEqual(participant_name, participant.name)
        self.assertEqual(url_code, participant.meeting_id)
        participant_dates = await ParticipantDateModel.get_all_by_participant_id(participant.id)
        self.assertEqual(len(participant_dates), 3)
        self.assertEqual(
            [date.date for date in participant_dates],
            [datetime.date(2026, 3, 10), datetime.date(2026, 3, 11), datetime.date(2026, 3, 12)],
        )

    async def test_can_not_create_participant_when_meeting_does_not_exist(self) -> None:
        # When
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # When
            response = await client.post(
                "/v1/mysql/participants",
                json={"meeting_url_code": "not_exist", "name": "test"},
            )

        # Then
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        response_body = response.json()
        self.assertEqual(response_body["detail"], "meeting with url_code: not_exist not found")

    async def test_can_not_create_participant_when_meeting_date_range_does_not_exist(self) -> None:
        # When
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # Given
            meeting_create_response = await client.post("/v1/mysql/meetings")
            url_code = meeting_create_response.json()["url_code"]

            # When
            response = await client.post(
                "/v1/mysql/participants",
                json={"meeting_url_code": url_code, "name": "test"},
            )

        # Then
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        response_body = response.json()
        self.assertEqual(response_body["detail"], "start and end should be set.")
