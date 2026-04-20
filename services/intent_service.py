def detect_intent(user_text: str) -> str:
    text = user_text.lower().strip()

    if any(word in text for word in ["привет", "здравствуй", "здравствуйте", "добрый день"]):
        return "greeting"

    if any(word in text for word in ["помощь", "что ты умеешь", "что умеешь", "help"]):
        return "help"

    if any(word in text for word in ["тест", "проверка", "опрос", "давай тест", "начать тест"]):
        return "start_test"

    if any(word in text for word in ["обучение", "изучение", "теория", "объясни", "объяснение", "урок"]):
        return "start_learning"

    if any(word in text for word in ["прогресс", "результат", "статистика"]):
        return "show_progress"

    if any(word in text for word in ["выход", "стоп", "хватит", "завершить"]):
        return "exit"

    return "unknown"