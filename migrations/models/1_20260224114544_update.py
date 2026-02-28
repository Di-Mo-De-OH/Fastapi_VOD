from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `meeting` ADD `location` VARCHAR(255) NOT NULL  DEFAULT '';
        ALTER TABLE `meeting` ADD `title` VARCHAR(255) NOT NULL  DEFAULT '';
        ALTER TABLE `meeting` ADD `end_date` DATETIME(6);
        ALTER TABLE `meeting` ADD `start_date` DATETIME(6);
        ALTER TABLE `meeting` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `meeting` DROP COLUMN `location`;
        ALTER TABLE `meeting` DROP COLUMN `title`;
        ALTER TABLE `meeting` DROP COLUMN `end_date`;
        ALTER TABLE `meeting` DROP COLUMN `start_date`;
        ALTER TABLE `meeting` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL;"""
