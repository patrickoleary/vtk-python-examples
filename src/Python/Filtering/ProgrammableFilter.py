#!/usr/bin/env python

# Demonstrate vtkProgrammableFilter to apply custom logic that computes a
# scalar field (distance from center) on a sphere mesh.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkFiltersProgrammable import vtkProgrammableFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: sphere
sphere = vtkSphereSource()
sphere.SetPhiResolution(32)
sphere.SetThetaResolution(32)

# Filter: programmable filter to compute distance from the +Z pole
prog_filter = vtkProgrammableFilter()
prog_filter.SetInputConnection(sphere.GetOutputPort())


def compute_distance():
    input_data = prog_filter.GetInput()
    output_data = prog_filter.GetOutput()
    output_data.ShallowCopy(input_data)

    scalars = vtkFloatArray()
    scalars.SetName("PoleDistance")
    scalars.SetNumberOfTuples(input_data.GetNumberOfPoints())

    for i in range(input_data.GetNumberOfPoints()):
        pt = input_data.GetPoint(i)
        dist = math.sqrt(pt[0] ** 2 + pt[1] ** 2 + (pt[2] - 1.0) ** 2)
        scalars.SetValue(i, dist)

    output_data.GetPointData().SetScalars(scalars)


prog_filter.SetExecuteMethod(compute_distance)

# Mapper: map the output to graphics primitives with scalar coloring
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(prog_filter.GetOutputPort())
mapper.SetScalarRange(0, 2)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ProgrammableFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
