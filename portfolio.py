# would be using chromadb to make our vector database
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import chromadb
import pandas as pd
import uuid


class Portfolio:
    def __init__(self):
        self.file_path = "assets/portfolio.csv"
        self.df = pd.read_csv(self.file_path)
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name=str(uuid.uuid4()))
        """
        we are using uuid here to name the collection because it was giving error when we were using 
        a fixed name -> saying that collection already exists -> so we fixed this using uuid. now each
        time a random string would be used as name for the collection.
        """

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.df.iterrows():
                self.collection.add(
                    documents=[row['Techstack']],
                    metadatas={'links': row['Links']},
                    ids=[str(uuid.uuid4())]
                )

    def get_query(self, skills):
        return self.collection.query(query_texts=skills, n_results=3).get('metadatas', [])
