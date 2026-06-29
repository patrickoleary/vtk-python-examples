#!/usr/bin/env python

# Demonstrate vtkSubdivideTetra by creating a single tetrahedron,
# subdividing it, shrinking the cells, and rendering the result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkTetra, vtkUnstructuredGrid
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersModeling import vtkSubdivideTetra
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a single tetrahedron
tetra_points = vtkPoints()
tetra_points.SetNumberOfPoints(4)
tetra_points.InsertPoint(0, 0, 0, 0)
tetra_points.InsertPoint(1, 1, 0, 0)
tetra_points.InsertPoint(2, 0.5, 1, 0)
tetra_points.InsertPoint(3, 0.5, 0.5, 1)

a_tetra = vtkTetra()
a_tetra.GetPointIds().SetId(0, 0)
a_tetra.GetPointIds().SetId(1, 1)
a_tetra.GetPointIds().SetId(2, 2)
a_tetra.GetPointIds().SetId(3, 3)

a_tetra_grid = vtkUnstructuredGrid()
a_tetra_grid.Allocate(1, 1)
a_tetra_grid.InsertNextCell(a_tetra.GetCellType(), a_tetra.GetPointIds())
a_tetra_grid.SetPoints(tetra_points)

# Subdivide
subdivide = vtkSubdivideTetra()
subdivide.SetInputData(a_tetra_grid)

# Shrink cells for visualization
shrinker = vtkShrinkFilter()
shrinker.SetInputConnection(subdivide.GetOutputPort())

mapper = vtkDataSetMapper()
mapper.SetInputConnection(shrinker.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.7400, 0.9900, 0.7900)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("sub divide tetra")

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(0.183196, 9.15979)
camera.SetFocalPoint(0.579471, 0.462507, 0.283392)
camera.SetPosition(-1.04453, 0.345281, -0.556222)
camera.SetViewUp(0.197321, 0.843578, -0.499441)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
