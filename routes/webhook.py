from flask import Blueprint, jsonify, request

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    user_text = data.get("request", {}).get("original_utterance", "").lower()

    if "привет" in user_text:
        response_text = "Привет! Я учебный помощник по Python. Могу объяснить тему или провести тест."
    elif "тест" in user_text:
        response_text = "Хорошо. Начинаем тест по Python. Первый вопрос скоро будет добавлен."
    elif "обучение" in user_text or "объясни" in user_text:
        response_text = "Хорошо. Назови тему по Python, которую хочешь изучить."
    else:
        response_text = "Я учебный помощник. Скажи: обучение, тест или привет."

    return jsonify({
        "response": {
            "text": response_text,
            "end_session": False
        },
        "version": data.get("version", "1.0")
    })