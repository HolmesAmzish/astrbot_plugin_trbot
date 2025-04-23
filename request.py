import requests
import json

url = "http://localhost:7878/v2/players/list"
token = "20230612"
params = {"token": token}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()  # 检查请求是否成功

    data = response.json()

    if data["status"] == "200" and "players" in data:
        online_players = [player for player in data["players"] if player.get("active")]
        online_count = len(online_players)
        print(f"在线玩家数量: {online_count}")
    else:
        print("无法获取在线玩家列表或响应格式不正确。")
        print("响应内容:", data)

except requests.exceptions.RequestException as e:
    print(f"请求发生错误: {e}")
except json.JSONDecodeError:
    print("无法解析 JSON 响应。")
    print("响应内容:", response.text)