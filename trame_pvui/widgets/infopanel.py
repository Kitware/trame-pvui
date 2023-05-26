from .widget import HtmlElement


# -----------------------------------------------------------------------------
# Information Panel Widget
# -----------------------------------------------------------------------------
class InfoPanel(HtmlElement):
    """
     The InfoPanel widget for trame allows to display information organized in 5
     sections of tabulated data: "File Properties", "Data Grouping", "Data
     Statistics", "Data Arrays" and "TimeSteps"

    `file_properties` is a dictionary with the following format:
    {
      name:str,
      path:str,
    }


    `data_statistics` is a dictionary with the following format:
    # TODO say which are optional
     {
       type: str,
       num_datasets: int,
       num_cells: int,
       num_points: int,
       num_timesteps: int,
       current_time: float,
       time_range: [float,float]
       memory: int (in bytes),
       bounds: [int,int,int,int,int,int] in  [xmin,xam,ymin,ymax,zmin,zmax] order
     }


     `data_grouping` a list of dictionaries
     [
       {
         id: int
         name: str
         path: str
         children: [int]
       },
     ]

     `data_arrays` is a list of dictionaries with the following fields

      {
        name : str
        type: str
        ranges: str if type == str, list([min,max] of each component ) otherwise
        partial: int
      }

      and is rendered as a table :
       Name   |   Type    |  Ranges
              |           |
              ....
     where each list entry is a row in the table.

     `timesteps` is list of the timestep values available in the dataset.

     `byte_formatter": A (name of a) Javascript function to format the memory field of data_statistics.
     `float_formatter": A (name of a) Javascript function to format floats throughout the panel.
     `integer_formatter": A (name of a) Javascript function to format integers throughout the panel.


     Events:

     :param set_selected_node: Event triggered when the selects one of the nodes of data_grouping tree.
     :type set_selected_node: TODO
    """

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
            ("byte_formatter", "byteFormatter"),
            ("integer_formatter", "integerFormatter"),
            ("float_formatter", "floatFormatter"),
            ("visible_content", "visibleContent"),
        ]
        self._event_names += [
            ("set_selected_node", "setSelectedNode"),
            ("toggle_visible_content", "toggleVisibleContent"),
        ]
