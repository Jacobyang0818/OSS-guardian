"""
完整端到端測試：使用 Gemini
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001"

print("=" * 70)
print("🧪 OSS Guardian 完整測試（使用 Gemini）")
print("=" * 70)

# 1. 測試首頁
print("\n1️⃣ 測試首頁訪問...")
try:
    response = requests.get(BASE_URL, timeout=5)
    if response.status_code == 200:
        print("   ✅ 首頁可以訪問")
    else:
        print(f"   ❌ 首頁錯誤: {response.status_code}")
        exit(1)
except Exception as e:
    print(f"   ❌ 無法連接到伺服器: {e}")
    print("   請確認伺服器正在運行")
    exit(1)

# 2. 測試 API
print("\n2️⃣ 測試分析 API（使用 Gemini）...")
query = "Python 物件偵測函式庫"

print(f"   查詢: {query}")

try:
    response = requests.get(
        f"{BASE_URL}/stream_analysis",
        params={"query": query},
        stream=True,
        timeout=120
    )
    
    if response.status_code != 200:
        print(f"   ❌ API 錯誤 ({response.status_code}): {response.text[:200]}")
        exit(1)
    
    print("   ✅ SSE 連接成功")
    print("\n   📡 接收即時狀態更新...")
    
    step_count = 0
    for line in response.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            if decoded.startswith("data: "):
                data_str = decoded[6:]
                try:
                    data = json.loads(data_str)
                    
                    if data["type"] == "status":
                        step_count += 1
                        if step_count <= 5:  # 只顯示前 5 個狀態
                            print(f"      • {data['message']}")
                        elif step_count == 6:
                            print(f"      • ...")
                            
                    elif data["type"] == "result":
                        report = data["report"]
                        print(f"\n   ✅ 分析完成！")
                        print(f"   📊 報告長度: {len(report)} 字元")
                        print(f"\n   📝 報告預覽（前 300 字）:")
                        print("   " + "-" * 66)
                        preview = report[:300].replace('\n', '\n   ')
                        print(f"   {preview}...")
                        print("   " + "-" * 66)
                        break
                        
                    elif data["type"] == "error":
                        print(f"\n   ❌ 錯誤: {data['message']}")
                        exit(1)
                except:
                    pass
    
    print("\n" + "=" * 70)
    print("✅ 測試成功！OSS Guardian 運作正常")
    print("=" * 70)
    print(f"\n🌐 網頁地址: {BASE_URL}")
    print("📌 請打開瀏覽器訪問上述地址")
    
except requests.exceptions.Timeout:
    print("\n   ❌ 請求超時（可能是 Gemini API 配額問題）")
    print("   建議等待 1 分鐘後重試")
except Exception as e:
    print(f"\n   ❌ 測試失敗: {str(e)}")
    import traceback
    traceback.print_exc()
