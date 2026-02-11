import google.generativeai as genai
from groq import Groq
from config.config import GROQ_API_KEY, GEMINI_API_KEY

# Initialize Clients
groq_client = Groq(api_key=GROQ_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

SYSTEM_PROMPT = """
أنت مساعد ذكي شخصي للمهندس محمد علاء.
تتحدث باللهجة المصرية العامية فقط.
أسلوبك ودود، ذكي، ومختصر.
لا تتحدث بالفصحى أبداً إلا إذا طلب منك ذلك صراحة.
"""

def generate_response(history, new_message):
    # Prepare messages for Groq
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for msg in history:
        # Map internal roles to Groq roles
        role = "user" if msg['role'] == "user" else "assistant"
        messages.append({"role": role, "content": msg['content']})
    
    messages.append({"role": "user", "content": new_message})

    try:
        # 1. Try Groq (Fast & Cheap)
        # Using Llama 3.1 8B Instant for speed and cost efficiency
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant", 
            max_tokens=600,
            temperature=0.7
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}. Fallback to Gemini.")
        return _generate_gemini_fallback(history, new_message)

def _generate_gemini_fallback(history, new_message):
    # 2. Fallback to Gemini (Large Context / Backup)
    full_prompt = SYSTEM_PROMPT + "\n\n"
    for msg in history:
        full_prompt += f"{msg['role']}: {msg['content']}\n"
    full_prompt += f"user: {new_message}\nassistant:"
    
    try:
        response = gemini_model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "معلش، في مشكلة تقنية دلوقتي ومش عارف أرد."