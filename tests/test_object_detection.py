"""
測試：物件偵測查詢
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8001"

print("=" * 70)
print("🎯 測試物件偵測查詢")
print("=" * 70)

query = "我要做一個物件偵測的專案，用python開發，請推薦我一個package"
provider = "gemini"

print(f"\n查詢: {query}")
print(f"Provider: {provider}\n")

try:
    response = requests.get(
        f"{BASE_URL}/stream_analysis",
        params={"query": query, "provider": provider},
        stream=True,
        timeout=180
    )
    
    if response.status_code != 200:
        print(f"❌ 錯誤 ({response.status_code}): {response.text[:300]}")
        exit(1)
    
    print("✅ 連接成功，開始分析...\n")
    
    for line in response.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            if decoded.startswith("data: "):
                data_str = decoded[6:]
                try:
                    data = json.loads(data_str)
                    
                    if data["type"] == "status":
                        print(f"📍 {data['message']}")
                        
                    elif data["type"] == "result":
                        report = data["report"]
                        print(f"\n{'='*70}")
                        print("✅ 分析完成！")
                        print(f"{'='*70}\n")
                        print(f"報告長度: {len(report)} 字元\n")
                        print("報告內容（前 500 字）:")
                        print("-" * 70)
                        print(report[:500])
                        print("-" * 70)
                        break
                        
                    elif data["type"] == "error":
                        print(f"\n❌ 錯誤: {data['message']}")
                        break
                except:
                    pass
    
    print("\n✅ 測試成功！系統可以處理物件偵測查詢")
    
except Exception as e:
    print(f"\n❌ 錯誤: {str(e)}")
