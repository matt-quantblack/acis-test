## Product Content Generator

This small app will generate content for a product when provided with a description and vibe words

### Running Locally
Make sure to set your environment variable for the Open AI API key
`OPENAI_API_KEY`

From the `acis-tech` directory run the command

`chalice local`

Webserver will be serverd on 127.0.0.1:8000

### Usage

Post to the api `/v1/generate` endpoint with the example payload below
```json
{
"product_description": "A totally cool thing that makes you 100% more awesome",
"vibe_words": "awesome, extreme, terrifying"
}
```

Example response
```json
{
"product_names": ["AwesomeXtreme Terrorizer","AwesomeXtreme","Extreme Awesome Enhancer"]
"tv_ad_young_adults": "Are you tired of feeling average? Do you want to stand out and be the life of the party? Look no further! The Aweso
"facebook_ad_parents": "Attention all parents! Do you want to step up your cool game and become 100% more awesome? Introducing AwesomeXtre
"radio_ad_parents": "Attention all parents! Are you looking to add a little extra excitement to your daily routine? Look no further! The E
"safety_warning": "WARNING: The Extreme Awesome Enhancer is not a toy and should be used with caution. This device has been designed to i
}
```

### Deployment
Deploy to AWS by running the command

`chalice deploy`
NOTE: AWS credentials are required to be setup in environment variables

### Test
Test api endpoint using pytest

`pytest`