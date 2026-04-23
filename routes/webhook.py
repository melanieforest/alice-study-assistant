import random
from flask import Blueprint, jsonify, request

from services.intent_service import detect_intent
from services.dialog_service import get_or_create_session, reset_session, set_mode
from services.lesson_service import get_theory_response
from services.progress_service import get_progress_text
from services.quiz_service import start_quiz, process_answer

webhook_bp = Blueprint("webhook", __name__)

GREETINGS = [
    "Привет! Я учебный помощник по Python 😊",
    "Привет! Готов помочь 🚀",
    "Здравствуйте! Давайте учиться 💡"
]

HELP_TEXT = (
    "Я умею:\n"
    "- проводить тест\n"
    "- объяснять Python\n"
    "- показывать прогресс\n\n"
    "Скажи: 'хочу тест' или 'объясни функцию'"
)

UNKNOWN = [
    "Я не понял 😅",
    "Попробуй: тест, обучение или прогресс"
]


@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    user_text = data.get("request", {}).get("original_utterance", "")
    alice_user_id = data.get("session", {}).get("user_id", "test")

    session = get_or_create_session(alice_user_id)

    # если тест идёт
    if session.waiting_for_answer and session.mode == "quiz":
        response_text = process_answer(session, alice_user_id, user_text)

    else:
        intent = detect_intent(user_text)

        if intent == "greeting":
            response_text = random.choice(GREETINGS)

        elif intent == "help":
            response_text = HELP_TEXT

        elif intent == "start_test":
            response_text = start_quiz(session, alice_user_id)

        elif intent == "start_learning":
            set_mode(session, "learning")
            response_text = get_theory_response(user_text)

        elif intent == "show_progress":
            response_text = get_progress_text(alice_user_id)

        elif intent == "exit":
            reset_session(session)
            response_text = "Сессия сброшена 👍"

        else:
            if session.mode == "learning":
                response_text = get_theory_response(user_text)
            else:
                response_text = random.choice(UNKNOWN)

    return jsonify({
        "response": {
            "text": response_text,
            "end_session": False
        },
        "version": "1.0"
    })
