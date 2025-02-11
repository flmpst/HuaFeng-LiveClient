import aiohttp
import asyncio
import json
import typing

class MainProcessor(object):
    def __init__(self, baseURL: str) -> None:
        self.base_url = baseURL

    async def _getLiveList(self) -> typing.Union[dict, bool]:  # 获取直播列表
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + "/live/list") as response:
                liveList = json.loads(await response.text(encoding='utf-8-sig'))
                if liveList["code"] == 200:
                    returnContent = liveList["data"]["list"]
                else:
                    returnContent = False

        return returnContent

    def getLiveList(self) -> typing.Union[dict, bool]:  # 获取直播列表
        return asyncio.run(self._getLiveList())
        
    async def _getLiveSource(self, liveID: int) -> typing.Union[str, bool]:  # 获取直播源URL
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + f"/live/get?live_id={liveID}") as response:
                liveInformation = json.loads(await response.text(encoding='utf-8-sig'))
                if liveInformation["code"] == 200:
                    returnContent = liveInformation["data"]["videoSource"]
                else:
                    returnContent = False

        return returnContent

    def getLiveSource(self, liveID: int) -> typing.Union[str, bool]:  # 获取直播源URL
        return asyncio.run(self._getLiveSource(liveID))