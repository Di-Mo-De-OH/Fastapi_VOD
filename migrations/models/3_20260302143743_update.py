from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `participants` ADD INDEX `idx_participant_meeting_1de158` (`meeting_id`);
        ALTER TABLE `participant_dates` ADD INDEX `idx_participant_partici_ebb73d` (`participant_id`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `participant_dates` DROP INDEX `idx_participant_partici_ebb73d`;
        ALTER TABLE `participants` DROP INDEX `idx_participant_meeting_1de158`;"""
