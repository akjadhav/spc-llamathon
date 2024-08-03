from substrate import Substrate, Llama3Instruct70B
from dotenv import load_dotenv
import os

load_dotenv()

substrate_api_key = os.getenv("SUBSTRATE_API_KEY")

substrate = Substrate(api_key=substrate_api_key)

model = Llama3Instruct70B(
    prompt="Who is Don Quixote?",
    num_choices=2,
    temperature=0.4,
    max_tokens=800,
)

response = substrate.run(model)

summary_out = response.get(model)
print(summary_out)