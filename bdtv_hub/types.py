from typing import TypedDict


class Config(TypedDict):
    # 服务器可被公开访问的地址
    server_public_address: str
    # 服务器端口
    server_port: int
    # 服务器名称
    server_nickname: str
    # 服务器 ID
    server_slug: str

class Player(TypedDict):
    nickname: str
    uuid: str


class Server(TypedDict):
    nickname: str
    slug: str
    address: str
    port: int
