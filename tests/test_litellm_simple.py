"""
簡化測試：直接用 LiteLLM 測試 OpenRouter
"""
import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv(override=True)

api_key = os.getenv("OPENROUTER_API_KEY")
model = "mistralai/mistral-7b-instruct:free"

print("=" * 60)
print("🧪 測試 CrewAI LLM with OpenRouter")
print("=" * 60)
print(f"Model: {model}")
print(f"API Key: {api_key[:15]}...")

try:
    llm = LLM(
        model=f"openai/{model}",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    
    print("\n✅ LLM 初始化成功")
    print("\n📤 發送測試訊息...")
    
    # 簡單的測試
    response = llm.call(["Say hello in 5 words"])
    
    print(f"\n✅ 成功")
    print(f"📥 回應: {response}")
    print("\n" + "=" * 60)
    print("OpenRouter 完全可用！")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ 錯誤: {str(e)}")
    import traceback
    traceback.print_exc()
