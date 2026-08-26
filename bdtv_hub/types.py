from typing import TypedDict


class Config(TypedDict):
    # MC 服务器可被公开访问的地址
    mc_public_address: str
    # MC 服务器端口
    mc_port: int
    # 服务器名称
    server_nickname: str
    # 服务器 ID
    server_slug: str
    # BDTV hub 请求地址
    bdtv_hub_base: str


class Player(TypedDict):
    nickname: str
    uuid: str


class Server(TypedDict):
    nickname: str
    slug: str
    address: str
    port: int
