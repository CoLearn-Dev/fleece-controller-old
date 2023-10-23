from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base, engine

class ChatSession(Base):
    __tablename__ = "chatsessions"
    c_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    status = Column(String, index=True)
    
    # llm-related
    # https://platform.openai.com/docs/api-reference/completions/create
    stream = Column(Boolean, index=True)
    model = Column(String, index=True)
    messages = Column(String)
    n = Column(Integer, index=True)

class Task(Base):
    __tablename__ = "tasks"
    t_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), index=True)
    status = Column(String, index=True)
    from_c_id = Column(String, ForeignKey("chatsessions.c_id"), index=True)
    plan = Column(String)
    plan_step_num = Column(Integer, index=True)
    plan_current_step = Column(Integer, index=True)
    plan_current_round = Column(Integer, index=True)

    from_c = relationship("ChatSession", foreign_keys=[from_c_id])

class TaskProgress(Base):
    __tablename__ = "taskprogress"
    p_id = Column(String, primary_key=True, index=True)
    from_w_id = Column(String, ForeignKey("workers.w_id"), index=True)
    from_t_id = Column(String, ForeignKey("tasks.t_id"), index=True)
    reported_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    from_w = relationship("Worker", foreign_keys=[from_w_id])
    from_t = relationship("Task", foreign_keys=[from_t_id])

class Worker(Base):
    __tablename__ = "workers"
    w_id = Column(String, primary_key=True, index=True)
    worker_url = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    # TODO: add scheduling information

class WorkerStat(Base):
    __tablename__ = "memstats"
    s_id = Column(String, primary_key=True, index=True)
    from_w_id = Column(String, ForeignKey("workers.w_id"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    nickname = Column(String, index=True)
    gpu_type = Column(String, index=True)
    gpu_available_mem_in_mb = Column(Float, index=True)

    from_w = relationship("Worker", foreign_keys=[from_w_id])

class ConnStat(Base):
    __tablename__ = "connstats"
    s_id = Column(String, primary_key=True, index=True)
    from_w_id = Column(String, ForeignKey("workers.w_id"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    to_w_id = Column(String, ForeignKey("workers.w_id"), index=True)
    latency_in_ms = Column(Float, index=True)

    from_w = relationship("Worker", foreign_keys=[from_w_id])
    to_w = relationship("Worker", foreign_keys=[to_w_id])

class CompStat(Base):
    __tablename__ = "compstats"
    s_id = Column(String, primary_key=True, index=True)
    from_w_id = Column(String, ForeignKey("workers.w_id"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    step_type = Column(String, index=True)
    step_time_in_ms = Column(Float, index=True)

    from_w = relationship("Worker", foreign_keys=[from_w_id])


Base.metadata.create_all(bind=engine)
