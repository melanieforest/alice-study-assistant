from flask import Blueprint, jsonify, request
from models import db, Question, Topic, AnswerAttempt
from services.quote_service import get_quote

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/questions", methods=["GET"])
def get_questions():
    questions = Question.query.order_by(Question.id.asc()).all()

    result = []
    for question in questions:
        result.append({
            "id": question.id,
            "topic_id": question.topic_id,
            "text": question.text,
            "correct_answer": question.correct_answer,
            "question_type": question.question_type,
            "options": question.options
        })

    return jsonify(result), 200

@api_bp.route("/questions", methods=["POST"])
def create_question():
    data = request.get_json(silent=True) or {}

    topic_title = str(data.get("topic", "Python")).strip()
    text = str(data.get("text", "")).strip()
    correct_answer = str(data.get("correct_answer", "")).strip()
    question_type = str(data.get("question_type", "open")).strip()
    options = data.get("options")

    if not text or not correct_answer:
        return jsonify({
            "error": "Поля text и correct_answer обязательны."
        }), 400

    topic = Topic.query.filter_by(title=topic_title).first()
    if not topic:
        topic = Topic(title=topic_title, description=f"Тема {topic_title}")
        db.session.add(topic)
        db.session.commit()

    question = Question(
        topic_id=topic.id,
        text=text,
        correct_answer=correct_answer,
        question_type=question_type,
        options=options if isinstance(options, str) else None
    )

    db.session.add(question)
    db.session.commit()

    return jsonify({
        "message": "Вопрос успешно создан.",
        "question_id": question.id
    }), 201

@api_bp.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question_api(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": "Вопрос не найден."}), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify({"message": "Вопрос удалён."}), 200

@api_bp.route("/progress/<alice_user_id>", methods=["GET"])
def get_progress_api(alice_user_id):
    attempts = AnswerAttempt.query.filter_by(alice_user_id=alice_user_id).all()

    total = len(attempts)
    correct = sum(1 for attempt in attempts if attempt.is_correct)
    percent = round((correct / total) * 100, 1) if total else 0

    return jsonify({
        "alice_user_id": alice_user_id,
        "total_answers": total,
        "correct_answers": correct,
        "success_percent": percent
    }), 200

@api_bp.route("/quote", methods=["GET"])
def quote():
    result = get_quote()

    return jsonify({
        "success": True,
        "data": result,
        "error": None
    }), 200