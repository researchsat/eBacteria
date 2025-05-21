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

def test_microbial_identification_endpoint():
    response = client.post("/api/v1/analyze/microbial_identification", json={"image_name": "sample_id_image.png"})
    assert response.status_code == 200
    data = response.json()
    assert "image_name" in data
    assert "identified_microbe" in data
    assert data["image_name"] == "sample_id_image.png"
    assert isinstance(data["identified_microbe"], str)
    # Check if the identified microbe is one of the expected species
    expected_species = [
        "Escherichia coli",
        "Staphylococcus aureus",
        "Pseudomonas aeruginosa",
        "Streptococcus pneumoniae",
        "Candida albicans"
    ]
    assert data["identified_microbe"] in expected_species

def test_growth_monitoring_endpoint():
    payload = {
        "image_series": ["trial1_day1.jpg", "trial1_day2.jpg"],
        "duration_hours": 48
    }
    response = client.post("/api/v1/analyze/growth_monitoring", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "image_series" in data
    assert "duration_hours" in data
    assert "growth_status" in data
    assert data["image_series"] == payload["image_series"]
    assert data["duration_hours"] == payload["duration_hours"]
    assert isinstance(data["growth_status"], str)
    # Check if the growth status is one of the expected statuses
    expected_statuses = [
        "No Significant Growth",
        "Low Growth",
        "Moderate Growth",
        "High Growth",
        "Contamination Detected"
    ]
    assert data["growth_status"] in expected_statuses
