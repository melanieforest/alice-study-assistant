import requests

def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        data = response.json()[0]

        return {
            "text": data["q"],
            "author": data["a"]
        }

    except Exception:
        return {
            "text": "Каждый день — шанс стать лучше.",
            "author": "System"
        }