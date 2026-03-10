#!/usr/bin/env python

# Render a single vtkParametricSpline surface, centered and
# normalized to fit the viewport.  The spline interpolates 10
# random 3-D points generated with a fixed seed.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricSpline
from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
navajo_white_rgb = (1.0, 0.871, 0.678)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Parametric function: define a spline through 10 random control points
parametric_fn = vtkParametricSpline()
spline_points = vtkPoints()
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(8775070)
for _ in range(10):
    xyz = [0.0] * 3
    for j in range(3):
        xyz[j] = rng.GetRangeValue(-1.0, 1.0)
        rng.Next()
    spline_points.InsertNextPoint(xyz)
parametric_fn.SetPoints(spline_points)

# Source: sample the parametric function to produce polygonal output
source = vtkParametricFunctionSource()
source.SetParametricFunction(parametric_fn)
source.SetUResolution(51)
source.SetVResolution(51)
source.SetWResolution(51)
source.Update()

# Normalize: scale and center the surface to fit the viewport
bounds = source.GetOutput().GetBounds()
max_dim = max(bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])
scale = 3.0 / max_dim if max_dim > 0 else 1.0
cx = (bounds[0] + bounds[1]) / 2.0
cy = (bounds[2] + bounds[3]) / 2.0
cz = (bounds[4] + bounds[5]) / 2.0

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())
# Actor: position and scale the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(navajo_white_rgb)
actor.SetScale(scale, scale, scale)
actor.SetPosition(-cx * scale, -cy * scale, -cz * scale)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(midnight_blue_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("ParametricObjectSpline")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
