import json
import logging
import os

logger = logging.getLogger("autoresponder")

DEFAULT_CONFIG = {
    "token": "YOUR_DISCORD_TOKEN_HERE",
    "rules": [
        {
            "guild_id": 123456789012345678,
            "channel_id": 123456789012345678,
            "user_ids": [123456789012345678],
            "trigger_on_mention": True,
            "trigger_on_reply": True,
            "responses": [
                "Меня сейчас нет, напишите позже.",
                "Я занят, отвечу позже!",
                "Автоответ: скоро буду."
            ]
        }
    ]
}

REQUIRED_FIELDS = {"token": str, "rules": list}

RULE_FIELDS = {
    "guild_id": int,
    "channel_id": int,
    "user_ids": list,
    "responses": list,
    "trigger_on_mention": bool,
    "trigger_on_reply": bool,
}


def _validate_rule(rule, index):
    for field, expected_type in RULE_FIELDS.items():
        if field not in rule:
            logger.error("Правило #%d: отсутствует поле '%s'", index, field)
            return False
        if not isinstance(rule[field], expected_type):
            logger.error("Правило #%d: поле '%s' должно быть типа %s", index, field, expected_type.__name__)
            return False

    if len(rule["responses"]) == 0:
        logger.error("Правило #%d: список 'responses' не должен быть пустым", index)
        return False

    return True


def load_config(path="config.json"):
    if not os.path.exists(path):
        logger.warning("Файл конфигурации не найден. Создаю шаблон: %s", path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        logger.error("Ошибка парсинга JSON: %s", e)
        return None

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in config:
            logger.error("Отсутствует обязательное поле: '%s'", field)
            return None
        if not isinstance(config[field], expected_type):
            logger.error("Поле '%s' должно быть типа %s", field, expected_type.__name__)
            return None

    for i, rule in enumerate(config["rules"]):
        if not _validate_rule(rule, i + 1):
            return None

    return config
