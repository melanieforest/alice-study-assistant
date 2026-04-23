import random
from models import db, Question, AnswerAttempt


def get_all_questions():
    return Question.query.all()


def start_quiz(session, alice_user_id: str) -> str:
    questions = get_all_questions()

    if not questions:
        return "Вопросов пока нет."

    random.shuffle(questions)

    session.mode = "quiz"
    session.question_index = 0
    session.score = 0
    session.waiting_for_answer = True

    session._cache = [q.id for q in questions]

    first = questions[0]
    session.current_question_id = first.id

    db.session.commit()

    return f"🎯 Тест начался!\n\nВопрос 1:\n{first.text}"


def process_answer(session, alice_user_id: str, user_text: str) -> str:
    questions = Question.query.order_by(Question.id.asc()).all()

    if not questions:
        return "Вопросы для теста не найдены."

    if session.current_question_id is None:
        return "Сейчас нет активного вопроса. Скажите: хочу тест."

    current_question = Question.query.get(session.current_question_id)

    if not current_question:
        return "Ошибка: текущий вопрос не найден. Начните тест заново."

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
        final_score = session.score
        total = len(questions)

        session.mode = None
        session.waiting_for_answer = False
        session.current_question_id = None
        session.question_index = 0
        session.score = 0

        db.session.commit()

        return (
            f"Тест завершён 🎯\n"
            f"Результат: {final_score} из {total}\n"
            f"Скажите: хочу тест, обучение или прогресс."
        )

    next_question = questions[next_index]

    session.question_index = next_index
    session.current_question_id = next_question.id
    session.waiting_for_answer = True

    db.session.commit()

    if is_correct:
        return f"Верно 👍\nСледующий вопрос: {next_question.text}"

    return (
        f"Неверно ❌ Правильный ответ: {current_question.correct_answer}\n"
        f"Следующий вопрос: {next_question.text}"
    )