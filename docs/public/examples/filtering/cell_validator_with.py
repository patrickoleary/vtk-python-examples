#!/usr/bin/env python

# Demonstrate vtkCellValidator as a filter by creating polydata with
# valid and invalid cells, running the validator, and rendering cells
# colored by their validity state.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkCellValidator
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create polydata with valid and invalid cells
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)     # 0
points.InsertNextPoint(0, 0, 1)     # 1
points.InsertNextPoint(0, 1, 1)     # 2
points.InsertNextPoint(0, 1, 0)     # 3
points.InsertNextPoint(0, 0.1, 0.1) # 4

polydata = vtkPolyData()
polydata.SetPoints(points)

# Lines (valid)
lines = vtkCellArray()
lines.InsertNextCell(2, [0, 1])
lines.InsertNextCell(2, [2, 3])
polydata.SetLines(lines)

# Polygons: mix of valid and invalid
polys = vtkCellArray()
# Valid quad
polys.InsertNextCell(4, [0, 1, 2, 3])
# Invalid: bowtie quad (self-intersecting)
polys.InsertNextCell(4, [0, 1, 3, 2])
# Nonconvex quad
polys.InsertNextCell(4, [0, 1, 4, 3])
# Degenerate: only 2 points for a polygon
polys.InsertNextCell(2, [0, 1])
polydata.SetPolys(polys)

# Run the validator filter
validator = vtkCellValidator()
validator.SetInputData(polydata)
validator.Update()

# Render result colored by validity state
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(validator.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("ValidityState")
mapper.SetScalarRange(0, 4)

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
render_window.SetWindowName("cell validator with")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(1, 0.5, 0.5)
renderer.GetActiveCamera().SetFocalPoint(0, 0.5, 0.5)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
