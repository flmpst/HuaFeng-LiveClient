import requests
import json
import typing
from enum import Enum

class MainProcessor(object):
    def __init__(self, baseURL:str, token: str) -> None:
        self.base_url = baseURL
        self.token = token

    def getLiveList(self) -> typing.Union[dict, bool]:  # Get live list
        response = requests.get(self.base_url + "api/v1/live/list")
        liveList = json.loads(response.content.decode('utf-8'))
        if liveList["code"] == 200:
            returnContent = liveList["data"]["list"]
        else:
            returnContent = False

        return returnContent
    
    def getLiveAuthorName(self, liveID):  # Get author name
        response = requests.get(self.base_url + f"api/v1/live/get?live_id={liveID}")
        liveInformation = json.loads(response.content.decode('utf-8'))
        if liveInformation["code"] == 200:
            returnContent = liveInformation["data"]["username"]
        else:
            returnContent = False

        return returnContent

    def getLiveSourece(self, liveID: int) -> typing.Union[str, bool]:  # Get live source url
        response = requests.get(self.base_url + f"api/v1/live/get?live_id={liveID}")
        liveInformation = json.loads(response.content.decode('utf-8'))
        if liveInformation["code"] == 200:
            returnContent = liveInformation["data"]["videoSource"]
        else:
            returnContent = False

        return returnContent
    
    def createLive(self, name: str, description:str, videoSource:str, sourceType: str) -> bool:
        data = {
            "token": self.token,
            "description": description,
            "name": name,
            "videoSource": videoSource,
            "videoSourceType": sourceType
        }

        response = requests.post(self.base_url + "api/v1/live/create", json=data)

        if response.status_code == 200:
            returnContent = True
        else:
            returnContent = False
        
        return returnContent
    
    def sendMessage(self, liveID: str, content: str) -> bool:
        data = {
            "token": self.token,
            "message": content
        }

        respone = requests.post(self.base_url + f"api/v1/chat/send?room_id={liveID}")

        if respone.status_code == 200:
            returnContent = True
        else:
            returnContent = False
        
        return returnContent