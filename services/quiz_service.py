from models import db, Question, AnswerAttempt

def get_all_questions():
    return Question.query.order_by(Question.id.asc()).all()

def start_quiz(session, alice_user_id: str) -> str:
    questions = get_all_questions()

    if not questions:
        return "В базе пока нет вопросов для теста."

    first_question = questions[0]

    session.mode = "quiz"
    session.question_index = 0
    session.score = 0
    session.current_question_id = first_question.id
    session.waiting_for_answer = True
    db.session.commit()

    return f"Начинаем тест. Вопрос 1: {first_question.text}"

def process_answer(session, alice_user_id: str, user_text: str) -> str:
    questions = get_all_questions()

    if not questions:
        return "Вопросы для теста не найдены."

    if session.current_question_id is None:
        return "Сейчас нет активного вопроса. Скажите: хочу тест."

    current_question =Question.query.get(session.current_question_id)
    if current_question is None:
        return "Текущий вопрос не найден. Скажите: хочу тест."

    user_answer = user_text.strip().lower()
    correct_answer = current_question.correct_answer.strip().lower()
    is_correct = user_answer == correct_answer

    attempt = AnswerAttempt(
        alice_user_id=alice_user_id,
        question_id=current_question.id,
        user_answer=user_text,
        is_correct=is_correct
    )
    db.session.add(attempt)

    if is_correct:
        session.score += 1

    next_index = session.question_index + 1

    if next_index >= len(questions):
        total_questions = len(questions)
        final_score = session.score
        session.waiting_for_answer = False
        session.current_question_id = None
        session.mode = None
        session.question_index = 0
        session.score = 0
        db.session.commit()

        if is_correct:
            return (
                f"Верно! Тест завершён. "
                f"Ваш результат: {final_score} из {total_questions}. "
                f"Можете сказать: хочу тест, обучение или прогресс."
            )
        return (
            f"Неверно. Правильный ответ: {current_question.correct_answer}. "
            f"Тест завершён. Ваш результат: {final_score} из {total_questions}. "
            f"Можете сказать: хочу тест, обучение или прогресс."
        )

    next_question = questions[next_index]
    session.question_index = next_index
    session.current_question_id = next_question.id
    session.waiting_for_answer = True
    db.session.commit()

    if is_correct:
        return f"Верно! Следующий вопрос {next_index + 1}: {next_question.text}"

    return (
        f"Неверно. Правильный ответ: {current_question.correct_answer}. "
        f"Следующий вопрос {next_index + 1}: {next_question.text}"
    )