"""
PulseGrid BRICS - Verification Test Suite
Tests FastAPI routes, optimizer, federated engine, and Gemini service locally.
"""

import sys
import os

# Set UTF-8 encoding for standard output on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from backend.main import app

def run_all_tests():
    print("[*] Starting PulseGrid BRICS Automated Verification Suite...\n")
    client = TestClient(app)

    # 1. Test Health Endpoint
    print("[1/7] Testing GET /api/health...")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health = res.json()
    print(f"  [PASS] Health Status: {health['status']}, Model: {health['model']}, Tracked PHCs: {health['phcs_tracked']}")

    # 2. Test PHC Network Telemetry
    print("[2/7] Testing GET /api/phcs...")
    res = client.get("/api/phcs")
    assert res.status_code == 200
    phcs = res.json()
    print(f"  [PASS] Total facilities evaluated: {phcs['total_facilities']}, Critical shortages: {phcs['critical_stockouts_count']}")

    # 3. Test Critical Inventory
    print("[3/7] Testing GET /api/inventory/critical...")
    res = client.get("/api/inventory/critical")
    assert res.status_code == 200
    crit = res.json()
    print(f"  [PASS] Critical facilities identified: {crit['count']}")

    # 4. Test Redistribution Optimizer
    print("[4/7] Testing GET /api/redistribution/plan...")
    res = client.get("/api/redistribution/plan")
    assert res.status_code == 200
    plan = res.json()
    print(f"  [PASS] Generated {plan['total_proposals']} automated cross-district transfer recommendations.")
    if plan['plan']:
        first = plan['plan'][0]
        print(f"    - Sample: Transfer {first['transfer_quantity']} {first['medicine']['unit']} of {first['medicine']['name']} from {first['donor']['name']} to {first['recipient']['name']} ({first['distance_km']} km, ETA: {first['estimated_transit_hours']} hrs)")

    # 5. Test Forecast Engine
    print("[5/7] Testing GET /api/forecast...")
    res = client.get("/api/forecast?facility_id=PHC-MH-GAD-01")
    assert res.status_code == 200
    fc = res.json()
    print(f"  [PASS] Forecast generated for {fc['facility_id']}, Model: {fc['forecast_model']}, Curves: {len(fc['curves'])}")

    # 6. Test BRICS Federated Mesh
    print("[6/7] Testing GET /api/federated/mesh & POST /api/federated/round...")
    res = client.get("/api/federated/mesh")
    assert res.status_code == 200
    mesh = res.json()
    print(f"  [PASS] Participating Nations: {mesh['participating_nations']}, Convergence Accuracy: {mesh['convergence_accuracy_percent']}%")

    res_round = client.post("/api/federated/round")
    assert res_round.status_code == 200
    round_data = res_round.json()
    print(f"  [PASS] Triggered Round: {round_data['round']}, Status: {round_data['status']}")

    # 7. Test Gemini 3.8 Flash Triage Copilot
    print("[7/7] Testing POST /api/gemini/triage...")
    res_triage = client.post("/api/gemini/triage", json={
        "prompt": "Triage urgent snakebite antivenom shortage at PHC Bhamragad",
        "facility_id": "PHC-MH-GAD-01"
    })
    assert res_triage.status_code == 200
    triage = res_triage.json()
    print(f"  [PASS] Gemini Triage Output generated from: {triage['source']}")
    print(f"    Snippet: {triage['analysis'][:120]}...\n")

    # 8. Test Frontend Static Serves
    print("[Bonus] Testing UI File Availability...")
    res_index = client.get("/")
    assert res_index.status_code == 200, "Index page failed to serve"
    res_pitch = client.get("/pitch")
    assert res_pitch.status_code == 200, "Pitch deck failed to serve"
    print("  [PASS] Command War Room Dashboard (/) is serving OK")
    print("  [PASS] Judge Pitch Deck (/pitch) is serving OK")

    print("\nALL 8 TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_all_tests()
