import requests
from dotenv import load_dotenv
import os

load_dotenv()

model_id = os.getenv("BASETEN_MODEL_ID")
baseten_api_key = os.getenv("BASETEN_API_KEY")

messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]
data = {
    "messages": messages,
    "stream": True,
    "max_new_tokens": 512,
    "temperature": 0.9
}

# Call model endpoint
res = requests.post(
    f"https://model-{model_id}.api.baseten.co/production/predict",
    headers={"Authorization": f"Api-Key {baseten_api_key}"},
    json=data,
    stream=True
)

# Print the generated tokens as they get streamed
for content in res.iter_content():
    print(content.decode("utf-8"), end="", flush=True)