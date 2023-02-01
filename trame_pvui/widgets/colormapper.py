from .widget import HtmlElement


# -----------------------------------------------------------------------------
# Colormapper Widget
# -----------------------------------------------------------------------------
class Colormapper(HtmlElement):
    """
    The ColormapEditor widget for trame allows the user to edit two lists:
    The first is the color list, wherein each item is a list providing [val, R, G, B].
    The items in the first list should be added to a VTKColorTransferFunction via `AddRGBPoint(*item)`.
    The second is the opacity list, wherein each item is a list providing [val, opacity, midpoint, sharpness].
    The items in the second list should be added to a VTKPiecewiseFunction via `AddPoint(*item)`.
    When connected to a VTK pipeline, these transfer functions will adjust the appearance of the rendered scene.
    The widget also displays a histogram of the target image, and therefore requires the histogram data as a parameter.
    The histogram data should be provided as a dictionary with keys "range" and "counts",
        where each value is a list of numbers.

    :param dark: true for dark UI mode, false otherwise
    :type dark: bool
    :param colors: The current color list.
    :type colors: list[list[number]]
    :param opacities: The current opacity list.
    :type opacities: list[list[number]]
    :param histogram_data: The histogram of the scalar data for the target image, organized into buckets.
    :type histogram_data: {range: list[number], counts: list[number]}
    """

    def __init__(self, **kwargs):
        super().__init__(
            "colormapper",
            **kwargs,
        )
        self._attr_names += [
            ("histogram_data", "histogramData"),
            "colors",
            "opacities",
            "dark",
        ]
        self._event_names += [
            ("update_colors", "updateColors"),
            ("update_opacities", "updateOpacities"),
        ]
