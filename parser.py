import pandas as pd
from sqlalchemy.orm import sessionmaker
from db_setup import Publication, Section, init_db

def load_csv(csv_path="data/SB_publication_PMC.csv"):
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    df = pd.read_csv(csv_path)
    print(f"CSV loaded with {len(df)} rows and columns: {df.columns}")
    
    for _, row in df.iterrows():
        print(f" Adding : {row.get('Title')}")
        #create publication entry
        pub = Publication(
            title = row.get("Title"),
            authors = None,
            year = None,
            journal = None,
            doi = None,
            link=row.get("Link","")
        )
        session.add(pub)
         
    session.commit()
    print(f"Loaded {len(df)} publications from {csv_path}")
    
if __name__ == "__main__":
    load_csv("data/SB_publication_PMC.csv")
