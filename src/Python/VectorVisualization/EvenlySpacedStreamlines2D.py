#!/usr/bin/env python

# Generate evenly spaced 2D streamlines from a procedural vector field
# using vtkEvenlySpacedStreamlines2D. The vector field is a rotating
# vortex defined on a uniform grid.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersFlowPaths import vtkEvenlySpacedStreamlines2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.000, 0.388, 0.278)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a 2D vector field on a uniform grid
nx, ny = 64, 64
image = vtkImageData()
image.SetDimensions(nx, ny, 1)
image.SetOrigin(-2.0, -2.0, 0.0)
image.SetSpacing(4.0 / (nx - 1), 4.0 / (ny - 1), 1.0)

vectors = vtkFloatArray()
vectors.SetNumberOfComponents(3)
vectors.SetNumberOfTuples(nx * ny)
vectors.SetName("Velocity")
for j in range(ny):
    for i in range(nx):
        x = -2.0 + 4.0 * i / (nx - 1)
        y = -2.0 + 4.0 * j / (ny - 1)
        r = math.sqrt(x * x + y * y) + 1e-10
        speed = 1.0 / (1.0 + r * r)
        vx = -y * speed
        vy = x * speed
        vectors.SetTuple3(j * nx + i, vx, vy, 0.0)

image.GetPointData().SetVectors(vectors)

# Filter: generate evenly spaced streamlines in 2D
streamer = vtkEvenlySpacedStreamlines2D()
streamer.SetInputData(image)
streamer.SetStartPosition(0.5, 0.0, 0.0)
streamer.SetSeparatingDistance(0.3)
streamer.SetSeparatingDistanceRatio(0.5)
streamer.SetIntegratorTypeToRungeKutta4()
streamer.SetMaximumNumberOfSteps(2000)
streamer.SetTerminalSpeed(1e-12)
streamer.SetClosedLoopMaximumDistance(0.15)

# Mapper: map streamlines to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(streamer.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato_rgb)
actor.GetProperty().SetLineWidth(2)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().ParallelProjectionOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 640)
render_window.SetWindowName("EvenlySpacedStreamlines2D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
