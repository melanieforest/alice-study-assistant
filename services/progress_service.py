from models import AnswerAttempt


def get_progress_text(alice_user_id: str) -> str:
    attempts = AnswerAttempt.query.filter_by(alice_user_id=alice_user_id).all()

    if not attempts:
        return "Пока нет результатов теста."

    total = len(attempts)
    correct = sum(1 for a in attempts if a.is_correct)

    return (
        f"📊 Прогресс:\n"
        f"Правильных: {correct} из {total}\n"
        f"Успешность: {round(correct/total*100)}%"
    )