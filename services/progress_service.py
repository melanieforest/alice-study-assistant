from models import AnswerAttempt

def get_progress_stats(alice_user_id: str) -> dict:
    attempts = AnswerAttempt.query.filter_by(alice_user_id=alice_user_id).all()

    total = len(attempts)
    correct = sum(1 for attempt in attempts if attempt.is_correct)
    percent = round((correct / total) * 100, 1) if total else 0

    return {
        "total": total,
        "correct": correct,
        "percent": percent
    }

def get_progress_text(alice_user_id: str) -> str:
    stats = get_progress_stats(alice_user_id)

    if stats["total"] == 0:
        return "У вас пока нет результатов. Скажите: хочу тест."

    return (
        f"Ваш текущий прогресс:\n"
        f"Правильных ответов: {stats['correct']} из {stats['total']}.\n"
        f"Успешность: {stats['percent']}%."
    )