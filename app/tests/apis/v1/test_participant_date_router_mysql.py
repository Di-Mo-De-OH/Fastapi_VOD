import httpx
from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)
from tortoise.contrib.test import TestCase

from app import app
from app.tortoise_models.participant_date import ParticipantDateModel


class TestParticipantRouter(TestCase):

    async def test_turn_on_participant_date(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # Given
            meeting_create_response = await client.post("/v1/mysql/meetings")
            url_code = meeting_create_response.json()["url_code"]

            await client.patch(
                f"v1/mysql/meetings/{url_code}/date_range",
                json={"start_date": "2025-10-10", "end_date": "2025-10-12"},
            )

            create_participant_response = await client.post(
                "/v1/mysql/participants",
                json={"meeting_url_code": url_code, "name": "test"},
            )
            dates = create_participant_response.json()["participant_dates"]

            await client.patch(
                "/v1/mysql/participant_dates/off",
                json={"participant_date_id": dates[0]["id"], "meeting_url_code": url_code},
            )

            # When
            response = await client.patch(
                "/v1/mysql/participant_dates/on",
                json={"participant_date_id": dates[0]["id"], "meeting_url_code": url_code},
            )

        # Then
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_body = response.json()
        assert response_body["participants"][0]["dates"][0]["enabled"] is True
        participant_date = await ParticipantDateModel.filter(id=dates[0]["id"]).get()
        self.assertTrue(participant_date.enabled)

    async def test_turn_off_participant_date(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # Given
            meeting_create_response = await client.post("/v1/mysql/meetings")
            url_code = meeting_create_response.json()["url_code"]

            await client.patch(
                f"v1/mysql/meetings/{url_code}/date_range",
                json={"start_date": "2025-10-10", "end_date": "2025-10-12"},
            )

            create_participant_response = await client.post(
                "/v1/mysql/participants",
                json={"meeting_url_code": url_code, "name": "test"},
            )
            dates = create_participant_response.json()["participant_dates"]

            # When
            response = await client.patch(
                "/v1/mysql/participant_dates/off",
                json={"participant_date_id": dates[0]["id"], "meeting_url_code": url_code},
            )

        # Then
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_body = response.json()
        assert response_body["participants"][0]["dates"][0]["enabled"] is False
        participant_date = await ParticipantDateModel.filter(id=dates[0]["id"]).get()
        self.assertFalse(participant_date.enabled)

    async def test_turn_on_participant_date_when_meeting_does_not_exist(self) -> None:
        # When
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # When
            response = await client.patch(
                "/v1/mysql/participant_dates/on",
                json={"participant_date_id": 1, "meeting_url_code": "not_exist"},
            )

        # Then
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        response_body = response.json()
        self.assertEqual(response_body["detail"], "meeting with url_code: not_exist not found")

    async def test_turn_off_participant_date_when_meeting_does_not_exist(self) -> None:
        # When
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # When
            response = await client.patch(
                "/v1/mysql/participant_dates/off",
                json={"participant_date_id": 1, "meeting_url_code": "not_exist"},
            )

        # Then
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        response_body = response.json()
        self.assertEqual(response_body["detail"], "meeting with url_code: not_exist not found")

    async def test_star_participant_date(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # Given
            meeting_create_response = await client.post("/v1/mysql/meetings")
            url_code = meeting_create_response.json()["url_code"]

            await client.patch(
                f"v1/mysql/meetings/{url_code}/date_range",
                json={"start_date": "2026-03-10", "end_date": "2026-03-12"},
            )

            create_participant_response = await client.post(
                "/v1/mysql/participants",
                json={"meeting_url_code": url_code, "name": "test"},
            )
            dates = create_participant_response.json()["participant_dates"]

            await client.patch(
                "/v1/mysql/participant_dates/off",
                json={"participant_date_id": dates[0]["id"], "meeting_url_code": url_code},
            )

            # When
            response = await client.patch(
                "/v1/mysql/participant_dates/star",
                json={"participant_date_id": dates[0]["id"], "meeting_url_code": url_code},
            )

        # Then
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_body = response.json()
        assert response_body["participants"][0]["dates"][0]["started"] is True
        assert response_body["participants"][0]["dates"][0]["enabled"] is True
        participant_date = await ParticipantDateModel.filter(id=dates[0]["id"]).get()
        self.assertTrue(participant_date.started)
        self.assertTrue(participant_date.enabled)

    async def test_start_participant_date_when_meeting_does_not_exist(self) -> None:
        # When
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # When
            response = await client.patch(
                "/v1/mysql/participant_dates/star",
                json={"participant_date_id": 1, "meeting_url_code": "not_exist"},
            )

        # Then
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        response_body = response.json()
        self.assertEqual(response_body["detail"], "meeting with url_code: not_exist not found")

    async def test_unstar_participant_date(self) -> None:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # Given
            meeting_create_response = await client.post("/v1/mysql/meetings")
            url_code = meeting_create_response.json()["url_code"]

            await client.patch(
                f"v1/mysql/meetings/{url_code}/date_range",
                json={"start_date": "2026-03-10", "end_date": "2026-03-12"},
            )

            create_participant_response = await client.post(
                "/v1/mysql/participants",
                json={"meeting_url_code": url_code, "name": "test"},
            )
            dates = create_participant_response.json()["participant_dates"]

            await client.patch(
                "/v1/mysql/participant_dates/star",
                json={"participant_date_id": dates[0]["id"], "meeting_url_code": url_code},
            )

            # When
            response = await client.patch(
                "/v1/mysql/participant_dates/unstar",
                json={"participant_date_id": dates[0]["id"], "meeting_url_code": url_code},
            )

        # Then
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_body = response.json()
        assert response_body["participants"][0]["dates"][0]["started"] is False
        assert response_body["participants"][0]["dates"][0]["enabled"] is True
        participant_date = await ParticipantDateModel.filter(id=dates[0]["id"]).get()
        self.assertFalse(participant_date.started)
        self.assertTrue(participant_date.enabled)

    async def test_unstar_participant_date_when_meeting_does_not_exist(self) -> None:
        # When
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            # When
            response = await client.patch(
                "/v1/mysql/participant_dates/unstar",
                json={"participant_date_id": 1, "meeting_url_code": "not_exist"},
            )

        # Then
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        response_body = response.json()
        self.assertEqual(response_body["detail"], "meeting with url_code: not_exist not found")
