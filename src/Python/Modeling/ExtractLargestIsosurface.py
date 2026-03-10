#!/usr/bin/env python

# Read a structured points volume, extract an isosurface with
# vtkFlyingEdges3D, and keep only the largest connected region
# using vtkPolyDataConnectivityFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdges3D,
    vtkPolyDataConnectivityFilter,
)
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
skin_rgb = (0.941, 0.722, 0.627)
backface_rgb = (1.000, 0.898, 0.784)

# Reader: load the brain volume
script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(script_dir, "brain.vtk")

reader = vtkStructuredPointsReader()
reader.SetFileName(file_name)

# Filter: extract isosurface at threshold 50
surface = vtkFlyingEdges3D()
surface.SetInputConnection(reader.GetOutputPort())
surface.ComputeNormalsOn()
surface.ComputeGradientsOn()
surface.SetValue(0, 50)

# Filter: keep only the largest connected region
connectivity = vtkPolyDataConnectivityFilter()
connectivity.SetInputConnection(surface.GetOutputPort())
connectivity.SetExtractionModeToLargestRegion()

# Mapper: map the largest isosurface
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(connectivity.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: the brain surface with backface color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(skin_rgb)

back_prop = vtkProperty()
back_prop.SetDiffuseColor(backface_rgb)
actor.SetBackfaceProperty(back_prop)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
renderer.GetActiveCamera().SetPosition(0.0, 1.0, 0.0)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.0, 0.0)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30.0)
renderer.GetActiveCamera().Elevation(30.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ExtractLargestIsosurface")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
