import paraview.web.venv  # noqa
from trame.app import get_server, dev
import engine
import ui


def _reload():
    server = get_server()
    dev.reload(ui)
    ui.initialize(server)


def main(server=None, **kwargs):
    # Get or create server
    if server is None:
        server = get_server()

    if isinstance(server, str):
        server = get_server(server)

    # Make UI auto reload
    server.controller.on_server_reload.add(_reload)

    server.cli.add_argument("--local_root", default=".")
    server.cli.add_argument("--remote_root", default=".")

    # Init application
    engine.initialize(server)
    ui.initialize(server)

    # Start server
    server.start(**kwargs)


if __name__ == "__main__":
    main()
