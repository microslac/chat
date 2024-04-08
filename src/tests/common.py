from sqlalchemy import orm
from app.database import engine

Session = orm.scoped_session(orm.sessionmaker(bind=engine, autoflush=True))
