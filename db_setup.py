import os
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publication(Base):
    __tablename__ = 'publications'
     # some things below are nullable due to the nature of the csv we have, since its title and link so we put thoise two first then scrape the link and fill in the rest
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    authors = Column(Text, nullable=True)   
    year = Column(Integer, nullable=True)
    journal = Column(String(255), nullable=True)
    doi = Column(String(100), unique=True)
    link = Column(String(500), nullable= True)
    
    sections = relationship("Section", back_populates="publication")
    
class Section(Base):
    __tablename__ = 'sections'
    
    id = Column(Integer, primary_key=True)
    publication_id = Column(Integer, ForeignKey('publications.id'), nullable=False)
    section_name = Column(String) # referring to abstract or methods or results or discussion
    content = Column(Text, nullable=False)
    
    publication = relationship("Publication", back_populates="sections")
    
    __table_args__ = (UniqueConstraint('publication_id', 'section_name', name='uix_pub_section'),)
    
def init_db(db_url="sqlite:///data/nasa_pubs.db"):
    os.makedirs("data",exist_ok=True)
        
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    print(f"Database initialized at {db_url}")
    return engine
    
if __name__ == "__main__":
    init_db()