from typing import cast

import mcdreforged as mcdr
from mcdreforged.api.decorator import new_thread

from .. import state
from ..utils import try_get_servers


@new_thread("GotoList")
def list_servers(src: mcdr.CommandSource, ctx: mcdr.CommandContext):
    servers = try_get_servers(src.get_server())

    if servers is None:
        src.reply("获取在线服务器失败")
        return

    t = [mcdr.RText(f"现在有{len(servers)}个服务器在线"), mcdr.RText("\n")]

    for index, server in enumerate(servers):
        if index > 0:
            t.append(mcdr.RText("\n"))

        s = [
            mcdr.RText(f"{server['nickname']}", color=mcdr.RColor.green).h(
                f"{server['slug']}"
            ),
            mcdr.RText(" ", color=mcdr.RColor.green),
        ]
        if server["slug"] == state.server_data["slug"]:
            s.append(
                mcdr.RText("(当前)", color=mcdr.RColor.yellow).h("你在这个服务器里")
            )
        else:
            s.append(
                mcdr.RText(">前往", color=mcdr.RColor.yellow)
                .h("点击前往")
                .c(mcdr.RClickAction.suggest_command, f"!!goto {server['slug']}")
            )

        t.extend(s)

    src.reply(mcdr.RTextList(*t))


@new_thread("GotoSwitch")
def switch_server(src: mcdr.CommandSource, ctx: mcdr.CommandContext):
    if not src.is_player:
        src.reply("Only players can use this command.")
        return

    src = cast(mcdr.PlayerCommandSource, src)

    player_name = src.player
    target_server_slug = ctx["server_slug"]

    if target_server_slug == state.server_data["slug"]:
        src.reply("你已经在这个服务器里了")
        return

    servers = try_get_servers(src.get_server())

    if servers is None:
        src.reply("获取在线服务器失败")
        return

    for server in servers:
        if server["slug"] != target_server_slug:
            continue

        command = f"/transfer {server['address']} {server['port']} {player_name}"
        src.get_server().execute(command)
        src.get_server().say(
            mcdr.RTextList(f"§e{player_name}前往了{server['nickname']}§r")
        )
        break
    else:
        t = [
            mcdr.RText("没有ID为"),
            mcdr.RText(f"{target_server_slug}", color=mcdr.RColor.aqua),
            mcdr.RText("的服务器在线，试试使用"),
            mcdr.RText("!!goto", color=mcdr.RColor.yellow)
            .h("点击执行")
            .c(mcdr.RClickAction.suggest_command, "!!goto"),
            mcdr.RText("命令查看在线服务器清单"),
        ]
        src.reply(mcdr.RTextList(*t))


def register_command(server: mcdr.PluginServerInterface):
    builder = mcdr.SimpleCommandBuilder()

    server.register_help_message("!!goto", "用于切换服务器的命令")
    builder.command("!!goto", list_servers)  # type: ignore[operator]
    builder.command("!!goto <server_slug>", switch_server)  # type: ignore[operator]

    builder.arg("server_slug", mcdr.Text)

    builder.register(server)
