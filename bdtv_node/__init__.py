import threading

import mcdreforged as mcdr

from . import state
from .commands import register_command
from .config import load_or_init_config
from .heart import start_heartbeat
from .utils import handle_player_join, pure_players


def on_player_joined(server: mcdr.PluginServerInterface, player: str, info: mcdr.Info):
    real_player = pure_players([player])

    # 非 0 则为单一玩家名称存在于白名单中
    if len(real_player) != 0:
        handle_player_join(server, real_player[0])  # type: ignore[operator]


def on_load(server: mcdr.PluginServerInterface, prev_module):
    logger = server.logger

    config = load_or_init_config(server)
    logger.info("配置文件已加载")

    state.server_data = {
        "address": config["mc_public_address"],
        "port": config["mc_port"],
        "nickname": config["server_nickname"],
        "slug": config["server_slug"],
    }
    state.hub_url_base = config["bdtv_hub_base"]

    register_command(server)

    state.stop_heartbeat = threading.Event()

    state.heartbeat_thread = start_heartbeat(server)  # type: ignore[operator]


def on_unload(server: mcdr.PluginServerInterface):
    logger = server.logger

    # 向心跳线程发送终止信号
    state.stop_heartbeat.set()
    # 等待心跳线程终止
    logger.info("等待心跳线程终止")
    state.heartbeat_thread.join()
