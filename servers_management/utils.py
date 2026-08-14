import json
import os

import mcdreforged as mcdr


def get_ops(server: mcdr.PluginServerInterface) -> list[dict]:
    with open(
        os.path.join(server.get_mcdr_config()["working_directory"], "ops.json"), "r"
    ) as f:
        ops = json.load(f)

        return ops


def get_whitelist(server: mcdr.PluginServerInterface) -> list[dict]:
    with open(
        os.path.join(server.get_mcdr_config()["working_directory"], "whitelist.json"),
        "r",
    ) as f:
        whitelist = json.load(f)

        return whitelist


def get_op_level(server: mcdr.PluginServerInterface, player_name: str) -> int:
    ops = get_ops(server)
    for op in ops:
        if op["name"] == player_name:
            return op["level"]
    return 0


def check_whitelist(server: mcdr.PluginServerInterface, player_name: str) -> bool:
    whitelist = get_whitelist(server)
    for player in whitelist:
        if player["name"] == player_name:
            return True
    return False
