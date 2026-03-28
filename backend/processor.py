import spacy, os, io
import speech_recognition as sr
from PIL import Image

try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def detect_context(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["pain","hospital","emergency","medical","doctor","blood","heart","fever","symptoms","diagnosis","patient","medicine"]):
        return "medical"
    elif any(w in t for w in ["traffic","accident","road","crash","jam","vehicle","collision","highway"]):
        return "traffic"
    elif any(w in t for w in ["weather","rain","storm","flood","temperature","humidity","wind","forecast"]):
        return "weather"
    elif any(w in t for w in ["news","breaking","update","report","headline","election"]):
        return "news"
    return "general"

def process_text(text: str) -> dict:
    doc = nlp(text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    keywords = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return {"input_type": "text", "raw_content": text, "entities": entities, "keywords": keywords[:15], "context": detect_context(text)}

def process_audio(audio_bytes: bytes) -> dict:
    recognizer = sr.Recognizer()
    try:
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        result = process_text(text)
        result["input_type"] = "voice"
        return result
    except Exception as e:
        return {"input_type": "voice", "raw_content": f"Could not transcribe: {str(e)}", "entities": [], "context": "general"}

def process_image_ocr(image_bytes: bytes) -> dict:
    try:
        import pytesseract
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        if text.strip():
            result = process_text(text)
            result["input_type"] = "image_ocr"
            result["ocr_text"] = text
            return result
    except Exception as e:
        pass
    return {"input_type": "image", "raw_content": "Image uploaded for visual AI analysis", "entities": [], "context": "general"}

def process_news_url(url: str) -> dict:
    try:
        from newspaper import Article
        article = Article(url)
        article.download()
        article.parse()
        text = f"{article.title}. {article.text[:2000]}"
        result = process_text(text)
        result["input_type"] = "news"
        result["title"] = article.title
        return result
    except Exception as e:
        return {"input_type": "news", "raw_content": f"Could not fetch: {str(e)}", "entities": [], "context": "news"}
