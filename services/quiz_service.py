from models import db, Question, AnswerAttempt


def get_first_question():
    return Question.query.first()


def start_quiz(session, alice_user_id: str) -> str:
    question = get_first_question()

    if not question:
        return "В базе пока нет вопросов для теста."

    session.mode = "quiz"
    session.current_question_id = question.id
    session.waiting_for_answer = True
    db.session.commit()

    return f"Начинаем тест. Первый вопрос: {question.text}"


def process_answer(session, alice_user_id: str, user_text: str) -> str:
    if not session.current_question_id:
        return "Сейчас нет активного вопроса. Скажите: хочу тест."

    question = Question.query.get(session.current_question_id)

    if not question:
        return "Вопрос не найден. Попробуйте начать тест заново."

    user_answer = user_text.strip().lower()
    correct_answer = question.correct_answer.strip().lower()

    is_correct = user_answer == correct_answer

    attempt = AnswerAttempt(
        alice_user_id=alice_user_id,
        question_id=question.id,
        user_answer=user_text,
        is_correct=is_correct
    )
    db.session.add(attempt)

    session.waiting_for_answer = False
    session.current_question_id = None
    db.session.commit()

    if is_correct:
        return "Верно! Тест завершён. Можете сказать: хочу тест, обучение или прогресс."

    return (
        f"Неверно. Правильный ответ: {question.correct_answer}. "
        f"Тест завершён. Можете сказать: хочу тест, обучение или прогресс."
    )
