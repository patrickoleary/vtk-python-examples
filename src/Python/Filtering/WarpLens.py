#!/usr/bin/env python

# Demonstrate vtkWarpLens to apply barrel/pincushion lens distortion to
# a regular planar grid.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkWarpLens
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: planar grid
plane = vtkPlaneSource()
plane.SetXResolution(30)
plane.SetYResolution(30)
plane.SetOrigin(-1, -1, 0)
plane.SetPoint1(1, -1, 0)
plane.SetPoint2(-1, 1, 0)

# Filter: apply lens distortion
warp = vtkWarpLens()
warp.SetInputConnection(plane.GetOutputPort())
warp.SetPrincipalPoint(0, 0)
warp.SetFormatWidth(2)
warp.SetFormatHeight(2)
warp.SetImageWidth(2)
warp.SetImageHeight(2)
warp.SetK1(0.4)
warp.SetK2(0.05)
warp.SetP1(0)
warp.SetP2(0)

# Mapper: map the warped grid to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(warp.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornflower_blue_rgb)
actor.GetProperty().SetRepresentationToWireframe()
actor.GetProperty().SetLineWidth(2)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("WarpLens")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
