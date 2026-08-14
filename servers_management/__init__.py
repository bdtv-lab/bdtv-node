import mcdreforged as mcdr

from online_player_api import get_player_list


class CenterConnector:
    def __init__(self):
        pass


def on_player_joined(server: mcdr.PluginServerInterface, player: str, info: mcdr.Info):
    server.say(
        f"玩家 {player} 加入了服务器！现在在线的有 {', '.join(get_player_list())}"
    )


def on_load(server: mcdr.PluginServerInterface, old):
    pass
