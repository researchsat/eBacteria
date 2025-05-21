from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_colony_count_endpoint():
    response = client.post("/api/v1/analyze/colony_count", json={"image_name": "test_image.png"})
    assert response.status_code == 200
    data = response.json()
    assert "image_name" in data
    assert "estimated_colony_count" in data
    assert data["image_name"] == "test_image.png"
    assert isinstance(data["estimated_colony_count"], int)
