from .widget import HtmlElement


# -----------------------------------------------------------------------------
# Server Browser Widget
# -----------------------------------------------------------------------------
class ServerBrowser(HtmlElement):
    """
    The ServerBrowser widget for trame allows the user to manage
    a list of local and remote servers.
    Server objects are dictionaries with the following shape:
    {
        name: str
        host: str
        port: number
        startupCommand: str
        type: str
        waitTime: number
    }

    :param dark: true for dark UI mode, false otherwise
    :type dark: bool
    :param servers: a list of all available server objects
    :type servers: list[server]

    Events:

    :param add: Event triggered when the user creates a new server object
        and submits it to be added to the list of available servers
    :type add: Function or JS expression (event)
    :param update: Event triggered when the user edits the values on a
        single server object and submits the changes to be saved to the
        list of available servers.
    :type update: Function or JS expression (event)
    """

    def __init__(self, **kwargs):
        super().__init__(
            "server-browser",
            **kwargs,
        )
        self._attr_names += [
            "dark",
            "servers",
        ]
        self._event_names += [
            ("add_server", "add"),
            ("update_server", "update"),
        ]
