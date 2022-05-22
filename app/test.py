from app import api
from fastapi.testclient import TestClient

from app.api import app
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "I am alive!"}

def test_fetch_data():
    response = client.post(
        "/scrape",
        json={
            "tag_name": "trump",
          
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}