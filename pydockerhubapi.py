#!/usr/bin/python3
# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet
import requests
from json import loads as jsonload
from json import dumps as jsondumps
import argparse
import os


'''
pydockerhubapi.py is to be used by other python modules to automate dockerhub api usage.
it could be called in command line.
More information about all APIs : https://docs.docker.com/docker-hub/api/latest/

Examples : 
List of tokens :  without any parameters returns the result of "/v2/access-tokens"

GET /v2/access-tokens: return list of tokens
    python3 pydockerhubapi.py
    {'count': 1, 'next': None, 'previous': None, 'active_count': 1, 'results': [{'uuid': '9z9zzz9zz-z999-9999-9z9z-9z999zz9zz99', \
        'client_id': 'HUB', 'creator_ip': '255.255.255.255', 'creator_ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.47', \
                'created_at': '2022-04-09T20:22:02.901518Z', 'last_used': None, 'generated_by': 'manual', 'is_active': True, \
                    'token': '', 'token_label': 'your_label', 'scopes': ['repo:admin']}]}


To create a new token: required DOCKERHUB_USER and DOCKERHUB_PASSWORD environment variables
    python3 pydockerhubapi.py -g 

define DOCKERHUB_TOKEN environment variable to use the generated token

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


'''

__version__ = "1.0.0"

ALLOWED_METHODS = ["DELETE", "GET", "POST", "PUT", "PATCH"]
URL = "https://hub.docker.com"
NO_CONTENT = 204
def pydockerhubApiVersion():
    return f"pydockerhubapi version : {__version__}"


class dockerhubApi():
    def __init__(self, api, method, url, user, token, jsonfile):
        self.api = api
        self.method = method
        self.json = jsonfile
        self.url = url
        self.user = user
        self.token = dockerhubApi.crypted(token)

    def __repr__(self):
        return (f"dockerhubApi api: {self.api}, method: {self.method}, url: {self.url}")

    #return the encrypted password/token
    @classmethod
    def crypted(cls, token):
        cls.privkey = Fernet.generate_key()        
        cipher_suite = Fernet(cls.privkey)
        ciphered_text = cipher_suite.encrypt(token.encode())
        cls.token = ciphered_text
        return cls.token

    #return the decrypted password/token
    @classmethod
    def decrypted(cls, token):
        cls.token = token
        cipher_suite = Fernet(cls.privkey)
        decrypted_text = cipher_suite.decrypt(cls.token)
        decrypted_text = decrypted_text.decode()
        return decrypted_text

    #execute the dockerhub api using a temp instance
    @staticmethod
    def rundockerhubApi(api, method, url, user, token, json):
        if token == None:
            response = jsonload('{"message": "Error : token missing!"}')
            return response 
        tempdockerhub = dockerhubApi(api, method, url, user, token, json)
        response = tempdockerhub.dockerhubAuthentication()
        tempdockerhub = None
        return response       

    @staticmethod
    def getDockerHubToken(url, user, password):
        apiurl = url + "/v2/users/login"
        header = {}
        header['Accept'] = 'application/json'
        header['Content-Type'] = 'application/json'   
        data = jsondumps({"username": user, "password": password})
        response = requests.post(apiurl, data=data, headers=header)
        try:
            response = response.json()
        except requests.exceptions.RequestException as e:  
            raise SystemExit(e)   
        return response

    #call private function
    def dockerhubAuthentication(self):
        response = self.__dockerhubTokenAuth()
        return response

    #internal function that formats the url and calls the dockerhub apis
    def __dockerhubTokenAuth(self):
        apiurl = self.url + self.api  
        header = {}
        header['Content-Type'] = 'application/json'
        header['Authorization'] = "Bearer " + dockerhubApi.decrypted(self.token)  
        response = self.__dockerhubDispatch(apiurl, header)
        return response

    #internal function that calls the requests
    def __dockerhubDispatch(self, apiurl, header):
        response = "{}"        
        try:
            if self.method == "POST":
                contents = open(self.json, 'rb')
                response = requests.post(apiurl, data=contents,headers=header)
                contents.close()
            elif self.method == "GET":
                response = requests.get(apiurl, headers=header)
            elif self.method == "PUT":
                if self.json == '':
                    response = requests.put(apiurl, headers=header)
                else:
                    contents = open(self.json, 'rb')
                    response = requests.put(apiurl, data=contents, headers=header)
                    contents.close()
            elif self.method == "DELETE":
                response = requests.delete(apiurl, headers=header)  
            elif self.method == "PATCH":
                if self.json == '':
                    response = requests.patch(apiurl, headers=header)
                else:
                    contents = open(self.json, 'rb')
                    response = requests.patch(apiurl, data=contents, headers=header)
                    contents.close()
        except requests.exceptions.RequestException as e:  
            raise SystemExit(e)   
        if response.status_code == NO_CONTENT:
            response = "{}"
        elif response.status_code != 200:
            response = jsonload('{"message": "Error : ' + str(response.status_code) + ' ' + response.reason + '"}')
        else:            
            response = response.json()
        return response

def pydockerhubapi(args):
    message = ''
    if args.user == '':
        user = os.environ.get("DOCKERHUB_USER")
    else:
        user = args.user  
    if args.token == '':
        itoken = os.environ.get("DOCKERHUB_TOKEN")
    else:
        itoken = args.token               
    if args.api == '':
        api=f"/v2/access-tokens"
    else:
        api=args.api    
    if args.url == '':
        iurl = URL
    else:
        iurl = args.url        
    method = args.method     
    if "POST" in method and args.jsonfile == "" and args.generatetoken == False:
        message = {"error": "Json file required with method POST!"}
        print(message)
        return message
    json = args.jsonfile  
    if args.generatetoken:
        ipassword = os.environ.get("DOCKERHUB_PASSWORD")
        if ipassword == '':
            message = {"error" : "DOCKERHUB_PASSWORD environment variable required!"}
            print(message)
            return message 
        message = dockerhubApi.getDockerHubToken(iurl, user, ipassword)      
    else:
        message= dockerhubApi.rundockerhubApi(api=api, method=method, url=iurl, user=user, token=itoken, json=json ) 
    return message


if __name__== "__main__":
    helpmethod = f"should contain one of the method to use : {str(ALLOWED_METHODS)}"
    parser = argparse.ArgumentParser(description="pydockerhubapi is a python3 program that call dockerhub apis in command line or imported as a module")
    parser.add_argument('-V', '--version', help='Display the version of pydockerhubapi', action='version', version=pydockerhubApiVersion())
    parser.add_argument('-U', '--user', help='dockerhub user', default='', required=False)    
    parser.add_argument('-t', '--token', help='dockerhub token', default='', required=False)    
    parser.add_argument('-u', '--url', help='dockerhub url', default='', required=False)    
    parser.add_argument('-a', '--api', help='dockerhub api should start by a slash', default='', required=False)    
    parser.add_argument('-m', '--method', help = helpmethod, default="GET", required=False)   
    parser.add_argument('-J', '--jsonfile', help='json file needed for POST method', default='', required=False)
    parser.add_argument('-g', '--generatetoken', help='generate token required DOCKERHUB_USER and DOCKERHUB_PASSWORD', action="store_true" , required=False)
    args = parser.parse_args()
    message = pydockerhubapi(args)
    print(message)