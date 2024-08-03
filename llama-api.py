import requests

# Replace the empty string with your model id below
model_id = "nwxln67w"
baseten_api_key = "8XFRY8fC.VGNvc7V9Gt8AdMh88Wx03cStmxNr28N1"

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