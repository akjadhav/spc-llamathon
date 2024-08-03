import requests
import pdb
from loguru import logger
import os
import time
import json
import copy
from llama_api_baseten import call_stream_baseten_api

def generate_baseten_stream(
    prompt,
    max_tokens=2048,
    temperature=0.7,
):
    output = None
    for sleep_time in [1, 2, 4, 8, 16, 32]:

        try:
            stream_res = call_stream_baseten_api(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=(temperature if temperature > 1e-4 else 0),
            )

            return stream_res

            # output = ""

            # for content in stream_res:
            #     output += content.decode("utf-8")
            #     print(output)

            # if "error" in res.json():

            #     print("------------------------------------------")
            #     print(f"Model with Error: BASETEN")
            #     print(res.json())
            #     print("------------------------------------------")

            #     if res.json()["error"]["type"] == "invalid_request_error":
            #         return None

            # output = res.json()["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"{e} on response:")
            print(f"Retry in {sleep_time}s..")
            time.sleep(sleep_time)

    if output is None:
        return output

    return ""

def generate_together(
    model,
    messages,
    max_tokens=2048,
    temperature=0.7,
):
    output = None
    for sleep_time in [1, 2, 4, 8, 16, 32]:

        try:
            endpoint = "https://api.together.xyz/v1/chat/completions"


            res = requests.post(
                endpoint,
                json={
                    "model": model,
                    "max_tokens": max_tokens,
                    "temperature": (temperature if temperature > 1e-4 else 0),
                    "messages": messages,
                },
                headers={
                    "Authorization": f"Bearer {os.environ.get('TOGETHER_API_KEY')}",
                },
            )

            if "error" in res.json():

                print("------------------------------------------")
                print(f"Model with Error: {model}")
                print(res.json())
                print("------------------------------------------")

                if res.json()["error"]["type"] == "invalid_request_error":
                    return None

            output = res.json()["choices"][0]["message"]["content"]

            break

        except Exception as e:
            logger.error(f"{e} on response:")
            print(f"Retry in {sleep_time}s..")
            time.sleep(sleep_time)

    if output is None:
        return output

    return output.strip()


# generate_baseten(
#     prompt="What is AGI?",
#     max_tokens=2048,
#     temperature=0.7,
# )