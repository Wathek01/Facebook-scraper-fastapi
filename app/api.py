from typing import Dict
import pandas as pd
import sqlite3
from facebook_scraper import get_posts
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()



print('Data loaded.......')

@app.get("/")
def hello():
    return "I am alive!"

def fetch_data(tag_name):
    posts=get_posts(tag_name, pages=10)
    df=pd.DataFrame(posts)
    conn = sqlite3.connect('.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE posts(text TEXT, post_id INT)''')

    #data to insert
    for i in range(len(df)):

        text = df.iloc[i]['text']
        post_id = df.iloc[i]['post_id']
        #insert and commit to database
        c.execute('''INSERT INTO posts VALUES(?,?)''', (text ,post_id))
        conn.commit()

    
    


    c.execute('''SELECT * FROM posts''')
    results = c.fetchall()
    return results


class ScrapingRequest(BaseModel):
    tag_name: str

@app.post("/scrape")
def predict(request:ScrapingRequest):
    
    
    print(request.tag_name)
    data = fetch_data(request.tag_name)
    
    return {'data':data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)