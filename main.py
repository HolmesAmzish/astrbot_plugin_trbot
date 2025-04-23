from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import requests
import json

@register("TShock Bot", "Cacciatore", "A TShock Bot to control server", "1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    @filter.command("playing")
    async def query_online_players(self, event: AstrMessageEvent):
        """Query the number of online players"""
        
        online_count = None

        # Get the result of online players
        url = "http://localhost:7878/v2/players/list"
        token = "astrbot"
        params = {"token": token}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if data["status"] == "200" and "players" in data:
                online_players_data = [player for player in data["players"]]
                #online_players_data = [player for player in data["players"] if player.get("active")]
                online_count = len(online_players_data)
                online_players = [player.get("nickname") for player in online_players_data]
            else:
                print("Cannot get online player list or response format is incorrect.")
                print("Response", data)

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except json.JSONDecodeError:
            print("Cannot parse JSON response.")
            print("Response:", response.text)


        # Contruct the result
        if online_count:
            result = f"服务器当前在线玩家 {online_count} 名"
            if (len(online_players) > 0):
                result += "\n" + "玩家列表：" + ", ".join(online_players)
        else:
            result = "当前服务器未开启或设置错误"

        yield event.plain_result(result)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""