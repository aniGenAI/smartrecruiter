from app.db.mysql import engine, Base
from app.models import candidate, job, interview, evaluation


def init_db():
    Base.metadata.create_all(bind=engine)