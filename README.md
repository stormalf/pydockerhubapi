# pydockerhubapi

python3 module to call dockerhub api in command line or inside a module.

# pydockerhub.py

pydockerhubapi.py --help

    usage: pydockerhubapi.py [-h] [-V] [-U USER] [-t TOKEN] [-u URL] [-a API] [-m METHOD] [-J JSONFILE] [-g]

    pydockerhubapi is a python3 program that call dockerhub apis in command line or imported as a module

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of pydockerhubapi
    -U USER, --user USER  dockerhub user
    -t TOKEN, --token TOKEN
                            dockerhub token
    -u URL, --url URL     dockerhub url
    -a API, --api API     dockerhub api should start by a slash
    -m METHOD, --method METHOD
                            should contain one of the method to use : ['DELETE', 'GET', 'POST', 'PUT', 'PATCH']
    -J JSONFILE, --jsonfile JSONFILE
                            json file needed for POST method
    -g, --generatetoken   generate token required DOCKERHUB_USER and DOCKERHUB_PASSWORD

Examples :
pydockerhubapi.py -V

    pydockerhubapi version : 1.0.0

Generating an access token. To create a new token: required DOCKERHUB_USER and DOCKERHUB_PASSWORD environment variables

    pydockerhubapi.py -g
    {'token': 'ey...mw'}

List of tokens : without any parameters returns the result of "/v2/access-tokens"

GET /v2/access-tokens: return list of tokens

    python3 pydockerhubapi.py
    {'count': 1, 'next': None, 'previous': None, 'active_count': 1, 'results': [{'uuid': '9z9zzz9zz-z999-9999-9z9z-9z999zz9zz99', \
    'client_id': 'HUB', 'creator_ip': '255.255.255.255', 'creator_ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.47', \
    'created_at': '2022-04-09T20:22:02.901518Z', 'last_used': None, 'generated_by': 'manual', 'is_active': True, \
    'token': '', 'token_label': 'your_label', 'scopes': ['repo:admin']}]}

PATCH /v2/access-tokens/{uuid}:

    python3 pydockerhubapi.py -m PATCH -a /v2/access-tokens/9z9zzz9zz-z999-9999-9z9z-9z999zz9zz99 -J patch_test.json
    {'uuid': '9z9zzz9zz-z999-9999-9z9z-9z999zz9zz99', 'client_id': 'HUB', 'creator_ip': '255.255.255.255', \
    'creator_ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.47', 'created_at': '2022-04-09T20:22:02.901518Z', \
    'last_used': None, 'generated_by': 'manual', 'is_active': True, 'token': '', 'token_label': 'My token', \
    'scopes': ['repo:admin']}

POST /v2/access-tokens: create a new personal access token

    python3 pydockerhubapi.py -m POST -a /v2/access-tokens -J token_new.json
    {'errinfo': None, 'message': 'not allowed to create a scoped personal access token with your current plan'}

DELETE /v2/access-tokens/{uuid}: delete a personal access token

    python3 pydockerhubapi.py -m DELETE -a /v2/access-tokens/9z9zzz9zz-z999-9999-9z9z-9z999zz9zz99
    example if token doesn't exist :
    {'fields': {'column': '', 'constraint': '', 'data_type_name': '', 'detail': '', 'error_class': 'data_exception', \
    'error_code': 'invalid_text_representation', 'severity': 'ERROR', 'table': '', 'user_uuid': \
    'zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzzz', 'username': 'greatuser', 'uuid': '9z9zzz9zz-z999-9999-9z9z-9z999zz9zz99'}, \
    'file': '/go/src/github.com/docker/saas-mega/lib/go-pg/error.go', 'func': \
    'github.com/docker/saas-mega/lib/go-pg.Error', 'line': 33, 'text': 'GetApiToken query error'}

# release notes

pydockerhubapi.py

1.0.0 initial version
