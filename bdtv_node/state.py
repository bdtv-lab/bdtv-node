import threading

from mcdreforged import FunctionThread

from .types import Server

# BDTV hub 请求地址
hub_url_base: str
# 服务器数据
server_data: Server
# 是否需要终止心跳
stop_heartbeat: threading.Event
heartbeat_thread: FunctionThread
