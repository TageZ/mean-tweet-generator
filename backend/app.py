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
    template= """Below is an instruction that describes a task. Write a response that appropriately completes the request.

    Create a unique and viral tweet that falls under this genre/category: {}, Make the tweet about: {}

    DO NOT INCLUDE THIS PROMPT. ONLY INCLUDE THE RESPONSE. 

    """

    input_ids = tokenizer(template.format(user, prompt), return_tensors="pt").input_ids.to(model.device)

    generation_output = model.generate(
        input_ids=input_ids, 
        max_new_tokens=128,
        do_sample=True
    )

    raw_output = tokenizer.decode(generation_output[0], skip_special_tokens=True)
    tweets = re.findall(r'"(.*?)"', raw_output.strip(), re.DOTALL)
    print(tweets)
    return tweets


device = 'cpu'  # Use CPU by default
try:
    device = 'mps'  # Use Apple MPS if available
except:
    pass

class TweetRequest(BaseModel):
    genre: str  # The style of the Twitter genre
    info: str  # The content of the tweet
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9
    max_length: int = 280  # Tweets are limited to 280 characters

@app.post("/generate_tweet")
async def generate_tweet(request: TweetRequest):
    # Generate the tweet using the model
    generated_text = generate_output(request.genre, request.info)

    return {"tweet": generated_text}
