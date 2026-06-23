import json, urllib.request

with open('.login-resp.json') as f:
    token = json.load(f)['data']['token']
auth = 'Bearer ' + token

def admin_post(path, body):
    url = 'http://localhost:1337/admin' + path
    data = json.dumps(body).encode()
    r = urllib.request.Request(url, data=data, method='POST')
    r.add_header('Authorization', auth)
    r.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(r, timeout=15)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try: return e.code, json.loads(body)
        except: return e.code, {'error': body[:200]}

# Create categories
cats = [
    ('Train Tour', 'train-tour'),
    ('City Experiences', 'city-experiences'),
    ('Custom Private Tours', 'custom-private-tours'),
    ('Expert-led Journeys', 'expert-led-journeys'),
    ('Small Group Departures', 'small-group-departures'),
    ('GUDAO Hiking', 'gudao-hiking'),
]

ct = 'api::category.category'
for name, slug in cats:
    s, d = admin_post(
        f'/content-manager/collection-types/{ct}',
        {'name': name, 'slug': slug}
    )
    print(f'CAT {name}: {s}')

# Create types
types = [
    ('Adventure', 'adventure'),
    ('Cultural', 'cultural'),
    ('Culinary', 'culinary'),
    ('Family', 'family'),
]

ct2 = 'api::type.type'
for name, slug in types:
    s, d = admin_post(
        f'/content-manager/collection-types/{ct2}',
        {'name': name, 'slug': slug}
    )
    print(f'TYPE {name}: {s}')

print('Done')
