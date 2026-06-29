#!/usr/bin/env python

# Demonstrate vtkDecimatePro on a bumpy plane with four combinations
# of BoundaryVertexDeletion and AccumulateError, displayed in a 2x2
# grid of viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersCore import (
    vtkDecimatePro,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersProgrammable import vtkProgrammableFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a plane with a couple of bumps
plane = vtkPlaneSource()
plane.SetXResolution(10)
plane.SetYResolution(10)

tf = vtkTriangleFilter()
tf.SetInputConnection(plane.GetOutputPort())
tf.Update()

# Programmable filter to adjust point heights
adjust_points = vtkProgrammableFilter()
adjust_points.SetInputConnection(tf.GetOutputPort())


def adjust_points_proc():
    inp = adjust_points.GetPolyDataInput()
    in_pts = inp.GetPoints()
    new_pts = vtkPoints()
    new_pts.DeepCopy(in_pts)

    pt = inp.GetPoint(17)
    new_pts.SetPoint(17, pt[0], pt[1], 0.25)
    pt = in_pts.GetPoint(50)
    new_pts.SetPoint(50, pt[0], pt[1], 1.0)
    pt = in_pts.GetPoint(77)
    new_pts.SetPoint(77, pt[0], pt[1], 0.125)

    adjust_points.GetPolyDataOutput().CopyStructure(inp)
    adjust_points.GetPolyDataOutput().SetPoints(new_pts)


adjust_points.SetExecuteMethod(adjust_points_proc)

# Remove the extreme peak in the center with extent clipping
gf = vtkGeometryFilter()
gf.SetInputConnection(adjust_points.GetOutputPort())
gf.ExtentClippingOn()
gf.SetExtent(-100, 100, -100, 100, -1, 0.9)

# Four combinations of boundary vertex deletion and accumulate error.

# BoundaryVertexDeletion=On, AccumulateError=On.
deci_on_on = vtkDecimatePro()
deci_on_on.SetInputConnection(gf.GetOutputPort())
deci_on_on.SetTargetReduction(0.95)
deci_on_on.BoundaryVertexDeletionOn()
deci_on_on.AccumulateErrorOn()
mapper_on_on = vtkPolyDataMapper()
mapper_on_on.SetInputConnection(deci_on_on.GetOutputPort())
plane_actor_on_on = vtkActor()
plane_actor_on_on.SetMapper(mapper_on_on)

# BoundaryVertexDeletion=On, AccumulateError=Off.
deci_on_off = vtkDecimatePro()
deci_on_off.SetInputConnection(gf.GetOutputPort())
deci_on_off.SetTargetReduction(0.95)
deci_on_off.BoundaryVertexDeletionOn()
deci_on_off.AccumulateErrorOff()
mapper_on_off = vtkPolyDataMapper()
mapper_on_off.SetInputConnection(deci_on_off.GetOutputPort())
plane_actor_on_off = vtkActor()
plane_actor_on_off.SetMapper(mapper_on_off)

# BoundaryVertexDeletion=Off, AccumulateError=On.
deci_off_on = vtkDecimatePro()
deci_off_on.SetInputConnection(gf.GetOutputPort())
deci_off_on.SetTargetReduction(0.95)
deci_off_on.BoundaryVertexDeletionOff()
deci_off_on.AccumulateErrorOn()
mapper_off_on = vtkPolyDataMapper()
mapper_off_on.SetInputConnection(deci_off_on.GetOutputPort())
plane_actor_off_on = vtkActor()
plane_actor_off_on.SetMapper(mapper_off_on)

# BoundaryVertexDeletion=Off, AccumulateError=Off.
deci_off_off = vtkDecimatePro()
deci_off_off.SetInputConnection(gf.GetOutputPort())
deci_off_off.SetTargetReduction(0.95)
deci_off_off.BoundaryVertexDeletionOff()
deci_off_off.AccumulateErrorOff()
mapper_off_off = vtkPolyDataMapper()
mapper_off_off.SetInputConnection(deci_off_off.GetOutputPort())
plane_actor_off_off = vtkActor()
plane_actor_off_off.SetMapper(mapper_off_off)

# Four renderers in 2x2 layout
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0.5, 0.5, 1)
renderer_0.AddActor(plane_actor_on_on)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.5, 1, 1)
renderer_1.AddActor(plane_actor_on_off)
renderer_1.SetBackground(0, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0, 0, 0.5, 0.5)
renderer_2.AddActor(plane_actor_off_on)
renderer_2.SetBackground(0, 0, 0)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0, 1, 0.5)
renderer_3.AddActor(plane_actor_off_off)
renderer_3.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(500, 500)
render_window.SetWindowName("deci plane")

# Scene
camera = vtkCamera()
camera.SetPosition(-0.128224, 0.611836, 2.31297)
camera.SetFocalPoint(0, 0, 0.125)
camera.SetViewAngle(30)
camera.SetViewUp(0.162675, 0.952658, -0.256864)

renderer_0.SetActiveCamera(camera)
renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)
renderer_3.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
