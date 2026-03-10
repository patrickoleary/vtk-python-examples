#!/usr/bin/env python

# Thicken a stroked font using implicit modelling and contouring.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersHybrid import vtkImplicitModeller
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato = (1.000, 0.388, 0.278)
peacock = (0.200, 0.631, 0.788)
wheat = (0.961, 0.871, 0.702)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "hello.vtk")

# Reader: load the stroked font lines
reader = vtkPolyDataReader()
reader.SetFileName(file_name)

# Mapper: map the original lines to graphics primitives
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(reader.GetOutputPort())

# Actor: display the original lines
line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(tomato)
line_actor.GetProperty().SetLineWidth(3.0)

# Filter: compute distance field from the line geometry
imp = vtkImplicitModeller()
imp.SetInputConnection(reader.GetOutputPort())
imp.SetSampleDimensions(110, 40, 20)
imp.SetMaximumDistance(0.25)
imp.SetModelBounds(-1.0, 10.0, -1.0, 3.0, -1.0, 1.0)

# Filter: extract the isosurface at distance 0.25
contour = vtkContourFilter()
contour.SetInputConnection(imp.GetOutputPort())
contour.SetValue(0, 0.25)

# Mapper: map the thickened surface to graphics primitives
imp_mapper = vtkPolyDataMapper()
imp_mapper.SetInputConnection(contour.GetOutputPort())
imp_mapper.ScalarVisibilityOff()

# Actor: display the thickened surface
imp_actor = vtkActor()
imp_actor.SetMapper(imp_mapper)
imp_actor.GetProperty().SetColor(peacock)
imp_actor.GetProperty().SetOpacity(0.5)

# Renderer: assemble the scene and configure the camera
camera = vtkCamera()
camera.SetFocalPoint(4.5, 1, 0)
camera.SetPosition(4.5, 1.0, 6.73257)
camera.SetViewUp(0, 1, 0)

renderer = vtkRenderer()
renderer.AddActor(line_actor)
renderer.AddActor(imp_actor)
renderer.SetBackground(wheat)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()
camera.Dolly(1.3)
camera.SetClippingRange(1.81325, 90.6627)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Hello")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
