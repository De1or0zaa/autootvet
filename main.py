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
    
    config_env = os.getenv('CONFIG_JSON')
    if config_env:
        config = json.loads(config_env)
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
