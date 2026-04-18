from models import AnswerAttempt


def get_progress_text(alice_user_id: str) -> str:
    attempts = AnswerAttempt.query.filter_by(alice_user_id=alice_user_id).all()

    if not attempts:
        return "У вас пока нет результатов. Скажите: хочу тест."

    total = len(attempts)
    correct = sum(1 for attempt in attempts if attempt.is_correct)

    return f"Ваш текущий результат: {correct} правильных ответов из {total}."
