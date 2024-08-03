import requests # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

# model_id = os.getenv("BASETEN_MODEL_ID")
# baseten_api_key = os.getenv("BASETEN_API_KEY")

model_id = os.getenv("BASETEN_405_MODEL_ID")
baseten_api_key = os.getenv("BASETEN_405_API_KEY")

def call_no_stream_baseten_api(prompt, max_tokens=5000, temperature=0.9):
    data = {
        "prompt": prompt,
        "stream": False,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    res = requests.post(
        f"https://model-{model_id}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {baseten_api_key}"},
        json=data,
        stream=False
    )

    return res.json()

def call_stream_baseten_api(prompt, max_tokens=5000, temperature=0.9):
    data = {
        "prompt": prompt,
        "stream": True,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    res = requests.post(
        f"https://model-{model_id}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {baseten_api_key}"},
        json=data,
        stream=True
    )

    return res

# data = {
#     "prompt": "Generate example tests using Jest.",
#     "stream": True,
#     "max_tokens": 5000,
#     "temperature": 0.9
# }

# # Call model endpoint
# res = requests.post(
#     f"https://model-{model_id}.api.baseten.co/production/predict",
#     headers={"Authorization": f"Api-Key {baseten_api_key}"},
#     json=data,
#     stream=True
# )

# # Print the generated tokens as they get streamed
# for content in res.iter_content():
#     print(content.decode("utf-8"), end="", flush=True)