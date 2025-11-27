import requests
import json
import time
import os

def verify_frontend():
    base_url = "http://127.0.0.1:8000"
    
    print("1. Verifying Frontend (GET /)...")
    try:
        response = requests.get(base_url + "/")
        if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
            print("✅ Frontend is accessible.")
        else:
            print(f"❌ Frontend check failed. Status: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Frontend check failed: {e}")
        return

    print("\n2. Verifying Analysis (GET /stream_analysis)...")
    markdown_report = ""
    try:
        # SSE is a GET request with stream=True
        # Test OpenRouter provider
        print("   Testing with provider=openrouter...")
        response = requests.get(base_url + "/stream_analysis", params={"query": "fastapi", "provider": "openrouter"}, stream=True)
        
        if response.status_code == 200:
            print("✅ Connected to SSE stream.")
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        data_str = decoded_line[6:]
                        try:
                            data = json.loads(data_str)
                            if data["type"] == "status":
                                print(f"   Status Update: {data['message']}")
                            elif data["type"] == "result":
                                markdown_report = data["report"]
                                print("✅ Received Final Report.")
                                break
                            elif data["type"] == "error":
                                print(f"❌ Error from SSE: {data['message']}")
                                return
                        except json.JSONDecodeError:
                            pass
        else:
            print(f"❌ Analysis failed. Status: {response.status_code}")
            print(f"Response Body: {response.text}")
            return
            
        if "# OSS Guardian Due Diligence Report" in markdown_report:
             print("✅ Report is structured correctly.")
        else:
             print("⚠️ Report structure might be missing headers.")
             print(f"Snippet: {markdown_report[:100]}...")
             
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return

    print("\n3. Verifying PDF Generation (POST /report/pdf)...")
    try:
        payload = {"markdown": markdown_report}
        response = requests.post(base_url + "/report/pdf", json=payload)
        if response.status_code == 200 and response.headers["content-type"] == "application/pdf":
            with open("test_report.pdf", "wb") as f:
                f.write(response.content)
            print("✅ PDF generated successfully (saved to test_report.pdf).")
        else:
            print(f"❌ PDF generation failed. Status: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")

if __name__ == "__main__":
    # Wait for server to start
    time.sleep(5)
    verify_frontend()
