import json, urllib.request, sys

# Read admin token
with open('.login-resp.json') as f:
    token = json.load(f)['data']['token']

auth = 'Bearer ' + token

def api(method, path, body=None):
    url = 'http://localhost:1337/api' + path
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header('Authorization', auth)
    r.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(r, timeout=15)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

cats = [
    {"name": "Train Tour", "slug": "train-tour"},
    {"name": "City Experiences", "slug": "city-experiences"},
    {"name": "Custom Private Tours", "slug": "custom-private"},
    {"name": "Expert-led Journeys", "slug": "expert-led"},
    {"name": "Small Group Departures", "slug": "small-group"},
    {"name": "Ancient Hiking Trails", "slug": "hiking-trails"},
]

types = [
    {"name": "Family", "slug": "family"},
    {"name": "Adventure", "slug": "adventure"},
    {"name": "Cultural", "slug": "cultural"},
    {"name": "Culinary", "slug": "culinary"},
]

print("=== Creating Categories ===")
cat_ids = {}
for c in cats:
    s, d = api('POST', '/categories', {"data": c})
    if s in (200, 201):
        cid = d['data'].get('id') or d['data'].get('documentId')
        cat_ids[c['slug']] = cid
        print(f"  OK: {c['name']} ({cid})")
    else:
        print(f"  FAIL {s}: {c['name']} - {d.get('error',{}).get('message','?')}")

print("\n=== Creating Types ===")
type_ids = {}
for t in types:
    s, d = api('POST', '/types', {"data": t})
    if s in (200, 201):
        tid = d['data'].get('id') or d['data'].get('documentId')
        type_ids[t['slug']] = tid
        print(f"  OK: {t['name']} ({tid})")
    else:
        print(f"  FAIL {s}: {t['name']} - {d.get('error',{}).get('message','?')}")

# Save IDs for tour creation
with open('.test-ids.json', 'w') as f:
    json.dump({"cat_ids": cat_ids, "type_ids": type_ids}, f)

print(f"\nSaved IDs: {len(cat_ids)} categories, {len(type_ids)} types")
