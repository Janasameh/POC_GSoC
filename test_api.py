import requests
import time

BASE = "http://localhost:8000"

def test_flow():
    # 1. Register a device
    print("1. Registering new device...")
    r = requests.post(f"{BASE}/v1/devices", json={"name": "Test Sensor X"})
    assert r.status_code == 200, f"Failed to register. {r.text}"
    device = r.json()
    api_key = device["api_key"]
    print(f"✅ Registered: {device['id']} with key {api_key}")

    # 2. Ingest telemetry (authorized)
    print("\n2. Ingesting telemetry...")
    # Add a few points to see on dashboard
    for temp, hum in [(23.5, 50), (23.8, 52), (24.1, 51), (23.6, 49), (23.5, 48)]:
        r = requests.post(
            f"{BASE}/v1/telemetry",
            headers={"X-Device-Token": api_key},
            json={"values": {"temperature": temp, "humidity": hum}}
        )
        assert r.status_code == 200, f"Failed ingestion. {r.text}"
        time.sleep(0.1)
    print("✅ Ingested telemetry points successfully")

    # 3. Ingest telemetry (unauthorized)
    print("\n3. Testing unauthorized ingestion...")
    r = requests.post(
        f"{BASE}/v1/telemetry",
        headers={"X-Device-Token": "invalid-key"},
        json={"values": {"temperature": 25.0}}
    )
    assert r.status_code == 401
    print("✅ Correctly rejected invalid key")
    
    # 4. Fetch telemetry
    print("\n4. Fetching telemetry for dashboard...")
    r = requests.get(f"{BASE}/v1/telemetry")
    assert r.status_code == 200
    data = r.json()
    print(f"✅ Retrieved {len(data)} telemetry records. Latest: {data[-1]['payload'] if data else 'None'}")

if __name__ == "__main__":
    try:
        test_flow()
        print("\n🎉 All tests passed!")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server. Did you run 'python main.py'?")
