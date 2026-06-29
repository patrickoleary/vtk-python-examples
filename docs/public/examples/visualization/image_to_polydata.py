#!/usr/bin/env python

# Demonstrate vtkImageToPolyDataFilter converting a PNG image to polygonal
# data using color quantization and decimation.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersHybrid import vtkImageToPolyDataFilter
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingColor import vtkImageQuantizeRGBToIndex
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read image
reader = vtkPNGReader()
reader.SetFileName(os.path.join(data_dir, "vtk.png"))

# Quantize colors
quant = vtkImageQuantizeRGBToIndex()
quant.SetInputConnection(reader.GetOutputPort())
quant.SetNumberOfColors(32)

# Convert image to polygonal data
i2pd = vtkImageToPolyDataFilter()
i2pd.SetInputConnection(quant.GetOutputPort())
i2pd.SetLookupTable(quant.GetLookupTable())
i2pd.SetColorModeToLUT()
i2pd.SetOutputStyleToPolygonalize()
i2pd.SetError(0)
i2pd.DecimationOn()
i2pd.SetDecimationError(0.0)
i2pd.SetSubImageSize(25)

# Triangulate complex/concave polygons
tf = vtkTriangleFilter()
tf.SetInputConnection(i2pd.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tf.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 250)
render_window.SetWindowName("image to polydata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
camera.SetClippingRange(343.331, 821.78)
camera.SetPosition(-139.802, -85.6604, 437.485)
camera.SetFocalPoint(117.424, 106.656, -14.6)
camera.SetViewUp(0.430481, 0.716032, 0.549532)
camera.SetViewAngle(30)
renderer.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
