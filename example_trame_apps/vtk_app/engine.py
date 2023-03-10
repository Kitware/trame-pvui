from vtk_pipeline import VtkPipeline
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DATASET_PATH = Path("example_trame_apps/data/skull.vti").absolute()

DEFAULT_COLOR_MAP = [
    [15, 0, 0, 0],
    [75, 0, 1, 0],
    [100, 1, 0, 0],
    [175, 0, 0, 1],
]

DEFAULT_OPACITY_MAP = [
    [0, 0, 0.7, 1],
    [70, 0.3, 0.2, 1],
    [190, 0.7, 0.5, 1],
    [255, 1, 0.5, 0],
]


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


class WidgetTesterEngine:
    def initialize(self, server):
        ColorMapperEngine().initialize(server)


def initialize(server):
    WidgetTesterEngine().initialize(server)
