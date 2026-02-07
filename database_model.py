from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String,Text

Base=declarative_base()
class Medicine(Base):
    __tablename__="medicines"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    medical_usage = Column(Text)
    side_effects = Column(Text)
    warnings = Column(Text)
    age_restriction = Column(String(100))