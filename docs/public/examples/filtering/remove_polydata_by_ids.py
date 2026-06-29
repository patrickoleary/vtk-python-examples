#!/usr/bin/env python

# Demonstrate vtkRemovePolyData removal using cell ids, point ids, cells,
# and a combination. Four viewports show the results side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIdTypeArray
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

# Mark cells to be deleted (plus one bogus cell)
pd = vtkPolyData()
pd.SetPoints(plane.GetOutput().GetPoints())
cells = vtkCellArray()
cells.InsertNextCell(4, [1, 2, 6, 5])
cells.InsertNextCell(4, [1, 2, 6, 4])
cells.InsertNextCell(4, [4, 5, 9, 8])
cells.InsertNextCell(4, [6, 7, 11, 10])
cells.InsertNextCell(4, [9, 10, 14, 13])
cells.InsertNextCell(4, [0, 3, 15, 12])
pd.SetPolys(cells)

# Remove by cells
remove_1 = vtkRemovePolyData()
remove_1.AddInputConnection(plane.GetOutputPort())
remove_1.AddInputData(pd)
remove_1.Update()

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(remove_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Remove by point ids
pt_ids = vtkIdTypeArray()
pt_ids.SetNumberOfTuples(4)
pt_ids.SetTuple1(0, 0)
pt_ids.SetTuple1(1, 3)
pt_ids.SetTuple1(2, 12)
pt_ids.SetTuple1(3, 15)

remove_2 = vtkRemovePolyData()
remove_2.AddInputConnection(plane.GetOutputPort())
remove_2.SetPointIds(pt_ids)
remove_2.Update()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(remove_2.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Remove by cell ids
cell_ids = vtkIdTypeArray()
cell_ids.SetNumberOfTuples(1)
cell_ids.SetTuple1(0, 4)

remove_3 = vtkRemovePolyData()
remove_3.AddInputConnection(plane.GetOutputPort())
remove_3.SetCellIds(cell_ids)
remove_3.Update()

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(remove_3.GetOutputPort())

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

# Remove by combination (should produce nothing)
remove_4 = vtkRemovePolyData()
remove_4.AddInputConnection(plane.GetOutputPort())
remove_4.AddInputData(pd)
remove_4.SetCellIds(cell_ids)
remove_4.SetPointIds(pt_ids)
remove_4.Update()

mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(remove_4.GetOutputPort())

actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)

# Four renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.25, 1.0)
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.25, 0, 0.5, 1.0)
renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.5, 0, 0.75, 1.0)
renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.75, 0, 1.0, 1.0)

renderer_0.AddActor(actor_1)
renderer_1.AddActor(actor_2)
renderer_2.AddActor(actor_3)
renderer_3.AddActor(actor_4)

renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_2.SetBackground(0.1, 0.2, 0.4)
renderer_3.SetBackground(0.1, 0.2, 0.4)

renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_3.SetActiveCamera(renderer_0.GetActiveCamera())

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(600, 150)
render_window.SetWindowName("remove polydata by ids")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.GetActiveCamera().SetPosition(0, 0, 1)
renderer_0.ResetCamera()

interactor.Initialize()
interactor.Start()
