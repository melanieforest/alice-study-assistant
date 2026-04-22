from flask import Blueprint, jsonify, request
from services.intent_service import detect_intent
from services.dialog_service import get_or_create_session, reset_session, set_mode
from services.lesson_service import get_theory_response
from services.progress_service import get_progress_text
from services.quiz_service import start_quiz, process_answer

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    user_text = data.get("request", {}).get("original_utterance", "")
    version = data.get("version", "1.0")

    alice_user_id = (
        data.get("session", {}).get("user_id")
        or data.get("session", {}).get("application", {}).get("application_id")
        or "test_user"
    )

    session = get_or_create_session(alice_user_id)

    if session.waiting_for_answer and session.mode == "quiz":
        response_text = process_answer(session, alice_user_id, user_text)
    else:
        intent = detect_intent(user_text)

        if intent == "greeting":
            response_text = (
                "Привет! Я учебный помощник по Python. "
                "Могу запустить тест, объяснить тему или показать прогресс."
            )

        elif intent == "help":
            response_text = (
                "Скажите: хочу тест, обучение, объясни переменную, "
                "объясни цикл for, объясни функцию, объясни список, объясни if или покажи прогресс."
            )

        elif intent == "start_test":
            response_text = start_quiz(session, alice_user_id)

        elif intent == "start_learning":
            set_mode(session, "learning")

            theory_response = get_theory_response(user_text)

            default_learning_text = (
                "Я могу объяснить темы по Python.\n"
                "Например: объясни переменную, объясни цикл for, "
                "объясни функцию, объясни список, объясни if или объясни словарь."
            )

            if theory_response != default_learning_text:
                response_text = theory_response
            else:
                response_text = (
                    "Хорошо, начинаем обучение.\n"
                    "Скажите, какую тему объяснить: переменная, цикл for, функция, список, if или словарь."
                )

        elif intent == "show_progress":
            response_text = get_progress_text(alice_user_id)

        elif intent == "exit":
            reset_session(session)
            response_text = "Хорошо, текущий режим сброшен. Если захотите продолжить, скажите: привет."

        else:
            if session.mode == "learning":
                response_text = get_theory_response(user_text)
            else:
                response_text = (
                    "Я не совсем понял запрос. "
                    "Скажите: хочу тест, обучение, помощь или прогресс."
                )

    return jsonify({"response": {
            "text": response_text,
            "end_session": False
        },
        "version": version
    })