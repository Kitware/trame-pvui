from pathlib import Path
import logging

from paraview.simple import (
    IOSSReader,
    GetActiveViewOrCreate,
    GetAnimationScene,
    GetTimeKeeper,
    OpenDataFile,
    Render,
    SetActiveSource,
    Show,
)

from filebrowser_functions import (
    get_initial_state,
    get_applicable_file_types,
    get_dir_contents,
    save_file,
    open_file,
)
from serverbrowser_functions import (
    add_server,
    update_server,
)

from infopanel_functions import DataInformationMicroservice, DataAssemplyToDict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DATASET_PATH = Path("example_trame_apps/data/can.ex2").absolute()


class ParaviewEngine:
    def initialize(self, server):
        state, ctrl = server.state, server.controller
        self.state = state
        self.control = ctrl

        self.reader = IOSSReader(
            registrationName="can.ex2",
            FileName=[str(DATASET_PATH)],
        )
        self.animation = GetAnimationScene()
        self.time_keeper = GetTimeKeeper()
        self.animation.UpdateAnimationUsingDataTimeSteps()
        SetActiveSource(self.reader)
        self.render = GetActiveViewOrCreate("RenderView")
        self.repr = Show()
        self.view = Render()

        @ctrl.set("get_render_window")
        def get_render_window():
            return self.view


class FileBrowserEngine:
    def initialize(self, server):
        args, _ = server.cli.parse_known_args()
        state, ctrl = server.state, server.controller
        initial_state = get_initial_state(
            local_root=args.local_root,
            remote_root=args.remote_root,
        )
        for key, value in initial_state.items():
            setattr(state, key, value)
        state.file_types = get_applicable_file_types()
        ctrl.save_file = save_file
        ctrl.open_file = open_file

        @state.change("current_local_dir")
        def update_local_dir(current_local_dir, **kwargs):
            print("update local dir to", current_local_dir)
            state.current_local_dir_contents = get_dir_contents(current_local_dir)

        @state.change("current_remote_dir")
        def update_remote_dir(current_remote_dir, **kwargs):
            print("update remote dir to", current_remote_dir)
            state.current_remote_dir_contents = get_dir_contents(current_remote_dir)


class ServerBrowserEngine:
    def initialize(self, server):
        state, ctrl = server.state, server.controller
        state.servers = []
        ctrl.add_server = add_server
        ctrl.update_server = update_server


class InfoPanelEngine:
    def initialize(self, server):
        state = server.state

        split_path = str(DATASET_PATH).split("/")
        state.file_properties = {
            "name": split_path[-1],
            "path": "/".join(split_path[:-1]),
        }

        self.microservice = DataInformationMicroservice()
        proxy = OpenDataFile(str(DATASET_PATH))
        self.microservice.SetProxy(proxy)
        self.microservice.UpdateDataInformation()
        info = self.microservice.GetDataInformation()
        state.data_grouping = DataAssemplyToDict(info.GetHierarchy())
        state.timesteps = self.microservice.GetTimeSteps()

        @state.change("selected_node")
        def update_selected_node(selected_node, **kwargs):
            print("update selected node to", selected_node)
            if selected_node == "/Root":
                self.microservice.UpdateDataInformation()
            else:
                self.microservice.UpdateDataInformation(selectorPath=selected_node)
            node_info = self.microservice.GetDataInformation()

            state.data_statistics = {
                "type": node_info.GetPrettyDataTypeString(),
                "num_datasets": node_info.GetNumberOfDataSets(),
                "num_cells": node_info.GetNumberOfCells(),
                "num_points": node_info.GetNumberOfPoints(),
                "num_timesteps": node_info.GetNumberOfTimeSteps(),
                "current_time": node_info.GetTime(),
                "time_range": node_info.GetTimeRange(),
                "memory": node_info.GetMemorySize() * 1024,  # convert to bytes
                "bounds": node_info.GetBounds(),
            }
            state.data_arrays = []
            for array_collection in [
                node_info.GetPointDataInformation(),
                node_info.GetCellDataInformation(),
                node_info.GetFieldDataInformation(),
            ]:
                for i in range(array_collection.GetNumberOfArrays()):
                    array = array_collection.GetArrayInformation(i)
                    state.data_arrays.append(
                        {
                            "name": array.GetName(),
                            "type": array.GetDataTypeAsString(),
                            "ranges": array.GetRangesAsString(),
                            "partial": array.GetIsPartial(),
                        }
                    )

        state.selected_node = "/Root"


class WidgetTesterEngine:
    def initialize(self, server):
        ParaviewEngine().initialize(server)
        FileBrowserEngine().initialize(server)
        ServerBrowserEngine().initialize(server)
        InfoPanelEngine().initialize(server)


def initialize(server):
    WidgetTesterEngine().initialize(server)
