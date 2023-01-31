from chalice import Chalice, BadRequestError
from pydantic import ValidationError

from chalicelib.serializers import ProductRequest
from chalicelib.generators import OpenAIGenerator as Generator

app = Chalice(app_name='acis-tech')


def validator(validator_class):
    """
    Generic wrapper for Chalice api endpoints that uses the validator class to validate the payload
    and return the valid pydantic object
    """
    def decorator(func):
        def execute_func(*args, **kwargs):
            try:
                model = validator_class(**app.current_request.json_body)
            except ValidationError as e:
                raise BadRequestError(e.raw_errors)
            return func(*args, model=model, **kwargs)
        return execute_func
    return decorator


@app.route('/v1/generate', methods=['POST'])
@validator(ProductRequest)
def generate(model: None):
    """
    Generates some auto generated content for a product based in the description and vibe words
    """
    response = Generator(model).generate_content()
    return response.json()
