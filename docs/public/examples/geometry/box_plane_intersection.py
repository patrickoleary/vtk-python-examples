#!/usr/bin/env python
# Demonstrate vtkBox IntersectWithPlane on three cubes with different plane orientations.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkBox, vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create three cubes.
box_l = vtkCubeSource()
box_l.SetBounds(-2.5, -1.5, -0.5, 0.5, -0.5, 0.5)
box_c = vtkCubeSource()
box_c.SetBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
box_r = vtkCubeSource()
box_r.SetBounds(1.5, 2.5, -0.5, 0.5, -0.5, 0.5)

box_l_mapper = vtkPolyDataMapper()
box_l_mapper.SetInputConnection(box_l.GetOutputPort())
box_l_actor = vtkActor()
box_l_actor.SetMapper(box_l_mapper)
box_l_actor.GetProperty().SetRepresentationToWireframe()
box_l_actor.GetProperty().SetAmbient(1)

box_c_mapper = vtkPolyDataMapper()
box_c_mapper.SetInputConnection(box_c.GetOutputPort())
box_c_actor = vtkActor()
box_c_actor.SetMapper(box_c_mapper)
box_c_actor.GetProperty().SetRepresentationToWireframe()
box_c_actor.GetProperty().SetAmbient(1)

box_r_mapper = vtkPolyDataMapper()
box_r_mapper.SetInputConnection(box_r.GetOutputPort())
box_r_actor = vtkActor()
box_r_actor.SetMapper(box_r_mapper)
box_r_actor.GetProperty().SetRepresentationToWireframe()
box_r_actor.GetProperty().SetAmbient(1)

xout = [0.0] * 18
bds = [0.0] * 6
clip_box = vtkBox()

# Left: normal = [1, 1, 1].
normal = [1, 1, 1]
origin = list(box_l.GetCenter())
box_l.GetBounds(bds)
num_ints = clip_box.IntersectWithPlane(bds, origin, normal, xout)
pts_l = vtkPoints()
pts_l.SetDataTypeToDouble()
pts_l.SetNumberOfPoints(num_ints)
poly_l = vtkCellArray()
poly_l.InsertNextCell(num_ints)
for i in range(num_ints):
    pts_l.SetPoint(i, xout[3 * i], xout[3 * i + 1], xout[3 * i + 2])
    poly_l.InsertCellPoint(i)
pd_l = vtkPolyData()
pd_l.SetPoints(pts_l)
pd_l.SetPolys(poly_l)
mapper_pl = vtkPolyDataMapper()
mapper_pl.SetInputData(pd_l)
actor_pl = vtkActor()
actor_pl.SetMapper(mapper_pl)

# Center: normal = [0.4, 0.8, 0.4].
normal = [0.4, 0.8, 0.4]
origin = list(box_c.GetCenter())
box_c.GetBounds(bds)
num_ints = clip_box.IntersectWithPlane(bds, origin, normal, xout)
pts_c = vtkPoints()
pts_c.SetDataTypeToDouble()
pts_c.SetNumberOfPoints(num_ints)
poly_c = vtkCellArray()
poly_c.InsertNextCell(num_ints)
for i in range(num_ints):
    pts_c.SetPoint(i, xout[3 * i], xout[3 * i + 1], xout[3 * i + 2])
    poly_c.InsertCellPoint(i)
pd_c = vtkPolyData()
pd_c.SetPoints(pts_c)
pd_c.SetPolys(poly_c)
mapper_pc = vtkPolyDataMapper()
mapper_pc.SetInputData(pd_c)
actor_pc = vtkActor()
actor_pc.SetMapper(mapper_pc)

# Right: normal = [0, 0, 1].
normal = [0, 0, 1]
origin = list(box_r.GetCenter())
box_r.GetBounds(bds)
num_ints = clip_box.IntersectWithPlane(bds, origin, normal, xout)
pts_r = vtkPoints()
pts_r.SetDataTypeToDouble()
pts_r.SetNumberOfPoints(num_ints)
poly_r = vtkCellArray()
poly_r.InsertNextCell(num_ints)
for i in range(num_ints):
    pts_r.SetPoint(i, xout[3 * i], xout[3 * i + 1], xout[3 * i + 2])
    poly_r.InsertCellPoint(i)
pd_r = vtkPolyData()
pd_r.SetPoints(pts_r)
pd_r.SetPolys(poly_r)
mapper_pr = vtkPolyDataMapper()
mapper_pr.SetInputData(pd_r)
actor_pr = vtkActor()
actor_pr.SetMapper(mapper_pr)
renderer = vtkRenderer()
renderer.AddActor(box_l_actor)
renderer.AddActor(box_c_actor)
renderer.AddActor(box_r_actor)
renderer.AddActor(actor_pl)
renderer.AddActor(actor_pc)
renderer.AddActor(actor_pr)

render_window = vtkRenderWindow()
render_window.SetSize(600, 200)
render_window.AddRenderer(renderer)
render_window.SetWindowName("box plane intersection")

renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetPosition(0, 0.5, 1)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.5)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
