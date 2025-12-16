import openai
import os

# 🔥 முக்கியம்: இங்கே ரியல் Key-ஐ போடக்கூடாது! GitHub தடுக்கும்.
# நாம் PythonAnywhere சர்வரில் தனியாக செட் பண்ணிக்கலாம்.
openai.api_key = os.getenv("OPENAI_API_KEY", "PLACEHOLDER_FOR_NOW")

def ask_ai_bot(prompt):
    try:
        # இது ஒரு மாதிரி (Sample) ஃபங்ஷன்
        response = "AI Bot is ready. Configure API Key in Server."
        return response
    except Exception as e:
        return str(e)