import threading

import mcdreforged as mcdr

from . import state
from .config import load_or_init_config
from .heart import start_heartbeat


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

    state.stop_heartbeat = threading.Event()

    state.heartbeat_thread = start_heartbeat(server)  # type: ignore[operator]


def on_unload(server: mcdr.PluginServerInterface):
    logger = server.logger

    # 向心跳线程发送终止信号
    state.stop_heartbeat.set()
    # 等待心跳线程终止
    logger.info("等待心跳线程终止")
    state.heartbeat_thread.join()
