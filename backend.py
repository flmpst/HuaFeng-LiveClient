import requests
import json
import typing

class MainProcessor(object):
    def __init__(self, baseURL:str) -> None:
        self.base_url = baseURL

    def getLiveList(self) -> typing.Union[dict, bool]:  # Get live list
        response = requests.get(self.base_url + "/live/list")
        liveList = json.loads(response.content.decode('utf-8-sig'))
        if liveList["code"] == 200:
            returnContent = liveList["data"]["list"]
        else:
            returnContent = False

        return returnContent
        
    def getLiveSourece(self, liveID: int) -> typing.Union[str, bool]:  # Get live source url
        response = requests.get(self.base_url + f"/live/get?live_id={liveID}")
        liveInformation = json.loads(response.content.decode('utf-8-sig'))
        if liveInformation["code"] == 200:
            returnContent = liveInformation["data"]["videoSource"]
        else:
            returnContent = False

        return returnContent