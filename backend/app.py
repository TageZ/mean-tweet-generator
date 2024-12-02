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

model_path = './finetuned'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

device = 'cpu'
try:
    device = 'mps'
except:
    pass

generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

class AITAPostRequest(BaseModel):
    topic: str
    judgment: str
    temperature: float = 0.7
    top_k: int = 100
    top_p: float = 0.9
    max_length: int = 512

@app.post("/generate")
async def generate_aita_post(request: AITAPostRequest):
        
    prompt = (
        "Write a Reddit AITA post in the following format:\n"
        "Topic: <Topic>\n"
        "Judgment: <Judgment>\n"
        "Response: <Here, write the main content of the post. Provide background, actions, and justification.>\n"
        "AITA?\n\n"
        f"Topic: {request.topic}\n"
        f"Judgment: {request.judgment.upper()}\n"
    )

    generated_texts = generator(
        prompt,
        max_length=request.max_length,
        temperature=request.temperature,
        top_k=request.top_k,
        top_p=request.top_p,
    )

    cleaned_texts = [
        re.sub(r'[\\\n\"#  ]+', ' ', generated_text['generated_text']).strip()
        for generated_text in generated_texts
    ]

    if "Response:" in cleaned_texts[0]:
        post_content = cleaned_texts[0].split("Response: ")[2].strip()
    else:
        post_content = cleaned_texts[0]

    post_content = post_content + "..."

    if not post_content.endswith("AITA?"):
        post_content += " AITA?"

    return {"post": post_content}
