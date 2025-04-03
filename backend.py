import aiohttp
import json
import typing
import webbrowser
import asyncio
import platform
import uuid
import flask
import werkzeug
import threading

class MainProcessor(object):
    def __init__(self, baseURL: str, token: str) -> None:
        self.token = token
        self.base_url = baseURL if baseURL.endswith('/') else baseURL + '/'

    async def deleteLive(self, liveID: int):
        data = {"token": self.token}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url + f"api/v1/live/delet?liveId={liveID}", data=data) as response:
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

    async def getChatLog(self, liveID: int, limit: int, offset: float = 0):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + f"api/v1/chat/get?room_id={liveID}&limit={limit}&offset={offset}") as response:
                await response.json(encoding='utf-8-sig')["data"]["message"]

    async def getLiveList(self) -> typing.Union[dict, bool]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + "api/v1/live/list") as response:
                content = await response.read()
                liveList = json.loads(content.decode('utf-8-sig'))
                if liveList["code"] == 200:
                    return liveList["data"]["list"]
                else:
                    return False

    async def getLiveAuthorName(self, liveID):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + f"api/v1/live/get?live_id={liveID}") as response:
                content = await response.read()
                liveInformation = json.loads(content.decode('utf-8-sig'))
                if liveInformation["code"] == 200:
                    return liveInformation["data"]["username"]
                else:
                    return False

    async def getLiveSource(self, liveID: int) -> typing.Union[str, bool]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + f"api/v1/live/get?live_id={liveID}") as response:
                content = await response.read()
                liveInformation = json.loads(content.decode('utf-8-sig'))
                if liveInformation["code"] == 200:
                    return liveInformation["data"]["videoSource"]
                else:
                    return False

    async def createLive(self, name: str, description: str, videoSource: str, sourceType: str, pictureUrl: str) -> bool:
        data = {
            "token": self.token,
            "description": description,
            "name": name,
            "videoSource": videoSource,
            "videoSourceType": sourceType,
            # "pic": pictureUrl
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url + "api/v1/live/create", data=data) as response:
                responseJson = await response.json(encoding='utf-8-sig')
                if responseJson["code"] == 200:
                    return True
                else:
                    return False

    async def sendMessage(self, liveID: str, content: str) -> bool:
        data = {
            "token": self.token,
            "message": content,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url + f"api/v1/chat/send?room_id={liveID}", data=data) as response:
                if response.status == 200:
                    return True
                else:
                    return False

class Auth(object):
    def __init__(self, base_url, callbackFunc):
        self.clientId = f"{platform.system()}-{("%012X" % uuid.getnode()).lower()}-{str(uuid.uuid4()).replace('-', '')[:5]}"
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

class OAuth(object):
    def __init__(self, base_url, callbackFunc):
        self.clientId = uuid4()
        self.base_url = base_url
        self.auth_url = base_url + f"verify/client?clientid={self.clientId}&callback=http://localhost:14193"
        self.callbackFunc = callbackFunc

        webbrowser.open(self.auth_url)

        try:
            oauthThread = threading.Thread(target=self.server)
            oauthThread.start()
        except:
            ...

    def server(self):
        oAuthCallback = flask.Flask(__name__)

        @oAuthCallback.route('/')
        def _():
            self.callbackFunc(flask.request.args.get("token"))
            oserver.shutdown()

        oserver = werkzeug.serving.make_server('localhost', 14193, oAuthCallback)
        oserver.serve_forever()