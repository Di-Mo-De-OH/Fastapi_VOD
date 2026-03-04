from datetime import date, timedelta

from tortoise.transactions import in_transaction

from app.dtos.create_participant_request import CreateParticipantRequestModel
from app.tortoise_models.participant import ParticipantModel
from app.tortoise_models.participant_date import ParticipantDateModel


async def service_create_participant(
    create_participant_request: CreateParticipantRequestModel, meeting_start_date: date, meeting_end_date: date
) -> tuple[ParticipantModel, list[ParticipantDateModel]]:
    dates = [meeting_start_date + timedelta(days=i) for i in range((meeting_end_date - meeting_start_date).days + 1)]
    async with in_transaction():
        participant = await ParticipantModel.create_participant(
            name=create_participant_request.name,
            meeting_url_code=create_participant_request.meeting_url_code,
        )
        await ParticipantDateModel.bulk_create_participant_dates(
            participant_id=participant.id,
            dates=dates,
        )
        participant_dates = await ParticipantDateModel.get_all_by_participant_id(participant.id)
        return participant, participant_dates
