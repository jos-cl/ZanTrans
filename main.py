from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URI = "mongodb+srv://josi-cl:Josi%402001@cluster0.y69u09g.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["db1"]
translations = db["translations"]

app = FastAPI(title="Zambian AI Translator API")


class TranslateRequest(BaseModel):
    source_language: str
    target_language: str
    text: str


class TranslateResponse(BaseModel):
    translated_text: str


@app.post("/translate", response_model=TranslateResponse)
def translate_text(data: TranslateRequest):
    demo_map = {
        ("english", "bemba"): "Mwakabona, muli shani lelo?",
        ("english", "nyanja"): "Moni, muli bwanji lero?",
        ("english", "tonga"): "Mwapona, muli uli lelo?",
    }

    translated = demo_map.get(
        (data.source_language, data.target_language),
        f"[Translated {data.source_language} → {data.target_language}] {data.text}"
    )

    translations.insert_one({
        "source_language": data.source_language,
        "target_language": data.target_language,
        "input_text": data.text,
        "output_text": translated,
        "created_at": datetime.utcnow()
    })

    return {"translated_text": translated}
