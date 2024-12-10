import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

os.environ["WANDB_DISABLED"] = "true" # disable weights and biases tool

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
    from transformers import AutoTokenizer, AutoModelForCausalLM

    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
    model = AutoModelForCausalLM.from_pretrained("finetuned", device_map="auto")

    return [tokenizer, model]

tokenizer, model = load_model()
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map='auto')

# Define a function to generate text with different settings
def generate_with_settings(prompt, temperature=1.0, top_k=50, top_p=0.9, max_length=150):
    return generator(
        prompt,
        max_length=max_length,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        repetition_penalty=1.2,
    )

def generate_output(prompt):
    prompt = "Write a detailed tweet about " + prompt

    response = str(generate_with_settings(prompt, temperature=0.25, top_k=5, top_p=0.9)[0]["generated_text"]).replace(prompt, "", 1).strip()

    return response


device = 'cpu'  # Use CPU by default
try:
    device = 'mps'  # Use Apple MPS if available
except:
    pass

class TweetRequest(BaseModel):
    prompt: str  # The content of the tweet
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9
    max_length: int = 280  # Tweets are limited to 280 characters

@app.post("/generate_tweet")
async def generate_tweet(request: TweetRequest):
    # Generate the tweet using the model
    generated_text = generate_output(request.prompt)

    return {"tweet": generated_text}
