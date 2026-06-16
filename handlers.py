import random


def setup_handlers(client, config, logger):
    @client.event
    async def on_message(message):
        try:
            if client.user is None:
                return
            if message.author == client.user:
                return
            if message.author.bot:
                return

            for rule in config["rules"]:
                if message.guild is None or message.guild.id != rule["guild_id"]:
                    continue
                if message.channel.id != rule["channel_id"]:
                    continue
                if message.author.id not in rule["user_ids"]:
                    continue

                mention = client.user.mentioned_in(message) and rule.get("trigger_on_mention", False)

                reply = False
                if (
                    message.reference is not None
                    and message.reference.resolved is not None
                    and isinstance(message.reference.resolved, discord.Message)
                    and rule.get("trigger_on_reply", False)
                ):
                    reply = message.reference.resolved.author == client.user

                if not mention and not reply:
                    continue

                response = random.choice(rule["responses"])
                await message.channel.send(response)

                logger.info(f"Ответ отправлен | Сервер: {message.guild.name} | Канал: {message.channel.name} | От: {message.author} | Ответ: {response}")
                break
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения: {e}", exc_info=True)