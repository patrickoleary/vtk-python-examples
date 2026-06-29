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
plane_source = vtkPlaneSource()
plane_source.SetXResolution(30)
plane_source.SetYResolution(30)
plane_source.SetOrigin(-1, -1, 0)
plane_source.SetPoint1(1, -1, 0)
plane_source.SetPoint2(-1, 1, 0)

# Filter: apply lens distortion
warp_lens = vtkWarpLens()
warp_lens.SetInputConnection(plane_source.GetOutputPort())
warp_lens.SetPrincipalPoint(0, 0)
warp_lens.SetFormatWidth(2)
warp_lens.SetFormatHeight(2)
warp_lens.SetImageWidth(2)
warp_lens.SetImageHeight(2)
warp_lens.SetK1(0.4)
warp_lens.SetK2(0.05)
warp_lens.SetP1(0)
warp_lens.SetP2(0)

# Mapper: map the warped grid to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(warp_lens.GetOutputPort())

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

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("warp lens")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
