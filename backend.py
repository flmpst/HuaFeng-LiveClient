import requests
import json
import typing

class MainProcessor(object):
    def __init__(self, baseURL:str) -> None:
        self.base_url = baseURL

    def getLiveList(self) -> typing.Union[dict, bool]:  # Get live list
        """
        返回示例
        [
      {
        "id": 1,
        "name": "河南卫视",
        "pic": "",
        "status": "on",
        "authr": "ushio_noa_@outlook.com",
        "peoples": null,
        "description": "懒得写"
      },
      {
        "id": 2,
        "name": "CGTV",
        "pic": "https://image.lolimi.cn/2025/01/29/679a3baae8f46.jpg",
        "status": "on",
        "authr": "小枫_QWQ",
        "peoples": null,
        "description": "中国国际电视台"
      },
      {
        "id": 4,
        "name": "tzdt打bjd",
        "pic": "",
        "status": "on",
        "authr": "2802247990@qq.com",
        "peoples": null,
        "description": "主板打布吉岛，拼尽全力无法战胜"
      },
      {
        "id": 5,
        "name": "“蛇来运转 万巳大吉”2025河南春晚",
        "pic": "https://media2.hndt.com/data_02/1/1/2025/01/16/fdfcc010175b10ae75b313e958b3d93e.jpg",
        "status": "on",
        "authr": "3859836281@qq.com",
        "peoples": null,
        "description": "回看：“蛇来运转 万巳大吉”2025河南春晚"
      },
      {
        "id": 6,
        "name": "2025中国杂技大联欢",
        "pic": "https://media2.hndt.com/data_02/1/1/2025/01/29/e66296e87ddce6715f3c0af59a4f8e6d_1500.jpg",
        "status": "on",
        "authr": "3859836281@qq.com",
        "peoples": null,
        "description": "河南卫视《2025中国杂技大联欢》"
      },
      {
        "id": 7,
        "name": "1",
        "pic": "",
        "status": null,
        "authr": "小枫是我老婆",
        "peoples": null,
        "description": "1"
      },
      {
        "id": 8,
        "name": "IPTV",
        "pic": "",
        "status": "on",
        "authr": "小枫是我老婆",
        "peoples": null,
        "description": "IPTV"
      },
      {
        "id": 9,
        "name": "《2025中央广播电视总台春节联欢晚会》 20250129 1/4（字幕版）",
        "pic": "https://p4.img.cctvpic.com/photoAlbum/page/performance/img/2021/9/28/1632795780652_242.jpg",
        "status": "on",
        "authr": "小枫_QWQ",
        "peoples": null,
        "description": "《2025中央广播电视总台春节联欢晚会》 20250129 1/4（字幕版）"
      },
      {
        "id": 10,
        "name": "测试",
        "pic": "",
        "status": "on",
        "authr": null,
        "peoples": null,
        "description": "111"
      }
    ]
    """
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