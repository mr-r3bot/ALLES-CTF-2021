## Amazing Crypto WAF

### Architecture

- All the requests are followed this:

Request -> Crypto WAF -(proxy through)-> App/back-end

Back-end: Interact with DB to CRUD notes and Create/Authen user
Crypto WAF: Check params, encrypt params and proxy requests


### Objective

Goal: Flag user

```python
pw = uuid.uuid4().hex

flag = open('flag', 'rb').read()

  

logger.info(f'flagger password: {pw}')

s = requests.Session()

r = s.post(f'http://127.0.0.1:1024/registerlogin',

data={'username': 'flagger','password':pw}, allow_redirects=False)

  

s.post(f'http://127.0.0.1:1024/add_note',

data={'body': flag, 'title':'flag'}, allow_redirects=False)
```

------------------
### Code analysis

Back-end API endpoints:
```javascript
/
/logout
/notes
/delete_note
/add_note
/registerlogin
```


- First, request will go to: `waf_param` function for filtering

```python
def waf_param(param):
	MALICIOUS = ['select', 'union', 'alert', 'script', 'sleep', '"', '\'', '<']
	for key in param:
	val = param.get(key, '')
	while val != unquote(val):
	val = unquote(val)
for evil in MALICIOUS:
	if evil.lower() in val.lower():
		raise Exception('hacker detected')
```

If `waf_param` check passed -> Continue 
Else -> return `error`


- Our first injection point

`/notes`

```python
notes = query_db(f'select * from notes where user = ? order by timestamp {order}', [g.user['uuid']])
```

`order` parameters was placed into the query without any sanitization => Blind SQL Injection

So our payload should look like this:
```
http://localhost:5000/notes?order=xxx
```


How the GET request is proxied to back-end ?

```python
query = request.query_string.decode()
if request.method=='GET':
	proxy_request = requests.get(f'{BACKEND_URL}{path}?{query}',
		headers=headers,allow_redirects=False)
```


PoC:
```text
GET /notes?order=asc%2C%20%28CASE%20WHEN%201%3D1%20THEN%20timestamp%20ELSE%20uuid%20END%20%29
```

Bypass WAF payload:
```text
GET /notes%3Forder=asc,(CASE%20WHEN%20(select%201)%20THEN%20timestamp%20ELSE%20uuid%20END%20)---
```

### Exploit

#### 1. Leak flag body
Now, we will have a Conditional base SQLi, we can use that to leak information of flag body

Before the `waf` send data to back-end, it encrypt all data

```python
elif request.method=='POST':
	headers['Content-type'] = request.content_type
	proxy_request = requests.post(f'{BACKEND_URL}{path}?{query}',
	data=encrypt_params(request.form),headers=headers,allow_redirects=False)
```

So the flag information that we leaked will be encrypted, and the algorithm is AES and well-implemented, we cannot attack the crypto

#### 2. Decrypt the encrypted flag body

```python
return f'ENCRYPT:{b64}'
```

The flag we get will have this format `"ENCRYPT:<base64_encoding>"`

```python
def encrypt_params(param):

# We don't want to encrypt identifiers.

# This is a default set of typical ID values.

# In the future should be configurable per customer.

IGNORE = ['uuid', 'id', 'pk', 'username', 'password']

encrypted_param = {}

for key in param:

val = param.get(key,'')

if key in IGNORE:

encrypted_param[key] = val

else:

encrypted_param[key] = encrypt(val)

return encrypted_param
```

The application won't encrypt the key in IGNORE list
`IGNORE = ['uuid', 'id', 'pk', 'username', 'password']`

That's mean, if we register a user with username is the ENCRYPTED flag, when the WAF decrypt it again, we will get the clear-text

`response_data = decrypt_data(proxy_request.content)`

Flag: `ALLES!{American_scientists_said,_dont_do_WAFs!}`