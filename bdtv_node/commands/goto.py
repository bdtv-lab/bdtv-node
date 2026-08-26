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
    # if src.is_player:
    #     src = cast(mcdr.PlayerCommandSource, src)

    #     player_name = src.player
    #     target_server = ctx["server_name"]

    #     if target_server not in SERVERS:
    #         src.reply(f"并没有找到名为 {target_server} 的服务器。")
    #         return

    #     command = f"/transfer {SERVERS[target_server]['address']} {SERVERS[target_server]['port']} {player_name}"

    #     src.get_server().execute(command)
    #     src.get_server().say(
    #         mcdr.RTextList(
    #             f"§e{player_name}前往了{SERVERS[target_server]['nickname']}§r"
    #         )
    #     )
    # else:
    #     src.reply("Only players can use this command.")
    pass


def register_command(server: mcdr.PluginServerInterface):
    builder = mcdr.SimpleCommandBuilder()

    server.register_help_message("!!goto", "用于切换服务器的命令")
    builder.command("!!goto", list_servers)  # type: ignore[operator]
    builder.command("!!goto <server_slug>", switch_server)  # type: ignore[operator]

    builder.arg("server_slug", mcdr.Text)

    builder.register(server)
