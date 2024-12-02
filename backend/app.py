import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the generic LLaMA model and tokenizer
def load_model():
    secret_value_0 = "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"

    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct", token=secret_value_0)

    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B-Instruct", token=secret_value_0, device_map="auto")

    return [tokenizer, model]

tokenizer, model = load_model()

def generate_output(user, prompt):
    # Pass in a sample prompt and generate with the model

    template= """Below is an instruction that describes a task. Write a response that appropriately completes the request.

    Create a detailed tweet made by the following user: {}, with the following amount of likes: 50000. Make the tweet about: {}

    DO NOT INCLUDE THIS PROMPT. ONLY INCLUDE THE RESPONSE
    """

    input_ids = tokenizer(template.format(user, prompt), return_tensors="pt").input_ids.to(model.device)



    # Generate text

    generation_output = model.generate(

        input_ids=input_ids, max_new_tokens=128

    )

    # Decode and print sample output

    return tokenizer.decode(generation_output[0], skip_special_tokens=True)

device = 'cpu'  # Use CPU by default
try:
    device = 'mps'  # Use Apple MPS if available
except:
    pass

class TweetRequest(BaseModel):
    account: str  # The style of the Twitter account
    info: str  # The content of the tweet
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9
    max_length: int = 280  # Tweets are limited to 280 characters

@app.post("/generate_tweet")
async def generate_tweet(request: TweetRequest):
    # Generate the tweet using the model
    generated_text = generate_output(request.account, request.info)

    return {"tweet": generated_text}
