import mcdreforged as mcdr
import requests
from mcdreforged.api.decorator import new_thread

from online_player_api import get_player_list
from whitelist_api import get_whitelist

from . import state
from .types import Player


@new_thread("Heartbeat")
def start_heartbeat(server: mcdr.PluginServerInterface, delay: float = 5.0):
    logger = server.logger

    while not state.stop_heartbeat.is_set():
        # 获取在线玩家列表
        players = get_player_list()
        # 获取白名单
        whitelist = get_whitelist()

        # 剔除白名单内不在线的玩家
        # 限定为白名单是因为不在白名单里的通常是假人
        # 顺便构造为请求用的结构
        # TODO: 如果玩家改名，白名单不会及时更新，那么玩家就无法被判定
        online_real_player: list[Player] = [
            {"nickname": player.name, "uuid": player.uuid}
            for player in whitelist
            if player.name in players
        ]

        json_data = {
            "players": online_real_player,
            "server": state.server_data,
        }

        try:
            requests.post(f"{state.hub_url_base}/beat", json=json_data, timeout=(3, 3))
        except requests.RequestException as _:
            pass

        state.stop_heartbeat.wait(delay)
    logger.info("Bye!")
