import requests
import sys

def test_health():
    try:
        response = requests.get('http://localhost:5000/api/health')
        assert response.status_code == 200, f"Status code: {response.status_code}"
        data = response.json()
        assert data.get('status') == 'healthy', f"Response: {data}"
        print("✅ Health check passed.")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_health()
