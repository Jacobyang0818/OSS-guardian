import requests
import json
import time

def test_api():
    url = "http://127.0.0.1:8000/analyze"
    payload = {
        "query": "fastapi"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Sending request to {url} with payload: {payload}")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("Error Response:")
            print(response.text)
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Wait a bit for the server to start
    time.sleep(5)
    test_api()
