#!/usr/bin/env python

# Create a structured grid of a semi-cylinder with tangential vectors.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkHedgeHog
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.0, 0.843, 0.0)
midnight_blue_rgb = (0.098, 0.098, 0.439)

r_min = 0.5
r_max = 1.0
dims = [13, 11, 11]

# Source: create a structured grid representing a semi-cylinder
sgrid = vtkStructuredGrid()
sgrid.SetDimensions(dims)

vectors = vtkDoubleArray()
vectors.SetNumberOfComponents(3)
vectors.SetNumberOfTuples(dims[0] * dims[1] * dims[2])
points = vtkPoints()
points.Allocate(dims[0] * dims[1] * dims[2])

delta_z = 2.0 / (dims[2] - 1)
delta_rad = (r_max - r_min) / (dims[1] - 1)
x = [0.0] * 3
v = [0.0] * 3
for k in range(dims[2]):
    x[2] = -1.0 + k * delta_z
    k_offset = k * dims[0] * dims[1]
    for j in range(dims[1]):
        radius = r_min + j * delta_rad
        j_offset = j * dims[0]
        for i in range(dims[0]):
            theta = i * vtkMath.RadiansFromDegrees(15.0)
            x[0] = radius * math.cos(theta)
            x[1] = radius * math.sin(theta)
            v[0] = -x[1]
            v[1] = x[0]
            offset = i + j_offset + k_offset
            points.InsertPoint(offset, x)
            vectors.InsertTuple(offset, v)

sgrid.SetPoints(points)
sgrid.GetPointData().SetVectors(vectors)

# HedgeHog: display vectors as oriented lines
hedgehog = vtkHedgeHog()
hedgehog.SetInputData(sgrid)
hedgehog.SetScaleFactor(0.1)

# Mapper: map the hedgehog output to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(hedgehog.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(gold_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(midnight_blue_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(60.0)
renderer.GetActiveCamera().Azimuth(30.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("SGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
