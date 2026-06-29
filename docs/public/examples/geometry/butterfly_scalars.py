#!/usr/bin/env python

# Demonstrate vtkButterflySubdivisionFilter by creating a cylinder,
# triangulating it, assigning per-point colors, subdividing with the
# butterfly scheme, and rendering the smooth result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkUnsignedCharArray
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersModeling import vtkButterflySubdivisionFilter
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a cylinder source
cylinder = vtkCylinderSource()
cylinder.Update()

# Triangulate for subdivision
triangles = vtkTriangleFilter()
triangles.SetInputConnection(cylinder.GetOutputPort())
triangles.Update()

original_mesh = triangles.GetOutput()

# Assign per-point colors
colors = vtkUnsignedCharArray()
colors.SetNumberOfComponents(3)
colors.SetNumberOfTuples(original_mesh.GetNumberOfPoints())
colors.SetName("Colors")

for i in range(original_mesh.GetNumberOfPoints()):
    if 0 < i < 5:
        colors.SetTuple3(i, 255, 255, 0)
    elif 4 < i < 10:
        colors.SetTuple3(i, 0, 0, 255)
    else:
        colors.SetTuple3(i, 255, 0, 0)

original_mesh.GetPointData().SetScalars(colors)

# Butterfly subdivision
subdivision = vtkButterflySubdivisionFilter()
subdivision.SetNumberOfSubdivisions(4)
subdivision.SetInputData(original_mesh)

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(subdivision.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("butterfly scalars")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
