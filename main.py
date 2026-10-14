
import json
import logging
from pathlib import Path

from config import load_config
from wolfram_api import send_query
from parser import parse_response


BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / "results"
LOGS_DIR = BASE_DIR / "logs"

RAW_FILE = RESULTS_DIR / "raw.json"
PARSED_FILE = RESULTS_DIR / "parsed.json"
LOG_FILE = LOGS_DIR / "app.log"


QUERIES = [
    "integrate x^2 sin^3 x dx",
    "population of Russia 2024",
    "molar mass of H2SO4",
    "kinetic energy of 5kg object at 10m/s",
    "distance between Moscow and Saint Petersburg",
    "100 USD to RUB",
    "current time in Kazan",
    "distance to Mars",
    "body mass index 180cm 75kg",
    "translate hello to Russian",
    "capital of France",
    "square root of 144",
    "boiling point of water",
    "chemical formula of table salt",
    "speed of light"
]


def setup_logging():
    LOGS_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    setup_logging()

    try:
        config = load_config()
        app_id = config["app_id"]
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        logging.error("Ошибка конфигурации: %s", error)
        print(f"Ошибка конфигурации: {error}")
        return

    raw_results = []
    parsed_results = []

    for number, query in enumerate(QUERIES, start=1):
        print(f"\n[{number}/{len(QUERIES)}] Запрос: {query}")
        logging.info("Выполняется запрос: %s", query)

        response = send_query(app_id, query)

        raw_item = {
            "query": query,
            **response
        }
        raw_results.append(raw_item)

        if response["success"]:
            parsed = parse_response(response["data"])

            parsed_item = {
                "query": query,
                **parsed
            }

            print("Запрос выполнен успешно.")

            for result in parsed["results"]:
                if result["text"]:
                    print(f"{result['title']}:")
                    for text in result["text"]:
                        print(f"  {text}")

            logging.info("Запрос выполнен успешно: %s", query)
        else:
            parsed_item = {
                "query": query,
                "success": False,
                "error": response["error"],
                "results": []
            }

            print(f"Ошибка: {response['error']}")
            logging.error(
                "Ошибка запроса '%s': %s",
                query,
                response["error"]
            )

        parsed_results.append(parsed_item)

        save_json(RAW_FILE, raw_results)
        save_json(PARSED_FILE, parsed_results)

    print("\nОбработка всех запросов завершена.")
    print(f"Полные ответы: {RAW_FILE}")
    print(f"Извлечённые результаты: {PARSED_FILE}")
    print(f"Лог работы: {LOG_FILE}")


if __name__ == "__main__":
    main()
