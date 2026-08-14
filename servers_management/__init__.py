import threading

import mcdreforged as mcdr

from online_player_api import get_player_list


class CenterConnector:
    INTERVAL = 5  # 秒

    def __init__(self, server: mcdr.PluginServerInterface):
        self.server = server

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
        self.server.logger.info(f"Instantly Heartbeat for {player}")

    def heartbeat(self):
        # wait 返回 True 说明被 set 了(要退出),返回 False 说明是超时(该干活了)
        while not self.heartbeat_stop_event.wait(self.INTERVAL):
            try:
                self.server.logger.info(f"Heartbeat for {', '.join(get_player_list())}")
            except Exception:
                self.server.logger.exception("定时任务执行出错")

    def clean_up(self):
        self.heartbeat_stop_event.set()
        self.heartbeat_worker.join(timeout=5)


def on_load(server: mcdr.PluginServerInterface, old):
    CenterConnector(server)
