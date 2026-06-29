#!/usr/bin/env python

# Demonstrate vtkRemovePolyData with exact matching vs non-exact matching.
# Two viewports show the difference: exact match only removes cells whose
# point ids match exactly, non-exact match removes cells with subset points.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkRemovePolyData
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

res = 3

# Create a grid of cells
plane = vtkPlaneSource()
plane.SetResolution(res, res)
plane.Update()

# Mark cells to be deleted - one exact match, one subset
pd = vtkPolyData()
pd.SetPoints(plane.GetOutput().GetPoints())
cells = vtkCellArray()
cells.InsertNextCell(4, [0, 1, 5, 4])
cells.InsertNextCell(3, [10, 11, 14])
pd.SetPolys(cells)

# Exact match: only the quad [0,1,5,4] is removed, the triangle [10,11,14]
# does not exactly match any cell
remove_1 = vtkRemovePolyData()
remove_1.AddInputConnection(plane.GetOutputPort())
remove_1.AddInputData(pd)
remove_1.ExactMatchOn()
remove_1.Update()

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(remove_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Non-exact match: cells containing subset points are also removed
remove_2 = vtkRemovePolyData()
remove_2.AddInputConnection(plane.GetOutputPort())
remove_2.AddInputData(pd)
remove_2.ExactMatchOff()
remove_2.Update()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(remove_2.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Two renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1.0)
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1.0, 1.0)

renderer_0.AddActor(actor_1)
renderer_1.AddActor(actor_2)

renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 150)
render_window.SetWindowName("remove polydata exact match")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.GetActiveCamera().SetPosition(0, 0, 1)
renderer_0.ResetCamera()

interactor.Initialize()
interactor.Start()
