from .widget import HtmlElement


# -----------------------------------------------------------------------------
# Server Browser Widget
# -----------------------------------------------------------------------------
class ServerBrowser(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )
        self._attr_names += [
            "dark",
        ]
        self.event_names = []
