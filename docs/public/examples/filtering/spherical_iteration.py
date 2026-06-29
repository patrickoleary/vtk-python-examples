#!/usr/bin/env python

# Demonstrate vtkSphericalPointIterator by iterating over a 2D point cloud
# in axis-sweep and spiral modes, displaying both in side-by-side viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import reference
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkSphericalPointIterator,
)
from vtkmodules.vtkFiltersPoints import vtkProjectPointsToPlane
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

res = 250
num_sweeps = 3

# Generate a random point cloud projected to the Z plane
ps = vtkPointSource()
ps.SetNumberOfPoints(res)
ps.SetCenter(0, 0, 0)
ps.SetRadius(10)

pc = vtkProjectPointsToPlane()
pc.SetInputConnection(ps.GetOutputPort())
pc.SetProjectionTypeToZPlane()
pc.Update()

# Create a spherical point iterator
XY_CW_AXES = 0
pcenter = [1, 2, 3]
piter = vtkSphericalPointIterator()
piter.SetDataSet(pc.GetOutput())
piter.SetAxes(XY_CW_AXES, 40)
piter.SetSortTypeToAscending()
piter.Initialize(pcenter)

# Axis sweep visualization data
pd = vtkPolyData()
pd.SetPoints(pc.GetOutput().GetPoints())
ca = vtkCellArray()
pd.SetVerts(ca)

axis_mapper = vtkPolyDataMapper()
axis_mapper.SetInputData(pd)

axis_actor = vtkActor()
axis_actor.SetMapper(axis_mapper)
axis_actor.GetProperty().SetColor(0.85, 0.85, 0.85)
axis_actor.GetProperty().SetPointSize(2)

# Spiral iteration visualization data
pd2 = vtkPolyData()
pd2.SetPoints(pc.GetOutput().GetPoints())
ca2 = vtkCellArray()
pd2.SetVerts(ca2)

spiral_mapper = vtkPolyDataMapper()
spiral_mapper.SetInputData(pd2)

spiral_actor = vtkActor()
spiral_actor.SetMapper(spiral_mapper)
spiral_actor.GetProperty().SetColor(0.85, 0.85, 0.85)
spiral_actor.GetProperty().SetPointSize(2)

# Point cloud background
pc_mapper = vtkPolyDataMapper()
pc_mapper.SetInputConnection(pc.GetOutputPort())

pc_actor = vtkActor()
pc_actor.SetMapper(pc_mapper)
pc_actor.GetProperty().SetColor(0.85, 0.5, 0.5)
pc_actor.GetProperty().SetPointSize(1)

# Two renderers side by side
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)

renderer_0.AddActor(axis_actor)
renderer_0.AddActor(pc_actor)
renderer_0.SetBackground(0, 0, 0)

renderer_1.AddActor(spiral_actor)
renderer_1.AddActor(pc_actor)
renderer_1.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(400, 200)
render_window.SetWindowName("spherical iteration")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_0.GetActiveCamera().SetPosition(0, 0, 1)
renderer_1.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_1.GetActiveCamera().SetPosition(0, 0, 1)
renderer_0.ResetCamera()
renderer_1.ResetCamera()

interactor.Initialize()
render_window.Render()

# Axis sweep: loop over all axes for lighthouse effect
npts = reference(0)
pts = reference((0,))
num_axes = piter.GetNumberOfAxes()

for sweeps in range(num_sweeps):
    for i in range(num_axes):
        piter.GetAxisPoints(i, npts, pts)
        ca.Reset()
        ca.InsertNextCell(npts)
        for j in range(npts):
            ca.InsertCellPoint(pts[j])
        pd.Modified()
        render_window.Render()

# Spiral out from the center
p_ids = [0]
ca.Reset()
piter.GoToFirstPoint()
while not piter.IsDoneWithTraversal():
    p_ids[0] = piter.GetCurrentPoint()
    ca2.InsertNextCell(1, p_ids)
    piter.GoToNextPoint()
    pd2.Modified()
    render_window.Render()

interactor.Start()
