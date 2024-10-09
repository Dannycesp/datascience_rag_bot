import os
import pandas as pd

import minsearch


DATA_PATH = os.getenv("DATA_PATH", "../data/data.csv")


def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)

    documents = df.to_dict(orient="records")
    
    index = minsearch.Index(
        
    text_fields=['Question', 'Answer'],  # Fields where text-based searches will be performed
    keyword_fields=['id']  # If you have an 'id' or unique identifier for each entry
        
    )
    
    index.fit(documents)
    return index