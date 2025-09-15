import pytest
from urllib.parse import urlencode
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_answer():

    query_params = {
        "max_value" : True,
        "include_ar": True
    }

    response = client.get(f"/data_analysis?{urlencode(query_params)}")

    assert response.status_code == 200

    # response_data = response.json()

    # assert response_data == {"message": [product]}

def test_assert():
    assert True

def test_breaks():
    assert not True