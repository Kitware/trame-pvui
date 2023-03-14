from trame_pvui.widgets.filebrowser import FileBrowser
from trame_pvui.widgets.infopanel import InfoPanel
from trame_pvui.widgets.colormapper import Colormapper
from trame_pvui.widgets.serverbrowser import ServerBrowser


def initialize(server):
    from trame_pvui import module

    server.enable_module(module)
