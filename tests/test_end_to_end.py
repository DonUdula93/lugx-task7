import os, time, uuid, requests

BASE_URL = os.getenv("BASE_URL", "").rstrip("/")
GAME_URL = os.getenv("GAME_URL")
ORDERS_URL = os.getenv("ORDERS_URL")
ANALYTICS_URL = os.getenv("ANALYTICS_URL")

def pick_endpoints():
    if BASE_URL:
        return (f"{BASE_URL}/api/game", f"{BASE_URL}/api/orders", f"{BASE_URL}/api/analytics")
    else:
        return (GAME_URL, ORDERS_URL, ANALYTICS_URL)

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
    g,o,a = pick_endpoints()
    assert wait_ok(f"{g}/health")
    assert wait_ok(f"{o}/health")
    assert wait_ok(f"{a}/health")

def test_game_crud_and_order_flow():
    g,o,a = pick_endpoints()
    title = f"Zelda-{uuid.uuid4().hex[:8]}"
    payload = {"title": title, "genre": "adventure", "price": 59.99}

    r = requests.post(f"{g}/games", json=payload, timeout=10)
    assert r.status_code in (200,201)
    created = r.json()
    gid = created.get("id") or created.get("_id") or created.get("game_id")

    r = requests.get(f"{g}/games", timeout=10)
    assert r.status_code == 200
    assert any((item.get("title")==title) for item in r.json())

    r = requests.get(f"{g}/games/{gid}", timeout=10)
    assert r.status_code == 200

    order_payload = {"game_id": gid, "quantity": 1, "payment_method": "card"}
    r = requests.post(f"{o}/orders", json=order_payload, timeout=10)
    assert r.status_code in (200,201)
