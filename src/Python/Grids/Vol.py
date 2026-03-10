#!/usr/bin/env python

# Create a structured points dataset with scalar data from a sphere equation.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkStructuredPoints
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
salmon_rgb = (0.980, 0.502, 0.447)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: create a 26^3 structured points dataset
vol = vtkStructuredPoints()
vol.SetDimensions(26, 26, 26)
vol.SetOrigin(-0.5, -0.5, -0.5)
sp = 1.0 / 25.0
vol.SetSpacing(sp, sp, sp)

# Scalars: compute x^2 + y^2 + z^2 - r^2 for a sphere of radius 0.4
scalars = vtkDoubleArray()
scalars.SetNumberOfComponents(1)
scalars.SetNumberOfTuples(26 * 26 * 26)
for k in range(26):
    z = -0.5 + k * sp
    k_offset = k * 26 * 26
    for j in range(26):
        y = -0.5 + j * sp
        j_offset = j * 26
        for i in range(26):
            x_val = -0.5 + i * sp
            s = x_val * x_val + y * y + z * z - (0.4 * 0.4)
            offset = i + j_offset + k_offset
            scalars.InsertTuple1(offset, s)
vol.GetPointData().SetScalars(scalars)

# ContourFilter: extract the zero-level isosurface (the sphere)
contour = vtkContourFilter()
contour.SetInputData(vol)
contour.SetValue(0, 0.0)

# Mapper: map the contour output to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(contour.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetColor(salmon_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(512, 512)
render_window.SetWindowName("Vol")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
