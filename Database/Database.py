from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Path(Base):
    __tablename__ = 'path'
    pk = Column('pk', Integer, primary_key=True, autoincrement=True)
    path = Column('path', String)

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f'pk={self.pk}, path={self.path}'


engine = create_engine('sqlite:///db.db', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# path = Path(1, 'cesta/k/subotu')
# session.add(path)
# session.commit()
# session.close()
