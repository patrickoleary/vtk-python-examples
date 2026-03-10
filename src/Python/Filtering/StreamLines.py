#!/usr/bin/env python

# Generate a synthetic vector field on a rectilinear grid and trace
# streamlines through it using vtkStreamTracer, displayed as tubes.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.0, 0.843, 0.0)
background_rgb = (0.1, 0.1, 0.2)

# Source: create a 3D image data with a swirling vector field
dims = (30, 30, 30)
image_data = vtkImageData()
image_data.SetDimensions(dims)
image_data.SetOrigin(-1.5, -1.5, -1.5)
spacing = 3.0 / (dims[0] - 1)
image_data.SetSpacing(spacing, spacing, spacing)

vectors = vtkFloatArray()
vectors.SetNumberOfComponents(3)
vectors.SetName("Vectors")
for k in range(dims[2]):
    for j in range(dims[1]):
        for i in range(dims[0]):
            x = -1.5 + i * spacing
            y = -1.5 + j * spacing
            z = -1.5 + k * spacing
            r = math.sqrt(x * x + y * y + z * z) + 1e-6
            vx = -y / r
            vy = x / r
            vz = 0.3
            vectors.InsertNextTuple3(vx, vy, vz)

image_data.GetPointData().SetVectors(vectors)

# Seed: generate random seed points near the center
seed_source = vtkPointSource()
seed_source.SetCenter(0, 0, -1.0)
seed_source.SetRadius(0.5)
seed_source.SetNumberOfPoints(50)

# Filter: trace streamlines through the vector field
stream_tracer = vtkStreamTracer()
stream_tracer.SetInputData(image_data)
stream_tracer.SetSourceConnection(seed_source.GetOutputPort())
stream_tracer.SetMaximumPropagation(10)
stream_tracer.SetIntegrationDirectionToForward()
stream_tracer.SetComputeVorticity(False)

# Filter: wrap tubes around the streamlines
tube_filter = vtkTubeFilter()
tube_filter.SetInputConnection(stream_tracer.GetOutputPort())
tube_filter.SetRadius(0.02)
tube_filter.SetNumberOfSides(8)

# Mapper: map the streamline tubes to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tube_filter.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(gold_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("StreamLines")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
