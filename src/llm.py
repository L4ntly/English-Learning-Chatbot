import requests
import json



# -----------------------
# SETTINGS 
# -----------------------
OLLAMA_URL = "your-ollama-url-address"
MODEL = "your-model-name"
# --------------------------------
def json_ayikla(metin):
    """LLM'in verdiği metnin içinden sadece JSON kısmını çeker."""
    baslangic = metin.find('{')
    bitis = metin.rfind('}') + 1
    if baslangic != -1 and bitis != 0:
        temiz_metin = metin[baslangic:bitis]

        try:
            return json.loads(temiz_metin)
        except json.JSONDecodeError as e:
            print(f"\n🚨 JSON PARSING ERROR: {e}")           
            print(f"Bozuk Metin:\n{temiz_metin}\n")
            return None

    print(f"\n🚨 SÜSLÜ PARANTEZ BULUNAMADI.\n")
    return None
# --------------------------------
def generate_quiz_question(word):
    print(f"👉 {word} 👈 için {MODEL.upper()} ile quiz sorusu üretiliyor...")    
    prompt = f"""
    You are an expert English teacher. Create a multiple-choice vocabulary quiz question for '{word}'.
    Make sure all wrong options (A, B, C, D) are REAL and VALID English words.
    Word: {word}    
    CRITICAL RULES:
    1. You MUST write a completely UNIQUE and original sentence that clearly demonstrates the meaning of '{word}'.
    2. NEVER use the words "manager", "accounting", or "records" in your sentence.
    3. Replace '{word}' in your sentence with a blank '_____'.
    4. Provide 4 single-word options (A, B, C, D). One MUST be exactly '{word}'.
    5. RANDOMLY place '{word}' as option_a, option_b, option_c, or option_d.
    6. The distractors must be grammatically correct but contextually wrong.

    Return EXACTLY this JSON format. No markdown.
    {{
        "question_text": "[Write your NEW sentence here containing a _____ blank]",
        "option_a": "[Option A word]",
        "option_b": "[Option B word]",
        "option_c": "[Option C word]",
        "option_d": "[Option D word]",
        "correct_answer": "[A, B, C, or D]",
        "explanation": "[A brief and clear explanation in English: Why is this option correct, and what meaning does it add to the sentence?]"
    }}
    """
    try:
        cevap = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "stream": False,
                "format": "json",
                "options": {
                    "num_ctx": 2048
                }
            },
            timeout=120
        )
        yanıt = cevap.json()

        if "error" in yanıt:
            print(f"\n🚨 Ollama'nın Gönderdiği Hata: {yanıt['error']}")
            return None
                    
        metin = yanıt["message"]["content"]
        return json_ayikla(metin)

    except Exception as Hata:
        print(f"Sistem Hatası: {Hata}")
        return None


# ----- CHATBOt için ---------
def generate_chat_response(chat_history):
    """Web arayüzünden gelen sohbet geçmişine (bellek) yanıt üretir."""
    try:
        cevap = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": chat_history,                
                "stream": False,
                "options": {
                    "num_ctx": 2048
                }
            },
            timeout=120
        )
        yanıt = cevap.json()

        if "error" in yanıt:
            return f"🚨 Ollama'nın Gönderdiği Hata: {yanıt['error']}"

        return yanıt["message"]["content"].strip()

    except Exception as Hata:
        return f"Sistem Hatası: {Hata}"

