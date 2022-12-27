from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

en2ro=pipeline("translation_en_to_ro", model='model/english2romanian/')

app = FastAPI()

class TextToTranslate(BaseModel):
    input_text: str
    
class TextsToTranslate(BaseModel):
    input_texts: list[str]


@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/echo")
def echo(text_to_translate: TextToTranslate):
    return {"message": text_to_translate.input_text}

@app.post("/translate")
def translate(text_to_translate: TextToTranslate):
    return {"message": en2ro(text_to_translate.input_text)}  

@app.post("/transm")
def transm(text_to_translate: TextsToTranslate):
    output=""
    for word in text_to_translate.input_texts:
        output+=str(en2ro(word)) + ' '
    return {"message": output}    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)