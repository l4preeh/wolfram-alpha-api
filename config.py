
import json
from pathlib import Path


CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8-sig") as file:
        config = json.load(file)

    if "app_id" not in config:
        raise ValueError(
            f"В {CONFIG_PATH} отсутствует поле app_id"
        )

    app_id = str(config["app_id"]).strip()

    if not app_id:
        raise ValueError(
            f"Поле app_id пустое в файле {CONFIG_PATH}"
        )

    return {"app_id": app_id}
