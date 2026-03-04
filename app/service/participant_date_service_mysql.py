from app.tortoise_models.participant_date import ParticipantDateModel


async def service_turn_on_participant_date_mysql(participant_date_id: int) -> None:
    await ParticipantDateModel.on(participant_date_id)


async def service_turn_off_participant_date_mysql(participant_date_id: int) -> None:
    await ParticipantDateModel.off(participant_date_id)


async def service_star_participant_date_mysql(participant_date_id: int) -> None:
    await ParticipantDateModel.star(participant_date_id)


async def service_unstar_participant_date_mysql(participant_date_id: int) -> None:
    await ParticipantDateModel.unstar(participant_date_id)
