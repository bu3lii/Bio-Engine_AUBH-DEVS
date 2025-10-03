import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from db_setup import Publication, Section, init_db

CATEGORY_MAP = {
    "abstract": "Abstract",
    "introduction": "Introduction",
    "background": "Introduction",
    "methods": "Methodology",
    "materials and methods": "Methodology",
    "methodology": "Methodology",
    "results": "Results",
    "analysis": "Results",
    "discussion": "Discussion",
    "conclusion": "Conclusion",
    "conclusions": "Conclusion",
}

def categorize(title:str) -> str:
    title = title.lower()
    for key, category in CATEGORY_MAP.items():
        if key in title:
            return category
    return "Other"

def scrape_publication(pub):
    pmc_id = pub.link.split("PMC")[-1].strip("/")
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC{pmc_id}"
    
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, 'lxml-xml')
    
    sections = []
    
    for sec in soup.find_all('sec'):
        title_tag = sec.find('title')
        title = title_tag.get_text(strip=True) if title_tag else "Untitled Section"
        content = ' '.join(p.get_text(strip=True) for p in sec.find_all('p'))
        
        if content.strip():
            section_name = categorize(title)
            sections.append(Section(publication_id=pub.id, section_name=section_name, content=content))
    return sections

def populate_sections():
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    pubs = session.query(Publication).all()
    for pub in pubs:
        if not pub.link:
            continue
        if session.query(Section).filter_by(publication_id=pub.id).count()>0:
            continue
        
        print(f"Scraping publication ID {pub.id} with link {pub.link}")
        try:
            sections = scrape_publication(pub)
        except Exception as e:
            print(f"Failed to scrape {pub.link}: {e}")
            continue
        
        #for name,content in sections:
         #   sec = Section(publication_id=pub.id, section_name=name, content=content)
          #  session.add(sec)
        #session.commit()
        
        for sec in sections:
            existing= session.query(Section).filter_by(publication_id=pub.id, section_name=sec.section_name).first()
            if(existing):
                existing.content += "\n\n" + sec.content
            else:
                session.add(sec)
        session.commit()
        
if __name__ == "__main__":
    populate_sections()