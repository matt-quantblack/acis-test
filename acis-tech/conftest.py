from chalice.test import Client
from mock.mock import MagicMock, patch
from openai.openai_object import OpenAIObject
import app
from pytest import fixture


@fixture
def test_client() -> Client:
    """ The Chalice test client for pytest """
    with Client(app.app) as client:
        yield client


@fixture
def openai_mock(
    product_name_response_text: str,
    tv_ad_response_text: str,
    radio_ad_response_text: str,
    facebook_ad_response_text: str,
    safety_warning_response_text: str,
) -> MagicMock:
    """
    An open AI mock to return specific text in an OpenAIObject based on words in the prompt.
    This can be used as a fixture in pytest tests
    """

    def side_effect_func(**kwargs):
        response = OpenAIObject()
        first_choice = OpenAIObject
        response.choices = [first_choice]
        if "milkshake maker" in kwargs["prompt"]:
            first_choice.text = product_name_response_text
        elif "tv" in kwargs["prompt"]:
            first_choice.text = tv_ad_response_text
        elif "radio" in kwargs["prompt"]:
            first_choice.text = radio_ad_response_text
        elif "Facebook" in kwargs["prompt"]:
            first_choice.text = facebook_ad_response_text
        elif "safety" in kwargs["prompt"]:
            first_choice.text = safety_warning_response_text
        else:
            first_choice.text = ""
        return response

    with patch("openai.Completion.create") as mock:
        mock.side_effect = side_effect_func
        yield mock


@fixture
def product_name_response_text():
    return "\nProduct names: Awesomeator, Extremator, Terrifyer, Awesomifyer."


@fixture
def product_names_list():
    return ["Awesomeator", "Extremator", "Terrifyer", "Awesomifyer"]


@fixture
def tv_ad_response_text():
    return "\nTV"


@fixture
def radio_ad_response_text():
    return "\nRadio"


@fixture
def facebook_ad_response_text():
    return "\nFacebook"


@fixture
def safety_warning_response_text():
    return "\nSafety"
