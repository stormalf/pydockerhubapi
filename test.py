import os
from pydockerhubapi import dockerhubApi

iurl = "https://hub.docker.com"
ijson = ""
imethod="GET"
iapi = "/v2/access-tokens"
iuser= os.environ.get("DOCKERHUB_USER")
itoken = os.environ.get("DOCKERHUB_TOKEN")
message= dockerhubApi.rundockerhubApi(api=iapi, method=imethod, url=iurl, user=iuser, token=itoken, json=ijson )
print(message)