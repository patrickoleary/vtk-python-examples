#!/usr/bin/env python

# Demonstrate vtkContourFilter on an implicit array representing a
# sphere level set over an image data grid.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a grid and compute a sphere level set explicitly
n_pix = 300
half_cells = n_pix // 2 - 1
spacing = 1.0 / n_pix
radius = 0.60

base_grid = vtkImageData()
base_grid.SetExtent(-half_cells, half_cells, -half_cells, half_cells, -half_cells, half_cells)
base_grid.SetSpacing(spacing, spacing, spacing)

# Compute level set values: distance to origin minus radius
level_set = vtkFloatArray()
level_set.SetName("LevelSet")
level_set.SetNumberOfComponents(1)
num_points = base_grid.GetNumberOfPoints()
level_set.SetNumberOfTuples(num_points)

for i in range(num_points):
    pt = base_grid.GetPoint(i)
    dist = math.sqrt(pt[0] * pt[0] + pt[1] * pt[1] + pt[2] * pt[2])
    level_set.SetValue(i, dist - radius)

base_grid.GetPointData().AddArray(level_set)
base_grid.GetPointData().SetActiveScalars("LevelSet")

# Contour at the zero level set
contour = vtkContourFilter()
contour.SetInputData(base_grid)
contour.SetValue(0, 0.0)
contour.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(contour.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("contour implicit arrays")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(9, 9, 9)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
