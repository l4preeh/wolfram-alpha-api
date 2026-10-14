
import requests


API_URL = "https://api.wolframalpha.com/v2/query"


def send_query(app_id, query):
    params = {
        "appid": app_id,
        "input": query,
        "output": "json"
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        query_result = data.get("queryresult", {})

        if query_result.get("error"):
            return {
                "success": False,
                "error": "Wolfram Alpha сообщил об ошибке"
            }

        if not query_result.get("success"):
            return {
                "success": False,
                "error": "Не удалось получить ответ на запрос"
            }

        return {
            "success": True,
            "data": data
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Превышено время ожидания ответа"
        }

    except requests.exceptions.RequestException as error:
        return {
            "success": False,
            "error": f"Ошибка сети или HTTP: {error}"
        }

    except ValueError:
        return {
            "success": False,
            "error": "Не удалось разобрать JSON-ответ"
        }
