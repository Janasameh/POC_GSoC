import requests

BASE = "http://localhost:8000"
VALID_KEY = "secret-device-key-123"

def test_authorized():
    r = requests.post(
        f"{BASE}/v1/telemetry",
        headers={"X-Device-Token": VALID_KEY},
        json={"values": {"temperature": 22.5, "humidity": 60}}
    )
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    print("✅ Authorized:", r.json())

def test_unauthorized():
    r = requests.post(
        f"{BASE}/v1/telemetry",
        json={"values": {"temperature": 22.5}}
    )
    assert r.status_code == 401, f"Expected 401, got {r.status_code}"
    print("✅ Unauthorized (correct 401):", r.json())

def test_get_all():
    r = requests.get(f"{BASE}/v1/telemetry")
    assert r.status_code == 200
    print("✅ Stored telemetry:", r.json())

if __name__ == "__main__":
    test_authorized()
    test_unauthorized()
    test_get_all()
    print("\n🎉 All tests passed!")
