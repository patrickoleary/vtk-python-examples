#!/usr/bin/env python

# Create a vtkImageData, fill it with scalar values, write it to a .vti
# file using vtkXMLImageDataWriter, read it back with vtkXMLImageDataReader,
# and render the result.

import tempfile
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import VTK_DOUBLE
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOXML import (
    vtkXMLImageDataReader,
    vtkXMLImageDataWriter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a small 3D image data and fill with scalar values
image_data = vtkImageData()
image_data.SetDimensions(3, 4, 5)
image_data.AllocateScalars(VTK_DOUBLE, 1)

dims = image_data.GetDimensions()
for z in range(dims[2]):
    for y in range(dims[1]):
        for x in range(dims[0]):
            image_data.SetScalarComponentFromDouble(x, y, z, 0, x + y + z)

# Writer: save the image data to a temporary .vti file
tmp_path = Path(tempfile.gettempdir()) / "WriteReadVtkImageData.vti"
writer = vtkXMLImageDataWriter()
writer.SetFileName(str(tmp_path))
writer.SetInputData(image_data)
writer.Write()

# Reader: load the .vti file back
reader = vtkXMLImageDataReader()
reader.SetFileName(str(tmp_path))
reader.Update()

# Filter: convert image data to polydata for rendering
geometry_filter = vtkImageDataGeometryFilter()
geometry_filter.SetInputConnection(reader.GetOutputPort())

# Mapper: map polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry_filter.GetOutputPort())
mapper.SetScalarRange(0.0, dims[0] + dims[1] + dims[2] - 3.0)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(5)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("WriteReadVtkImageData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
