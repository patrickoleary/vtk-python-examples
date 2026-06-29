#!/usr/bin/env python

# Demonstrate vtkExtractEdges on a plane source with cell data from
# a simple elevation filter, preserving original point numbering.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkExtractEdges,
    vtkSimpleElevationFilter,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 50

# Create a plane
plane = vtkPlaneSource()
plane.SetResolution(resolution, resolution)
plane.SetOrigin(0, 0, 0)
plane.SetPoint1(1, 0, 0)
plane.SetPoint2(0, 0, 1)
plane.Update()

# Create cell data using elevation filter
elevation = vtkSimpleElevationFilter()
elevation.SetInputConnection(plane.GetOutputPort())
elevation.Update()

# Extract edges preserving all points
extract = vtkExtractEdges()
extract.SetInputConnection(elevation.GetOutputPort())
extract.UseAllPointsOn()
extract.Update()

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(extract.GetOutputPort())
mapper.ScalarVisibilityOn()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetInterpolationToFlat()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("extract edges with cell data")

# Scene
renderer.GetActiveCamera().SetFocalPoint(0.5, 0, 0.5)
renderer.GetActiveCamera().SetPosition(0.5, 1, 0.5)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
