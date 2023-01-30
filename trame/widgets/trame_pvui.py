from trame_pvui.widgets.trame_pvui import *


def initialize(server):
    from trame_pvui import module

    server.enable_module(module)
