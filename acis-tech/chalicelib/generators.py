import abc
from .serializers import ProductRequest, GeneratorResponse
import os
import openai


class ContentGenerator(metaclass=abc.ABCMeta):
    """ Interface for any content generation obejct"""

    def __init__(self, product_request: ProductRequest):
        self.product_request = product_request

    @abc.abstractmethod
    def generate_content(self) -> GeneratorResponse:
        """ Method to generate context from the generator based on the product_request data """
        raise NotImplementedError


class OpenAIGenerator(ContentGenerator):
    """
    OpenAIGenerator implementation of content generator
    to generate ads from product descriptions
    """

    def __init__(self, product_request: ProductRequest):
        """
        :param product_request: Details of the product to generate content on
        """
        super().__init__(product_request)
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_content(self) -> GeneratorResponse:
        """ Generates the content for product details in the product_request object """
        return GeneratorResponse(
            product_names=self._generate_product_names(),
            tv_ad_young_adults=self._generate_tv_ad_young_adults(),
            facebook_ad_parents=self._generate_facebook_ad_parents(),
            radio_ad_parents=self._generate_radio_ad_parents(),
            safety_warning=self._generate_safety_warning(),
        )

    @staticmethod
    def _execute_request(
        prompt: str,
        model: str = "text-davinci-003",
        temperature: float = 0.5,
        max_tokens: float = 100,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
    ):
        """
        Helper function that executes the api call to OpenAI
        :param prompt: Text to prompt the open ai generator
        :param model: Type of open ai model to use
        :param temperature: parameter for openai
        :param max_tokens: parameter for openai
        :param top_p: parameter for openai
        :param frequency_penalty: parameter for openai
        :param presence_penalty: parameter for openai
        :return: The text extracted from the first option in the OpenAI response
        """
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response.choices[0].text if response.choices else None

    def _generate_product_names(self) -> list[str]:
        """
        Uses a script to prompt the open ai to suggest product names.
        :return: A list of product names
        """
        prompt = (
            f"Product description: A home milkshake maker\n"
            f"Seed words: fast, healthy, compact.\n"
            f"Product names: HomeShaker, Fit Shaker, QuickShake, Shake Maker\n\n"
            f"Product description: {self.product_request.product_description}\n" 
            f"Seed words: {self.product_request.vibe_words}."
        )
        text = self._execute_request(prompt=prompt, max_tokens=60)

        # extract a list of names from the response text into a list
        names = text[:-1].replace("\nProduct names: ", "").split(", ")
        return names

    def _generate_tv_ad_young_adults(self) -> str:
        """ Generates text for a tv ad for young adults """
        return self._execute_request(
            prompt=self._generate_prompt_for_ad(media="tv", audience="adults")
        )

    def _generate_facebook_ad_parents(self):
        """ Generates text for a facebook ad for parents """
        return self._execute_request(
            prompt=self._generate_prompt_for_ad(media="Facebook", audience="parents")
        )

    def _generate_radio_ad_parents(self):
        """ Generates text for a radio ad for parents """
        return self._execute_request(
            prompt=self._generate_prompt_for_ad(media="radio", audience="parents")
        )

    def _generate_safety_warning(self):
        """ Generates text for a safety warning for the product """
        prompt = (
            "Write a safety warning for this product"
            f"Product: {self.product_request.product_description}"
        )
        return self._execute_request(prompt=prompt)

    def _generate_prompt_for_ad(self, media: str, audience: str) -> str:
        """
        Helper function to generate the prompt for an ad for a specific media and audience type
        :param media: Type of media the ad is designed for
        :param audience: The audience the ad is targeted at
        :return: The full prompt to use in openai
        """
        return (
            f"Write a creative ad for the following product to "
            f"run on {media} aimed at {audience}:\n"
            f"Product: {self.product_request.product_description}"
        )
