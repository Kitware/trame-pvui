def test_import_via_package():
    from trame_pvui.widgets import (  # noqa: F401
        Colormapper,
        FileBrowser,
        ServerBrowser,
        InfoPanel,
    )


def test_import_via_trame():
    # For components only, the widgets are also importable via trame
    from trame.widgets.pvui import (  # noqa: F401
        Colormapper,
        FileBrowser,
        ServerBrowser,
        InfoPanel,
    )
