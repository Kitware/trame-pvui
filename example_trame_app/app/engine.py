from .vtk_pipeline import VtkPipeline
from pathlib import Path
import logging

from .filebrowser_functions import (
    get_initial_state,
    get_applicable_file_types,
    get_dir_contents,
    save_file,
    open_file,
)
from .serverbrowser_functions import (
    add_server,
    update_server,
)
from .default_states import (
    DEFAULT_COLOR_MAP,
    DEFAULT_OPACITY_MAP,
    DEFAULT_SERVER_LIST,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DATASET_PATH = Path("example_trame_app/data/skull.vti").absolute()


class VtkPipelineEngine:
    def initialize(self, server):
        self.vtk_pipeline = VtkPipeline(DATASET_PATH)
        state, ctrl = server.state, server.controller
        state.trame__title = "View skull.vti"
        self.state = state
        self.ctrl = ctrl

        @ctrl.set("get_render_window")
        def get_render_window():
            return self.vtk_pipeline.render_window


class ColorMapperEngine(VtkPipelineEngine):
    def initialize(self, server, **kwargs):
        super().initialize(server)
        state, ctrl = server.state, server.controller
        state.colormap_points = DEFAULT_COLOR_MAP
        state.opacity_points = DEFAULT_OPACITY_MAP
        state.histogram_data = self.vtk_pipeline.get_histogram_data(buckets=10)

        @state.change("colormap_points")
        def update_colors(colormap_points, **kwargs):
            self.vtk_pipeline.update_colors(colormap_points)
            ctrl.view_update()

        @state.change("opacity_points")
        def update_opacity(opacity_points, **kwargs):
            self.vtk_pipeline.update_opacity(opacity_points)
            ctrl.view_update()

        @ctrl.set("reset_colormap_points")
        def reset_colormap_points(self):
            self._server.state.colormap_points = DEFAULT_COLOR_MAP


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
        state.servers = DEFAULT_SERVER_LIST
        ctrl.add_server = add_server
        ctrl.update_server = update_server


class WidgetTesterEngine:
    def initialize(self, server):
        ColorMapperEngine().initialize(server)
        FileBrowserEngine().initialize(server)
        ServerBrowserEngine().initialize(server)


def initialize(server):
    WidgetTesterEngine().initialize(server)
