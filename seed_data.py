import json, urllib.request, sys

STRAPI = 'http://localhost:1337'

def get_token():
    # Try login first
    data = json.dumps({"email":"admin@tour.local","password":"Admin12345!"}).encode()
    r = urllib.request.Request(f'{STRAPI}/admin/login', data=data, method='POST')
    r.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(r, timeout=10)
        return json.loads(resp.read())['data']['token']
    except:
        # Try register
        data2 = json.dumps({
            "email":"admin@tour.local","password":"Admin12345!",
            "firstname":"Admin","lastname":"Tour"
        }).encode()
        r2 = urllib.request.Request(f'{STRAPI}/admin/register-admin', data=data2, method='POST')
        r2.add_header('Content-Type', 'application/json')
        resp2 = urllib.request.urlopen(r2, timeout=10)
        return json.loads(resp2.read())['data']['token']

token = get_token()
auth = 'Bearer ' + token
print(f"Auth OK (token len={len(token)})")

def api(method, path, body=None):
    url = STRAPI + '/api' + path
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header('Authorization', auth)
    r.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(r, timeout=15)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return e.code, json.loads(body)
        except:
            return e.code, {"error": body[:200]}

# Create categories
cats_raw = [
    ("Train Tour", "train-tour"),
    ("City Experiences", "city-experiences"),
    ("Custom Private Tours", "custom-private-tours"),
    ("Expert-led Journeys", "expert-led-journeys"),
    ("Small Group Departures", "small-group-departures"),
    ("GUDAO Ancient Hiking Trails", "gudao-hiking"),
]
cat_ids = {}
for name, slug in cats_raw:
    s, d = api('POST', '/categories', {"data": {"name": name, "slug": slug}})
    if s in (200, 201):
        cid = d['data'].get('id', d['data'].get('documentId', '?'))
        cat_ids[slug] = cid
        print(f"  CAT: {name} ({cid})")
    else:
        print(f"  CAT FAIL {s}: {name} - {str(d.get('error',{}))[:100]}")

# Create types
types_raw = [
    ("Adventure", "adventure"),
    ("Cultural", "cultural"),
    ("Culinary", "culinary"),
    ("Family", "family"),
]
type_ids = {}
for name, slug in types_raw:
    s, d = api('POST', '/types', {"data": {"name": name, "slug": slug}})
    if s in (200, 201):
        tid = d['data'].get('id', d['data'].get('documentId', '?'))
        type_ids[slug] = tid
        print(f"  TYPE: {name} ({tid})")
    else:
        print(f"  TYPE FAIL {s}: {name}")

# Create sample tours
tours = [
    {
        "title": "GUDAO Zhejiang: Hiking Through Tea Mountains of Songyang",
        "slug": "gudao-zhejiang-songyang",
        "excerpt": "Hike through Songyang's ancient tea mountains on this 5-day experience with WildChina. Trek terraced fields and discover hidden villages.",
        "description": "## Day 1: Arrival in Hangzhou\n\nArrive in Hangzhou and transfer to your hotel...\n\n## Day 2: Songyang Ancient Trail\n\nBegin your hike through the tea-scented mountains...",
        "duration_days": 5,
        "price": 2800,
        "currency": "USD",
        "start_city": "Lishui",
        "end_city": "Songyang",
        "availability": "January - June | October - December",
        "specific_dates": "Multiple departures available",
        "is_new": False,
        "is_waitlist": False,
        "rating": 4.8,
        "popularity": 95,
        "category": cat_ids.get("gudao-hiking"),
        "type": type_ids.get("adventure"),
    },
    {
        "title": "A National Geographic Trip to Guizhou",
        "slug": "natgeo-guizhou-dong-village",
        "excerpt": "Deep in the mountains of Guizhou, Huanggang Dong Village prepares for its most sacred festival. Immerse yourself in Dong culture.",
        "description": "## Journey into the Heart of Guizhou\n\nExperience the rich culture of the Dong people...",
        "duration_days": 4,
        "price": 1980,
        "currency": "USD",
        "start_city": "Guiyang",
        "end_city": "Guiyang",
        "availability": "March - November",
        "specific_dates": "Various dates available",
        "is_new": True,
        "is_waitlist": False,
        "rating": 4.9,
        "popularity": 88,
        "category": cat_ids.get("expert-led-journeys"),
        "type": type_ids.get("cultural"),
    },
    {
        "title": "Gastronomic Tour of China with Fuchsia Dunlop",
        "slug": "gastronomic-china-fuchsia-dunlop",
        "excerpt": "Ready your chopsticks for a China foodie adventure with award-winning author Fuchsia Dunlop. From Beijing to Shanghai through the lens of food.",
        "description": "## A Culinary Journey Across China\n\nJoin Fuchsia Dunlop on an unforgettable gastronomic adventure...",
        "duration_days": 12,
        "price": 9630,
        "currency": "USD",
        "start_city": "Beijing",
        "end_city": "Shanghai",
        "availability": "May 5th - May 16th, 2026",
        "specific_dates": "May 5th - May 16th, 2026",
        "is_new": False,
        "is_waitlist": True,
        "rating": 5.0,
        "popularity": 99,
        "category": cat_ids.get("expert-led-journeys"),
        "type": type_ids.get("culinary"),
    },
    {
        "title": "Allied Victory: Doolittle Raid & Battle of Shanghai",
        "slug": "doolittle-raid-shanghai-wwii",
        "excerpt": "Embark on a journey to the heart of the Doolittle Raid, a daring air attack that changed the course of WWII in the Pacific.",
        "description": "## WWII History Tour\n\nFollow the footsteps of the Doolittle Raiders...",
        "duration_days": 6,
        "price": 2900,
        "currency": "USD",
        "start_city": "Shanghai",
        "end_city": "Quzhou",
        "availability": "October 12th - 17th, 2026",
        "specific_dates": "October 12th - 17th, 2026",
        "is_new": True,
        "is_waitlist": False,
        "rating": 4.7,
        "popularity": 72,
        "category": cat_ids.get("city-experiences"),
        "type": type_ids.get("cultural"),
    },
    {
        "title": "Gastronomic Yunnan with Fuchsia Dunlop",
        "slug": "gastronomic-yunnan-dunlop",
        "excerpt": "Join food writer Fuchsia Dunlop on an epicurean odyssey through this far-flung region of China, from Kunming to Dali.",
        "description": "## Yunnan Food Adventure\n\nExplore the diverse culinary landscape of Yunnan...",
        "duration_days": 10,
        "price": 5980,
        "currency": "USD",
        "start_city": "Kunming",
        "end_city": "Dali",
        "availability": "September 11th - 20th, 2026",
        "specific_dates": "September 11th - 20th, 2026",
        "is_new": False,
        "is_waitlist": True,
        "rating": 4.9,
        "popularity": 85,
        "category": cat_ids.get("expert-led-journeys"),
        "type": type_ids.get("culinary"),
    },
    {
        "title": "Classic Beijing City Experience",
        "slug": "classic-beijing-experience",
        "excerpt": "Discover the imperial grandeur of Beijing - from the Forbidden City to the Great Wall, with expert local guides.",
        "description": "## Beijing Highlights\n\nExperience the best of China's capital...",
        "duration_days": 3,
        "price": 1200,
        "currency": "USD",
        "start_city": "Beijing",
        "end_city": "Beijing",
        "availability": "Available year-round",
        "specific_dates": "Daily departures",
        "is_new": False,
        "is_waitlist": False,
        "rating": 4.6,
        "popularity": 90,
        "category": cat_ids.get("city-experiences"),
        "type": type_ids.get("family"),
    },
]

print(f"\nCreating {len(tours)} tours...")
for tour in tours:
    # Build proper relation data for Strapi 5
    data = {"data": dict(tour)}
    # Convert relation IDs to proper Strapi format
    if data["data"]["category"]:
        data["data"]["category"] = {"connect": [data["data"]["category"]]}
    if data["data"]["type"]:
        data["data"]["type"] = {"connect": [data["data"]["type"]]}

    s, d = api('POST', '/tours', data)
    if s in (200, 201):
        tid = d['data'].get('id', d['data'].get('documentId', '?'))
        print(f"  TOUR: {tour['title'][:50]}... ({tid})")
    else:
        err = d.get('error', {}).get('message', str(d)[:150])
        print(f"  FAIL {s}: {tour['title'][:40]}... -> {err}")

print(f"\nDone! Visit http://localhost:1337/api/tours to verify")
