#!/usr/bin/env python

# Contour a PLOT3D structured grid using vtkGridSynchronizedTemplates3D,
# sweeping through iso-values.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkGridSynchronizedTemplates3D,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load PLOT3D data
reader = vtkMultiBlockPLOT3DReader()
reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
reader.SetScalarFunctionNumber(100)
reader.SetVectorFunctionNumber(202)
reader.Update()

pl3d_output = reader.GetOutput().GetBlock(0)
scalar_range = pl3d_output.GetPointData().GetScalars().GetRange()
value = (scalar_range[0] + scalar_range[1]) / 2.0

# Contour with triangles
contour = vtkGridSynchronizedTemplates3D()
contour.SetInputData(pl3d_output)
contour.SetValue(0, value)
contour.GenerateTrianglesOn()

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.SetScalarRange(scalar_range)

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(pl3d_output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(contour_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("grid synchronized templates3d")

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(3.95297, 50)
camera.SetFocalPoint(9.71821, 0.458166, 29.3999)
camera.SetPosition(2.7439, -37.3196, 38.7167)
camera.SetViewUp(-0.16123, 0.264271, 0.950876)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
