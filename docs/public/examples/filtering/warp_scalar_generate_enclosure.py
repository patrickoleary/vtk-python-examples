#!/usr/bin/env python

# Demonstrate vtkWarpScalar with GenerateEnclosure by creating a plane,
# adding a scalar warp attribute based on point distance from origin,
# warping the surface, and rendering the enclosed result.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkLookupTable,
    vtkMath,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a plane
plane = vtkPlaneSource()
plane.SetResolution(7, 7)
plane.Update()

# Add scalar attribute based on distance from origin
output = plane.GetOutput()
n_pts = output.GetNumberOfPoints()
warping = vtkFloatArray()
warping.SetName("Warp")
warping.SetNumberOfComponents(1)
warping.SetNumberOfTuples(n_pts)
for i in range(n_pts):
    pt = output.GetPoint(i)
    warping.SetValue(i, math.sqrt(pt[0] ** 2 + pt[1] ** 2 + pt[2] ** 2) + 1.0)
output.GetPointData().AddArray(warping)
output.GetPointData().SetActiveScalars("Warp")

# Warp by scalar with enclosure generation
warper = vtkWarpScalar()
warper.SetInputConnection(plane.GetOutputPort())
warper.GenerateEnclosureOn()
warper.SetScaleFactor(0.5)
warper.Update()

# Lookup table
warp_output = warper.GetOutput()
warp_output.GetPointData().SetActiveScalars("Warp")
scalar_range = warp_output.GetPointData().GetScalars().GetRange()

lut = vtkLookupTable()
lut.SetRange(scalar_range)
lut.Build()

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(warper.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetScalarRange(scalar_range)
mapper.SetLookupTable(lut)

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
render_window.SetWindowName("warp scalar generate enclosure")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(9, 9, 9)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
