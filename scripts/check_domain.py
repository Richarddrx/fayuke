import http.client, urllib.parse, hmac, hashlib, base64, datetime, json, os

def check_domain(domain_name, access_key_id, access_key_secret):
    params = {
        'Action': 'CheckDomain',
        'DomainName': domain_name,
        'Format': 'json',
        'Version': '2018-01-29',
        'AccessKeyId': access_key_id,
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureVersion': '1.0',
        'SignatureNonce': str(datetime.datetime.now().timestamp()),
        'Timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    }
    sorted_keys = sorted(params.keys())
    canonicalized = '&'.join([f'{urllib.parse.quote(k, safe="")}={urllib.parse.quote(params[k], safe="")}' for k in sorted_keys])
    string_to_sign = f'GET&%2F&{urllib.parse.quote(canonicalized, safe="")}'
    signature = base64.b64encode(hmac.new(f'{access_key_secret}&'.encode(), string_to_sign.encode(), hashlib.sha1).digest()).decode()
    params['Signature'] = signature
    query_string = '&'.join([f'{k}={urllib.parse.quote(v, safe="")}' for k, v in params.items()])
    conn = http.client.HTTPSConnection('domain.aliyuncs.com', timeout=10)
    conn.request('GET', f'/?{query_string}')
    resp = conn.getresponse()
    data = json.loads(resp.read().decode())
    conn.close()
    return data

key_id = os.environ.get('ALIYUN_KEY_ID')
key_secret = os.environ.get('ALIYUN_KEY_SECRET')

domains = ['europe58.com', 'faguo58.com', 'ouzhou58.com', 'huaren58.com', 'fayuke.fr', 'fayuke.com', 'paris58.com', 'faguo58.fr']
for d in domains:
    r = check_domain(d, key_id, key_secret)
    avail = r.get('Avail')
    if avail == 1:
        print(f'  ✅ {d} — Disponible')
    elif avail == 0:
        print(f'  ❌ {d} — Déjà enregistré')
    else:
        print(f'  ❓ {d} — {r}')
