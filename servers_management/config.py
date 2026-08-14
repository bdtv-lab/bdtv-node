import json
import os

DEFAULT_CONFIG = {
    "server": "localhost",
    "port": 7497,
    "id": "main",
    "nickname": "主服务器",
}

def load_or_init_config(config_path: str) -> dict:
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
