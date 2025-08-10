import os, time, uuid, requests

BASE_URL = os.getenv("BASE_URL", "").rstrip("/")

def wait_ok(url, timeout=120):
    start=time.time()
    while time.time()-start < timeout:
        try:
            r=requests.get(url, timeout=5)
            if r.status_code==200: return True
        except requests.RequestException:
            pass
        time.sleep(2)
    return False

def test_health_endpoints():
    assert wait_ok(f"{BASE_URL}/api/game/health")
    assert wait_ok(f"{BASE_URL}/api/orders/health")
    assert wait_ok(f"{BASE_URL}/api/analytics/health")

def test_game_crud_and_order_flow():
    # create a game
    gtitle = f"Zelda-{uuid.uuid4().hex[:8]}"
    payload = {"title": gtitle, "genre": "adventure", "price": 59.99}
    r = requests.post(f"{BASE_URL}/api/game/games", json=payload, timeout=10)
    assert r.status_code in (200,201)
    created = r.json()
    gid = created.get("id") or created.get("_id") or created.get("game_id")

    # list games includes it
    r = requests.get(f"{BASE_URL}/api/game/games", timeout=10)
    assert r.status_code==200
    assert any((g.get("title")==gtitle) for g in r.json())

    # fetch by id
    r = requests.get(f"{BASE_URL}/api/game/games/{gid}", timeout=10)
    assert r.status_code==200

    # place order
    order_payload = {"game_id": gid, "quantity": 1, "payment_method": "card"}
    r = requests.post(f"{BASE_URL}/api/orders/orders", json=order_payload, timeout=10)
    assert r.status_code in (200,201)
