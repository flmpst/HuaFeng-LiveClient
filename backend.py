import aiohttp
import json
import typing

class MainProcessor(object):
    def __init__(self, baseURL: str, token: str, phpsessid: str) -> None:
        self.base_url = baseURL if baseURL.endswith('/') else baseURL + '/'
        self.token = token
        self.phpsessid = phpsessid

    async def getLiveList(self) -> typing.Union[dict, bool]:  # Get live list
        async with aiohttp.ClientSession(cookies={"PHPSESSID": self.phpsessid}) as session:
            async with session.get(self.base_url + "api/v1/live/list") as response:
                content = await response.read()
                liveList = json.loads(content.decode('utf-8-sig'))
                if liveList["code"] == 200:
                    return liveList["data"]["list"]
                else:
                    return False

    async def getLiveAuthorName(self, liveID):  # Get author name
        async with aiohttp.ClientSession(cookies={"PHPSESSID": self.phpsessid}) as session:
            async with session.get(self.base_url + f"api/v1/live/get?live_id={liveID}") as response:
                content = await response.read()
                liveInformation = json.loads(content.decode('utf-8-sig'))
                if liveInformation["code"] == 200:
                    return liveInformation["data"]["username"]
                else:
                    return False

    async def getLiveSource(self, liveID: int) -> typing.Union[str, bool]:  # Get live source url
        async with aiohttp.ClientSession(cookies={"PHPSESSID": self.phpsessid}) as session:
            async with session.get(self.base_url + f"api/v1/live/get?live_id={liveID}") as response:
                content = await response.read()
                liveInformation = json.loads(content.decode('utf-8-sig'))
                if liveInformation["code"] == 200:
                    return liveInformation["data"]["videoSource"]
                else:
                    return False

    async def createLive(self, name: str, description: str, videoSource: str, sourceType: str) -> bool:
        data = {
            "token": self.token,
            "description": description,
            "name": name,
            "videoSource": videoSource,
            "videoSourceType": sourceType.lower()
        }
        
        async with aiohttp.ClientSession(cookies={"PHPSESSID": self.phpsessid}) as session:
            async with session.post(self.base_url + "api/v1/live/create", data=data) as response:
                print(data)
                if await response.json()["code"] == 200:
                    return True
                else:
                    return False

    async def sendMessage(self, liveID: str, content: str) -> bool:
        data = {
            "token": self.token,
            "message": content
        }
        async with aiohttp.ClientSession(cookies={"PHPSESSID": self.phpsessid}) as session:
            async with session.post(self.base_url + f"api/v1/chat/send?room_id={liveID}", data=data) as response:
                content = await response.read()
                if response.status == 200:
                    return True
                else:
                    return False
                
    async def ziSha(self) -> bool:
        async with aiohttp.ClientSession(cookies={"PHPSESSID": self.phpsessid}) as session:
            async with session.get(self.base_url + "api/v1/refresh") as response:
                content = await response.json(encoding='utf-8-sig')
                print(content)