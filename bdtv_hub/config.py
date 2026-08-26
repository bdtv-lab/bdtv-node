import json
import os

import mcdreforged as mcdr

from .types import Config

CONFIG_FILE = "config.json"

DEFAULT_CONFIG: Config = {
    "server_nickname": "我的服务器",
    "server_slug": "my-server",
    "server_public_address": "127.0.0.1",
    "server_port": 25565,
}


def load_or_init_config(server: mcdr.PluginServerInterface) -> Config:
    config_path = os.path.join(server.get_data_folder(), CONFIG_FILE)

    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write(
                json.dumps(
                    DEFAULT_CONFIG,
                    indent=4,
                    ensure_ascii=False,
                )
            )
    with open(config_path, "r") as f:
        conf = json.load(f)

    return conf
