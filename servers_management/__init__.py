import os
import threading

import mcdreforged as mcdr

from online_player_api import get_player_list

from .action import Action
from .config import load_or_init_config
from .utils import check_whitelist


class CenterConnector:
    INTERVAL = 5  # 秒

    def __init__(self, server: mcdr.PluginServerInterface):
        self.server = server

        config = load_or_init_config(
            os.path.join(server.get_data_folder(), "config.json")
        )

        self.action = Action(config["server"], config["port"])
        self.id = config["id"]
        self.nickname = config["nickname"]

        self.heartbeat_stop_event = threading.Event()
        self.heartbeat_worker: threading.Thread = threading.Thread(
            target=self.heartbeat, args=(), name="MyPluginTimer", daemon=True
        )

        self.heartbeat_stop_event.clear()
        self.heartbeat_worker.start()

        self.server.register_event_listener("mcdr.plugin_unloaded", self.clean_up)
        self.server.register_event_listener("mcdr.player_joined", self.on_player_joined)

    def on_player_joined(
        self, server: mcdr.PluginServerInterface, player: str, info: mcdr.Info
    ):
        if check_whitelist(self.server, player):
            self.server.logger.info(f"Instantly Heartbeat for {player}")
            self.action.heartbeat(player)

    def heartbeat(self):
        # wait 返回 True 说明被 set 了(要退出),返回 False 说明是超时(该干活了)
        while not self.heartbeat_stop_event.wait(self.INTERVAL):
            try:
                player_list = get_player_list()
                if player_list:
                    for player in player_list:
                        if check_whitelist(self.server, player):
                            # self.server.logger.info(f"Heartbeat for {player}")
                            self.action.heartbeat(player)

            except Exception:
                self.server.logger.exception("定时任务执行出错")

    def clean_up(self, server: mcdr.PluginServerInterface):
        self.heartbeat_stop_event.set()
        self.heartbeat_worker.join(timeout=5)
        # kill
        self.action.ws.close()


def on_load(server: mcdr.PluginServerInterface, old):
    CenterConnector(server)
