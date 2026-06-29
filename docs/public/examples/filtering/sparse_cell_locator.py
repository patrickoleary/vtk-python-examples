#!/usr/bin/env python

# Test vtkStaticCellLocator with sparsely populated data. Two inner spheres
# are colored by closest-point distance to an outer bounding sphere,
# producing a smooth mirror-symmetric distance function.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    reference,
    vtkDoubleArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkGenericCell,
    vtkStaticCellLocator,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

inner_sphere_res = 15
outer_sphere_res = 10
bin_res = 25

# Right inner sphere
right_inner_sphere = vtkSphereSource()
right_inner_sphere.SetCenter(2.5, 0, 0)
right_inner_sphere.SetRadius(2.5)
right_inner_sphere.SetPhiResolution(inner_sphere_res)
right_inner_sphere.SetThetaResolution(2 * inner_sphere_res)
right_inner_sphere.Update()
right_inner_pd = right_inner_sphere.GetOutput()

# Left inner sphere
left_inner_sphere = vtkSphereSource()
left_inner_sphere.SetCenter(-2.5, 0, 0)
left_inner_sphere.SetRadius(2.5)
left_inner_sphere.SetPhiResolution(inner_sphere_res)
left_inner_sphere.SetThetaResolution(2 * inner_sphere_res)
left_inner_sphere.Update()
left_inner_pd = left_inner_sphere.GetOutput()

# Outer bounding sphere
outer_sphere = vtkSphereSource()
outer_sphere.SetCenter(0.0, 0, 0)
outer_sphere.SetRadius(10)
outer_sphere.SetPhiResolution(outer_sphere_res)
outer_sphere.SetThetaResolution(2 * outer_sphere_res)
outer_sphere.Update()
outer_pd = outer_sphere.GetOutput()

# Build cell locator on the outer sphere
cell_loc = vtkStaticCellLocator()
cell_loc.SetDataSet(outer_pd)
cell_loc.SetNumberOfCellsPerNode(1)
cell_loc.BuildLocator()

# Compute closest-point distance from each inner sphere point to outer sphere
x = [0, 0, 0]
gen_cell = vtkGenericCell()
closest_pt = [0, 0, 0]
closest_cell_id = reference(-1)
sub_id = reference(0)
dist2 = reference(0.0)

num_inner_pts = right_inner_pd.GetNumberOfPoints()
right_inner_da = vtkDoubleArray()
right_inner_da.SetNumberOfTuples(num_inner_pts)
left_inner_da = vtkDoubleArray()
left_inner_da.SetNumberOfTuples(num_inner_pts)

for p_id in range(num_inner_pts):
    right_inner_pd.GetPoint(p_id, x)
    cell_loc.FindClosestPoint(x, closest_pt, gen_cell, closest_cell_id, sub_id, dist2)
    right_inner_da.SetTuple1(p_id, dist2)
    left_inner_pd.GetPoint(p_id, x)
    cell_loc.FindClosestPoint(x, closest_pt, gen_cell, closest_cell_id, sub_id, dist2)
    left_inner_da.SetTuple1(p_id, dist2)

right_inner_pd.GetPointData().SetScalars(right_inner_da)
left_inner_pd.GetPointData().SetScalars(left_inner_da)

# Display the inner spheres
right_inner_mapper = vtkPolyDataMapper()
right_inner_mapper.SetInputData(right_inner_pd)
right_inner_mapper.SetScalarRange(right_inner_da.GetRange())

right_inner_actor = vtkActor()
right_inner_actor.SetMapper(right_inner_mapper)

left_inner_mapper = vtkPolyDataMapper()
left_inner_mapper.SetInputData(left_inner_pd)
left_inner_mapper.SetScalarRange(left_inner_da.GetRange())

left_inner_actor = vtkActor()
left_inner_actor.SetMapper(left_inner_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(right_inner_actor)
renderer.AddActor(left_inner_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("sparse cell locator")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
