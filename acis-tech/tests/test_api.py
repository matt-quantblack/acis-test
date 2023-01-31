import json
from mock.mock import MagicMock
from chalice.test import Client
import pytest


@pytest.fixture
def valid_payload() -> dict:
    return dict(
        product_description="A totally cool thing that makes you 100% more awesome",
        vibe_words="awesome, extreme, terrifying"
    )


@pytest.fixture
def invalid_payload() -> dict:
    return dict(product_description="test")


def test_v1_generate_valid_post(
    test_client: Client,
    valid_payload: dict,
    openai_mock: MagicMock,
    product_names_list: list[str],
    tv_ad_response_text: str,
    radio_ad_response_text: str,
    facebook_ad_response_text: str,
    safety_warning_response_text: str,
):
    """
    Given
        - A valid payload is sent to the generate endpoint
    Then
        - a 200 status
        - json_body matches the mocked response text for each field
    """
    response = test_client.http.post(
        "/v1/generate",
        headers={"content-type": "application/json"},
        body=json.dumps(valid_payload)
    )
    assert response.status_code == 200
    assert response.json_body["product_names"] == product_names_list
    assert response.json_body["tv_ad_young_adults"] == tv_ad_response_text
    assert response.json_body["radio_ad_parents"] == radio_ad_response_text
    assert response.json_body["facebook_ad_parents"] == facebook_ad_response_text
    assert response.json_body["safety_warning"] == safety_warning_response_text


def test_v1_generate_invalid_post(
    test_client: Client,
    invalid_payload: dict
):
    """
    Given
        - A in-valid payload is sent to the generate endpoint
    Then
        - a 400 status
    """
    response = test_client.http.post(
        "/v1/generate",
        headers={"content-type": "application/json"},
        body=json.dumps(invalid_payload)
    )
    assert response.status_code == 400
