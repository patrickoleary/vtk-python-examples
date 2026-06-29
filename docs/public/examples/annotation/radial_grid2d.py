#!/usr/bin/env python

# Test vtkRadialGridActor2D with custom axes, ticks, angles, and text properties.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkOutlineSource
from vtkmodules.vtkRenderingAnnotation import vtkRadialGridActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Radial grid
radial_grid = vtkRadialGridActor2D()
radial_grid.GetProperty().SetColor(1, 0, 0)
radial_grid.GetProperty().SetLineWidth(2)
radial_grid.GetTextProperty().SetColor(1, 0, 1)
radial_grid.GetTextProperty().SetFontSize(18)
radial_grid.GetTextProperty().BoldOn()
radial_grid.SetNumberOfAxes(4)
radial_grid.SetNumberOfTicks(3)
radial_grid.SetStartAngle(42)
radial_grid.SetEndAngle(-87)
radial_grid.SetOrigin(0.3, 0.6)
radial_grid.SetAxesViewportLength(150)

# Outline for context
outline_source = vtkOutlineSource()

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_source.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(radial_grid)
renderer.AddActor(outline_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("radial grid2d")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
