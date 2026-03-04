import asyncio

import httpx
from starlette.status import HTTP_200_OK
from tortoise.contrib.test import TestCase

from app import app
from app.tortoise_models.participant_date import ParticipantDateModel


class TestBestDatesMysql(TestCase):
    async def test_best_dates(self) -> None:
        """
        미팅 생성 -> 날짜 지정 -> 참가자 둘 생성

        2025-12-03 을 2명이 전부 켠다.
        2025-12-10 을 2명이 전부 켜고 1명이 스타 준다.
        2025-12-11 을 1명만 켠다.

        2명 모두 다 되고, 스타도 있는 12-10 이 1등,
        그 다음 12-03, 그 다음 12-11 순이다.
        """

        # Given
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            create_meeting_response = await client.post(
                url="/v1/mysql/meetings",
            )
            url_code = create_meeting_response.json()["url_code"]

            await client.patch(
                url=f"/v1/mysql/meetings/{url_code}/date_range",
                json={
                    "start_date": "2026-04-01",
                    "end_date": "2026-04-30",
                },
            )
            participant_response1 = await client.post(
                url="/v1/mysql/participants",
                json={
                    "name": "test_name1",
                    "meeting_url_code": url_code,
                },
            )
            participant_response2 = await client.post(
                url="/v1/mysql/participants",
                json={
                    "name": "test_name2",
                    "meeting_url_code": url_code,
                },
            )

            participant_response1_body = participant_response1.json()
            participant_response2_body = participant_response2.json()
            participant1_id = participant_response1_body["participant_id"]
            participant2_id = participant_response2_body["participant_id"]

            # participant1 과 2의 모든 date 를 off
            await ParticipantDateModel.filter(participant_id=participant1_id).update(enabled=False)
            await ParticipantDateModel.filter(participant_id=participant2_id).update(enabled=False)

            # 켜는 작업 전부 수행
            await asyncio.gather(
                client.patch(
                    url="/v1/mysql/participant_dates/on",
                    json={
                        "participant_date_id": participant_response1_body["participant_dates"][2]["id"],
                        "meeting_url_code": url_code,
                    },
                ),
                client.patch(
                    url="/v1/mysql/participant_dates/on",
                    json={
                        "participant_date_id": participant_response2_body["participant_dates"][2]["id"],
                        "meeting_url_code": url_code,
                    },
                ),
                client.patch(
                    url="/v1/mysql/participant_dates/on",
                    json={
                        "participant_date_id": participant_response1_body["participant_dates"][10]["id"],
                        "meeting_url_code": url_code,
                    },
                ),
                client.patch(
                    url="/v1/mysql/participant_dates/on",
                    json={
                        "participant_date_id": participant_response2_body["participant_dates"][9]["id"],
                        "meeting_url_code": url_code,
                    },
                ),
                client.patch(
                    url="/v1/mysql/participant_dates/on",
                    json={
                        "participant_date_id": participant_response1_body["participant_dates"][9]["id"],
                        "meeting_url_code": url_code,
                    },
                ),
            )
            await client.patch(
                url="/v1/mysql/participant_dates/star",
                json={
                    "participant_date_id": participant_response1_body["participant_dates"][9]["id"],
                    "meeting_url_code": url_code,
                },
            )

            # When
            meeting_response = await client.get(
                url=f"/v1/mysql/meetings/{url_code}",
            )

        # Then
        self.assertEqual(meeting_response.status_code, HTTP_200_OK)
        meeting_response_body = meeting_response.json()
        self.assertEqual(meeting_response_body["best_dates"], ["2026-04-10", "2026-04-03", "2026-04-11"])
