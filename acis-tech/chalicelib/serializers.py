from pydantic import BaseModel


class ProductRequest(BaseModel):
    product_description: str
    vibe_words: str


class GeneratorResponse(BaseModel):
    product_names: list[str]
    tv_ad_young_adults: str
    facebook_ad_parents: str
    radio_ad_parents: str
    safety_warning: str

