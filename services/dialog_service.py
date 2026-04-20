from models import db, SessionState


def get_or_create_session(alice_user_id: str) -> SessionState:
    session = SessionState.query.filter_by(alice_user_id=alice_user_id).first()

    if not session:
        session = SessionState(
            alice_user_id=alice_user_id,
            mode=None,
            current_topic=None,
            current_question_id=None,
            waiting_for_answer=False,
            question_index=0,
            score=0
        )
        db.session.add(session)
        db.session.commit()

    return session


def reset_session(session: SessionState) -> None:
    session.mode = None
    session.current_topic = None
    session.current_question_id = None
    session.waiting_for_answer = False
    session.question_index = 0
    session.score = 0
    db.session.commit()


def set_mode(session: SessionState, mode: str) -> None:
    session.mode = mode
    session.current_question_id = None
    session.waiting_for_answer = False
    session.question_index = 0
    session.score = 0
    db.session.commit()