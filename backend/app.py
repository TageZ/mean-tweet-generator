import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the generic LLaMA model and tokenizer
model_path = './llama'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

device = 'cpu'  # Use CPU by default
try:
    device = 'mps'  # Use Apple MPS if available
except:
    pass

generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

class TweetRequest(BaseModel):
    account_style: str  # The style of the Twitter account
    content: str  # The content of the tweet
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9
    max_length: int = 280  # Tweets are limited to 280 characters

@app.post("/generate_tweet")
async def generate_tweet(request: TweetRequest):
    # Format the prompt to mimic the tweet
    prompt = (
        f"Generate a tweet in the style of the account '{request.account_style}'.\n"
        f"Tweet content: {request.content}\n"
        "Tweet:\n"
    )

    # Generate the tweet using the model
    generated_texts = generator(
        prompt,
        max_length=request.max_length,
        temperature=request.temperature,
        top_k=request.top_k,
        top_p=request.top_p,
        num_return_sequences=1  # Generate a single tweet
    )

    # Clean up the generated text
    cleaned_text = re.sub(r'[\\\n\"#]+', ' ', generated_texts[0]['generated_text']).strip()

    # Ensure the output adheres to Twitter's character limit
    if len(cleaned_text) > 280:
        cleaned_text = cleaned_text[:277] + "..."

    return {"tweet": cleaned_text}
