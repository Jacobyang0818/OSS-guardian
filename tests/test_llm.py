from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# 載入環境變數
load_dotenv()

key = os.getenv('GEMINI_API_KEY')

if key is None:
    raise ValueError('GEMINI_API_KEY is MISSING! Please check your .env file.')

try:
    # 嘗試初始化 LLM
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash', 
        google_api_key=key
    )
    print('✅ Gemini LLM initialization successful! The Key is valid.')
    print(llm)
except Exception as e:
    print(f"❌ Gemini LLM failed to initialize (Key invalid or quota issue): {e}")