from vtk import (
    vtkXMLImageDataReader,
    vtkFixedPointVolumeRayCastMapper,
    vtkColorTransferFunction,
    vtkPiecewiseFunction,
    vtkVolumeProperty,
    vtkVolume,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtk.util.numpy_support import vtk_to_numpy
import numpy


class VtkPipeline:
    def __init__(self, input_image):
        self.load_file(input_image)

        color_function = vtkColorTransferFunction()
        opacity_function = vtkPiecewiseFunction()

        volume_property = vtkVolumeProperty()
        volume_property.SetColor(color_function)
        volume_property.SetScalarOpacity(opacity_function)

        actor = vtkVolume()
        actor.SetProperty(volume_property)
        actor.SetMapper(self.mapper)
        renderer = vtkRenderer()
        render_window = vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_interactor = vtkRenderWindowInteractor()
        render_interactor.SetRenderWindow(render_window)
        render_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
        renderer.AddVolume(actor)
        renderer.ResetCamera()

        self.color_function = color_function
        self.opacity_function = opacity_function
        self.render_window = render_window

    def load_file(self, input_image):
        self.reader = vtkXMLImageDataReader()
        self.reader.SetFileName(input_image)
        self.reader.Update()
        mapper = vtkFixedPointVolumeRayCastMapper()
        mapper.SetInputConnection(self.reader.GetOutputPort())
        self.mapper = mapper

    def get_histogram_data(self, buckets):
        print(self.reader.GetOutput().GetPointData())
        scalar_data_source = vtk_to_numpy(
            self.reader.GetOutput().GetPointData().GetScalars()
        )
        bucket_counts, bucket_edges = numpy.histogram(scalar_data_source, buckets)
        histogram_data = {
            "counts": bucket_counts.tolist(),
            "range": [
                bucket_edges[0],
                bucket_edges[-1],
            ],
        }
        return histogram_data

    def update_colors(self, colormap_points):
        self.color_function.RemoveAllPoints()
        for point in colormap_points:
            self.color_function.AddRGBPoint(*point)

    def update_opacity(self, opacity_points):
        self.opacity_function.RemoveAllPoints()
        for point in opacity_points:
            self.opacity_function.AddPoint(*point)

    #  add any other pipeline functions
