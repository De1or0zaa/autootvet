import discord
import sys
import asyncio
import os
import json
from logger_setup import setup_logger
from config_loader import load_config
from handlers import setup_handlers


async def main():
    logger = setup_logger()
    
    token = os.getenv('TOKEN')
    if token:
        logger.info(f"Token loaded: {token[:10]}...")
        config = {
            "token": token,
            "rules": [
                {
                    "guild_id": int(os.getenv('GUILD_ID', '0')),
                    "channel_id": int(os.getenv('CHANNEL_ID', '0')),
                    "user_ids": json.loads(os.getenv('USER_IDS', '[]')),
                    "trigger_on_mention": os.getenv('TRIGGER_ON_MENTION', 'true').lower() == 'true',
                    "trigger_on_reply": os.getenv('TRIGGER_ON_REPLY', 'true').lower() == 'true',
                    "responses": json.loads(os.getenv('RESPONSES', '["Автоответ"]'))
                }
            ]
        }
    else:
        config = load_config()
    
    if config is None:
        logger.error("Failed to load config")
        sys.exit(1)
    
    client = discord.Client()
    setup_handlers(client, config, logger)
    logger.info("Bot starting...")
    await client.start(config["token"])


if __name__ == "__main__":
    asyncio.run(main())
