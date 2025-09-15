import pytest
from urllib.parse import urlencode
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_mean_value_in_argentina():

    query_params = {
        "mean" : True,
        "include_ar": True
    }

    response = client.get(f"/data_analysis?{urlencode(query_params)}")

    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data["AR"]["mean"], float)



def test_mean_median_and_max_value_in_argentina():

    query_params = {
        "mean" : True,
        "max_value": True,
        "median": True,
        "include_ar": True
    }

    response = client.get(f"/data_analysis?{urlencode(query_params)}")

    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data["AR"]["mean"], float)
    assert isinstance(response_data["AR"]["max"], float)
    assert isinstance(response_data["AR"]["median"], float)


def test_query_mean_median_and_max_value_in_grouped_by_country():

    query_params = {
        "mean" : True,
        "max_value": True,
        "median": True,
        "include_ar": True,
        "include_uy": True,
        "include_cl": True
    }

    response = client.get(f"/data_analysis?{urlencode(query_params)}")

    assert response.status_code == 200

    response_data = response.json()

    for country_code in ["AR", "CL", "UY"]:
        assert isinstance(response_data[country_code]["mean"], float)
        assert isinstance(response_data[country_code]["max"], float)
        assert isinstance(response_data[country_code]["median"], float)


def test_query_mean_median_and_max_value_in_all_countries_globally():

    query_params = {
        "mean" : True,
        "max_value": True,
        "median": True,
        "include_ar": True,
        "include_uy": True,
        "include_cl": True,
        "global_results": True
    }

    response = client.get(f"/data_analysis?{urlencode(query_params)}")

    assert response.status_code == 200

    response_data = response.json()

    response_data["country_codes"] = ["AR", "CL", "UY"]
    assert isinstance(response_data["global_results"]["mean"], float)
    assert isinstance(response_data["global_results"]["max"], float)
    assert isinstance(response_data["global_results"]["median"], float)


def test_query_without_query_params_returns_400_status_code():

    query_params = {}

    response = client.get(f"/data_analysis?{urlencode(query_params)}")

    assert response.status_code == 400
    assert response.json() == {"detail": "Specify at least one metric"}


def test_query_without_country_codes_returns_400_status_code():
    query_params = {"mean" : True}

    response = client.get(f"/data_analysis?{urlencode(query_params)}")

    assert response.status_code == 400
    assert response.json() == {"detail": "At least one country must be included"}


def test_query_data_with_no_results_returns_404_status_code():

    query_params = {"mean" : True, "include_ar": True, "year":-1}

    response = client.get(f"/data_analysis?{urlencode(query_params)}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Filters returned no data"}