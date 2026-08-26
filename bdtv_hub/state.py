import threading

from mcdreforged import FunctionThread

from .types import Server

server_data: Server
# 是否需要终止心跳
stop_heartbeat: threading.Event
heartbeat_thread: FunctionThread
