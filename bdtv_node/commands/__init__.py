import mcdreforged as mcdr

from . import goto


def register_command(server: mcdr.PluginServerInterface):
    goto.register_command(server)
