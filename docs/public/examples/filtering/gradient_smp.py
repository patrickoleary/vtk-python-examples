#!/usr/bin/env python

# Demonstrate vtkGradientFilter on a line source, verifying the filter
# handles SMP backends correctly without crashing, and visualizing
# the line with computed gradient data.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersGeneral import vtkGradientFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a line source
line_source = vtkLineSource()
line_source.Update()

# Compute gradient on the line
gradient = vtkGradientFilter()
gradient.SetInputData(line_source.GetOutput())
gradient.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Texture Coordinates"
)
gradient.Update()

# Add tube geometry so the line is visible
tube = vtkTubeFilter()
tube.SetInputConnection(gradient.GetOutputPort())
tube.SetRadius(0.02)
tube.SetNumberOfSides(12)

# Render colored by texture coordinates
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tube.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("Texture Coordinates")
mapper.SetScalarRange(0, 1)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("gradient smp")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
