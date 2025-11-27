# main.py
import uvicorn
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    
    print("-------------------------------------------------")
    print("🔥 OSS Guardian 服務啟動中...")
    print(f"預設 Gemini 模型: {os.getenv('GEMINI_MODEL_NAME')} (可於前端切換 Provider)")
    print("-------------------------------------------------")
    print("請前往 http://127.0.0.1:8000/docs 進行測試。")

    uvicorn.run("src.api.server:app", host="0.0.0.0", port=8001, reload=True)