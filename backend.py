import aiohttp
import json
import typing
from uuid import uuid4
import webbrowser
import asyncio

class MainProcessor(object):
    def __init__(self, baseURL: str, token: str, phpsessid: str) -> None:
        if token == "" and phpsessid != "":
            self.token = asyncio.run(self.getToken(baseURL, phpsessid))
        else:
            self.token = token

        self.base_url = baseURL if baseURL.endswith('/') else baseURL + '/'
        self.phpsessid = phpsessid

    async def deleteLive(self, liveID: int):
        try:
            async with aiohttp.ClientSession(cookies={"PHPSESSID": self.phpsessid}) as session:
                async with session.get(self.base_url + f"api/v1/live/delet?liveId={liveID}") as response:
                    response_json = await response.json(encoding='utf-8-sig')
                    match response_json['code']:
                        case 200:
                            returnContent = "success"
                        case 403:
                            returnContent = "refuse"
                        case _:
                            returnContent = False
        except:
            returnContent = False
        finally:
            return returnContent

    async def getToken(self, base_url, phpsessid: str) -> str:
        async with aiohttp.ClientSession(cookies={"PHPSESSID": phpsessid}) as session:
            async with session.get(base_url + f"api/v1/user/get") as respone:
                responeJson = await respone.json(encoding='utf-8-sig')
                if responeJson["code"] == 200:
                    returnContent = responeJson["data"]["token"]
                else:
                    returnContent = False

                return returnContent

    async def getChatLog(self, liveID: int, limit: int, offset:float = 0):
        async with aiohttp.ClientSession(cookies={"PHPSESSID": self.phpsessid}) as session:
            async with session.get(self.base_url + f"api/v1/chat/get?room_id={liveID}&limit={limit}&offset={offset}") as response:
                await response.json(encoding='utf-8-sig')["data"]["message"]

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
            "videoSourceType": sourceType
        }

        async with aiohttp.ClientSession(cookies={"PHPSESSID": self.phpsessid}) as session:
            async with session.post(self.base_url + "api/v1/live/create", data=data) as response:
                responseJson = await response.json(encoding='utf-8-sig')
                if responseJson["code"] == 200:
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
                
    async def refreshToken(self) -> bool:
        async with aiohttp.ClientSession(cookies={"PHPSESSID": self.phpsessid}) as session:
            async with session.get(self.base_url + "api/v1/refresh") as response:
                content = await response.json(encoding='utf-8-sig')["data"][0]

class Auth(object):
    def __init__(self, base_url, callbackFunc):
        self.clientId = uuid4()
        self.base_url = base_url
        self.auth_url = base_url + f"?method=clientAuth&clientid={self.clientId}"
        self.callbackFunc = callbackFunc
        webbrowser.open(self.auth_url)
        asyncio.run(self.pollAuthStatus())

    async def pollAuthStatus(self):
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(self.base_url + f"api/v1/user/clientAuth?clientid={self.clientId}") as response:
                    content = await response.json(encoding='utf-8-sig')
                    if content["code"] == 200:
                        self.callbackFunc(content["data"]["token"])
                        break
                await asyncio.sleep(1)
