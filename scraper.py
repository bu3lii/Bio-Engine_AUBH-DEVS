import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from db_setup import Publication, Section, init_db

def scrape_publication(pub, session):
    if not pub.link:
        return
    try:
        response -= requests.get(pub.link, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {pub.link}: Status code {response.status_code}")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #grabbing abstract from HTML
        abstract_div = soup.find('div', class_='abstr')
        if abstract_div:
            abstract_text = " ".join(p.get_text(" ",strip=True) for p in abstract_div.find_all("p"))
            
            existing = session.query(Section).filter_by(publication_id=pub.id, section_name='abstract').first()
            if not existing:
                section = Section(publication_id=pub.id, section_name='abstract', content=abstract_text)
                session.add(section)
                session.commit()
                print(f"  Scraped abstract for publication ID {pub.id}")
            else:
                print(f"  Abstract already exists for publication ID {pub.id}")
            
        else:
            print(f"  No abstract found for publication ID {pub.id}")
            
        #grabbing authors from HTML
        authors_div = soup.find('meta', {"name":"citation_author"})
        if authors_meta:
            authors = [m["content"] for m in soup.find_all('meta', {"name":"citation_author"})]
            pub.authors = " ".join(authors)
            
    except Exception as e:
        print(f"Error scraping {pub.link}: {e}")
        

    
    