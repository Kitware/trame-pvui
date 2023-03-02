from .widget import HtmlElement


# -----------------------------------------------------------------------------
# Information Panel Widget
# -----------------------------------------------------------------------------
class InfoPanel(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "info-panel",
            **kwargs,
        )
        # for future reference:
        # if self.server.client_type == 'Vue3':
        # self._elem_name = 'info-panel-3'
        self._attr_names += [
            ("selected_node", "selectedNode"),
            ("file_properties", "fileProperties"),
            ("data_grouping", "dataGrouping"),
            ("data_statistics", "dataStatistics"),
            ("data_arrays", "dataArrays"),
            ("timesteps", "timesteps"),
        ]
        self._event_names += [
            ("set_selected_node", "setSelectedNode"),
        ]