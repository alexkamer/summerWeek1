from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    questions = relationship("Question", back_populates="category")

class Question(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True)
    question_text = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="questions")
    hints = relationship("Hint", back_populates="question")

class Hint(Base):
    __tablename__ = 'hints'
    
    id = Column(Integer, primary_key=True)
    hint_text = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship("Question", back_populates="hints")

def init_db():
    """Initialize the database and create tables."""
    engine = create_engine('sqlite:///quiz.db')
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get a database session."""
    engine = create_engine('sqlite:///quiz.db')
    Session = sessionmaker(bind=engine)
    return Session() 