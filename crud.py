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

def create_task(db: Session, task: schemas.ChatCompletionRequest) -> models.Task:
    db_task = models.Task(
        t_id=uuid4().hex,
        model=task.model,
        n=task.n,
        stream=task.stream,
        messages=task.messages.model_dump_json(),
        status="pending",
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def process_task_update(db: Session, w_id: str, task_update: schemas.TaskUpdate):
    logger.info(f"Processing task update from worker {w_id}: {task_update}")
