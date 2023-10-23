from uuid import uuid4
from sqlalchemy.orm import Session
from logging import getLogger


import models, schemas

logger = getLogger()

def register_worker(db: Session, worker_url: str):
    db_worker = db.query(models.Worker).filter(models.Worker.worker_url == worker_url).first()
    if db_worker:
        return db_worker  # skip registering if already registered
    db_worker = models.Worker(w_id=uuid4().hex, worker_url=worker_url)
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

def deregister_worker(db: Session, w_id: str):
    db_worker = db.query(models.Worker).filter(models.Worker.w_id == w_id).first()
    db.delete(db_worker)
    db.commit()
    return db_worker

def create_chat_session(db: Session, chat_session: schemas.ChatCompletionRequest) -> models.ChatSession:
    db_chat_session = models.ChatSession(
        c_id=uuid4().hex,
        status="pending",
        stream=chat_session.stream,
        model=chat_session.model,
        messages=chat_session.messages.model_dump_json(),
        n=chat_session.n,
    )
    db.add(db_chat_session)
    db.commit()
    db.refresh(db_chat_session)
    return db_chat_session

def create_task_progress(db: Session, w_id: str, task_update: schemas.TaskUpdate):
    logger.debug(f"Processing task update from worker {w_id}: {task_update}")
    db_task_progress = models.TaskProgress(
        p_id=uuid4().hex,
        from_w_id=w_id,
        from_t_id=task_update.t_id,
    )
    db.add(db_task_progress)
    db.commit()
    db.refresh(db_task_progress)
    return db_task_progress
