#!/usr/bin/env python

# Display pre-defined vtkSphericalPointIterator axes sets: XY_CW, XY_CCW,
# XY_SQUARE, CUBE, OCTAHEDRON, CUBE_OCTAHEDRON, DODECAHEDRON, ICOSAHEDRON.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkSphericalPointIterator,
)
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Generate a random point cloud as placeholder
ps = vtkPointSource()
ps.SetNumberOfPoints(100)
ps.SetCenter(0, 0, 0)
ps.SetRadius(10)
ps.Update()

# XY_CW_AXES (0)
XY_CW_AXES = 0
pd_0 = vtkPolyData()
piter_0 = vtkSphericalPointIterator()
piter_0.SetDataSet(ps.GetOutput())
piter_0.SetAxes(XY_CW_AXES, 6)
piter_0.SetSortTypeToNone()
piter_0.Initialize([0, 0, 0])
piter_0.BuildRepresentation(pd_0)

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputData(pd_0)

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetColor(0.85, 0.85, 0.85)
actor_0.GetProperty().SetLineWidth(2)

# XY_CCW_AXES (1)
XY_CCW_AXES = 1
pd_1 = vtkPolyData()
piter_1 = vtkSphericalPointIterator()
piter_1.SetDataSet(ps.GetOutput())
piter_1.SetAxes(XY_CCW_AXES, 6)
piter_1.SetSortTypeToNone()
piter_1.Initialize([2.5, 0, 0])
piter_1.BuildRepresentation(pd_1)

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputData(pd_1)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetColor(0.85, 0.85, 0.85)
actor_1.GetProperty().SetLineWidth(2)

# XY_SQUARE_AXES (2)
XY_SQUARE_AXES = 2
pd_2 = vtkPolyData()
piter_2 = vtkSphericalPointIterator()
piter_2.SetDataSet(ps.GetOutput())
piter_2.SetAxes(XY_SQUARE_AXES)
piter_2.SetSortTypeToNone()
piter_2.Initialize([5, 0, 0])
piter_2.BuildRepresentation(pd_2)

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputData(pd_2)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetColor(0.85, 0.85, 0.85)
actor_2.GetProperty().SetLineWidth(2)

# CUBE_AXES (3)
CUBE_AXES = 3
pd_3 = vtkPolyData()
piter_3 = vtkSphericalPointIterator()
piter_3.SetDataSet(ps.GetOutput())
piter_3.SetAxes(CUBE_AXES)
piter_3.SetSortTypeToNone()
piter_3.Initialize([7.5, 0, 0])
piter_3.BuildRepresentation(pd_3)

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputData(pd_3)

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetColor(0.85, 0.85, 0.85)
actor_3.GetProperty().SetLineWidth(2)

# OCTAHEDRON_AXES (4)
OCTAHEDRON_AXES = 4
pd_4 = vtkPolyData()
piter_4 = vtkSphericalPointIterator()
piter_4.SetDataSet(ps.GetOutput())
piter_4.SetAxes(OCTAHEDRON_AXES)
piter_4.SetSortTypeToNone()
piter_4.Initialize([0, 2.5, 0])
piter_4.BuildRepresentation(pd_4)

mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputData(pd_4)

actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
actor_4.GetProperty().SetColor(0.85, 0.85, 0.85)
actor_4.GetProperty().SetLineWidth(2)

# CUBE_OCTAHEDRON_AXES (5)
CUBE_OCTAHEDRON_AXES = 5
pd_5 = vtkPolyData()
piter_5 = vtkSphericalPointIterator()
piter_5.SetDataSet(ps.GetOutput())
piter_5.SetAxes(CUBE_OCTAHEDRON_AXES)
piter_5.SetSortTypeToNone()
piter_5.Initialize([2.5, 2.5, 0])
piter_5.BuildRepresentation(pd_5)

mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputData(pd_5)

actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)
actor_5.GetProperty().SetColor(0.85, 0.85, 0.85)
actor_5.GetProperty().SetLineWidth(2)

# DODECAHEDRON_AXES (6)
DODECAHEDRON_AXES = 6
pd_6 = vtkPolyData()
piter_6 = vtkSphericalPointIterator()
piter_6.SetDataSet(ps.GetOutput())
piter_6.SetAxes(DODECAHEDRON_AXES)
piter_6.SetSortTypeToNone()
piter_6.Initialize([5, 2.5, 0])
piter_6.BuildRepresentation(pd_6)

mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputData(pd_6)

actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)
actor_6.GetProperty().SetColor(0.85, 0.85, 0.85)
actor_6.GetProperty().SetLineWidth(2)

# ICOSAHEDRON_AXES (7)
ICOSAHEDRON_AXES = 7
pd_7 = vtkPolyData()
piter_7 = vtkSphericalPointIterator()
piter_7.SetDataSet(ps.GetOutput())
piter_7.SetAxes(ICOSAHEDRON_AXES)
piter_7.SetSortTypeToNone()
piter_7.Initialize([7.5, 2.5, 0])
piter_7.BuildRepresentation(pd_7)

mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputData(pd_7)

actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)
actor_7.GetProperty().SetColor(0.85, 0.85, 0.85)
actor_7.GetProperty().SetLineWidth(2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(actor_5)
renderer.AddActor(actor_6)
renderer.AddActor(actor_7)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 200)
render_window.SetWindowName("spherical iterator sets")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetFocalPoint(1.25, 3.75, 0)
renderer.GetActiveCamera().SetPosition(1.45, 3.85, 0.4)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.65)

interactor.Initialize()
interactor.Start()
