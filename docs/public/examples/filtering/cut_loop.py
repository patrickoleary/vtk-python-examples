#!/usr/bin/env python

# Select and clip a region on a sphere defined by a loop of points
# using vtkSelectPolyData and vtkClipPolyData.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersModeling import vtkSelectPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

colors = vtkNamedColors()
peacock = [0.0, 0.0, 0.0]
colors.GetColorRGB("peacock", peacock)

# Define loop points on the sphere surface
selection_points = vtkPoints()
selection_points.InsertPoint(0, -0.16553, 0.135971, 0.451972)
selection_points.InsertPoint(1, -0.0880123, -0.134952, 0.4747)
selection_points.InsertPoint(2, 0.00292618, -0.134604, 0.482459)
selection_points.InsertPoint(3, 0.0641941, 0.067112, 0.490947)
selection_points.InsertPoint(4, 0.15577, 0.0734765, 0.469245)
selection_points.InsertPoint(5, 0.166667, -0.129217, 0.454622)
selection_points.InsertPoint(6, 0.241259, -0.123363, 0.420581)
selection_points.InsertPoint(7, 0.240334, 0.0727106, 0.432555)
selection_points.InsertPoint(8, 0.308529, 0.0844311, 0.384357)
selection_points.InsertPoint(9, 0.32672, -0.121674, 0.359187)
selection_points.InsertPoint(10, 0.380721, -0.117342, 0.302527)
selection_points.InsertPoint(11, 0.387804, 0.0455074, 0.312375)
selection_points.InsertPoint(12, 0.43943, -0.111673, 0.211707)
selection_points.InsertPoint(13, 0.470984, -0.0801913, 0.147919)
selection_points.InsertPoint(14, 0.436777, 0.0688872, 0.233021)
selection_points.InsertPoint(15, 0.44874, 0.188852, 0.109882)
selection_points.InsertPoint(16, 0.391352, 0.254285, 0.176943)
selection_points.InsertPoint(17, 0.373274, 0.154162, 0.294296)
selection_points.InsertPoint(18, 0.274659, 0.311654, 0.276609)
selection_points.InsertPoint(19, 0.206068, 0.31396, 0.329702)
selection_points.InsertPoint(20, 0.263789, 0.174982, 0.387308)
selection_points.InsertPoint(21, 0.213034, 0.175485, 0.417142)
selection_points.InsertPoint(22, 0.169113, 0.261974, 0.390286)
selection_points.InsertPoint(23, 0.102552, 0.25997, 0.414814)
selection_points.InsertPoint(24, 0.131512, 0.161254, 0.454705)
selection_points.InsertPoint(25, 0.000192443, 0.156264, 0.475307)
selection_points.InsertPoint(26, -0.0392091, 0.000251724, 0.499943)
selection_points.InsertPoint(27, -0.096161, 0.159646, 0.46438)

# Source: half sphere
sphere = vtkSphereSource()
sphere.SetPhiResolution(50)
sphere.SetThetaResolution(100)
sphere.SetStartPhi(0)
sphere.SetEndPhi(90)

# Select region using loop and generate scalars
loop = vtkSelectPolyData()
loop.SetInputConnection(sphere.GetOutputPort())
loop.SetLoop(selection_points)
loop.GenerateSelectionScalarsOn()
loop.SetSelectionModeToSmallestRegion()

# Clip out the positive region
clip = vtkClipPolyData()
clip.SetInputConnection(loop.GetOutputPort())

clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(clip.GetOutputPort())

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)

# Select region without clipping (colored display)
loop2 = vtkSelectPolyData()
loop2.SetInputConnection(sphere.GetOutputPort())
loop2.SetLoop(selection_points)
loop2.SetSelectionModeToSmallestRegion()

select_mapper = vtkPolyDataMapper()
select_mapper.SetInputConnection(loop2.GetOutputPort())

select_actor = vtkActor()
select_actor.SetMapper(select_mapper)
select_actor.AddPosition(1, 0, 0)
select_actor.GetProperty().SetColor(peacock)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.AddActor(select_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(500, 250)
render_window.SetWindowName("cut loop")

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(0.236644, 11.8322)
camera.SetFocalPoint(0.542809, -0.0166201, 0.183931)
camera.SetPosition(1.65945, 0.364443, 2.29141)
camera.SetViewUp(-0.0746604, 0.986933, -0.14279)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
