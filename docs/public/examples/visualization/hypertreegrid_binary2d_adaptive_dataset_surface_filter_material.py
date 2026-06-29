#!/usr/bin/env python
# Demonstrate vtkAdaptiveDataSetSurfaceFilter on a 2D binary HyperTreeGrid with material mask.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkHyperTreeGrid
from vtkmodules.vtkFiltersHybrid import vtkAdaptiveDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkHyperTreeGridSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkDataSetMapper,
    vtkMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# HyperTreeGrid source: 2D binary in XY plane with material mask
ht_grid = vtkHyperTreeGridSource()
ht_grid.SetMaxDepth(6)
ht_grid.SetDimensions(3, 4, 1)
ht_grid.SetGridScale(1.5, 1.0, 10.0)
ht_grid.SetBranchFactor(2)
ht_grid.UseMaskOn()
ht_grid.SetDescriptor(
    "RRRRR.|.... .R.. RRRR R... R...|.R.. ...R ..RR .R.. R... .... ....|.... "
    "...R ..R. .... .R.. R...|.... .... .R.. ....|...."
)
ht_grid.SetMask(
    "111111|0000 1111 1111 1111 1111|1111 0001 0111 0101 1011 1111 0111|1111 0111 "
    "1111 1111 1111 1111|1111 1111 1111 1111|1111"
)
ht_grid.Update()

htg = vtkHyperTreeGrid.SafeDownCast(ht_grid.GetOutput())
htg.GetCellData().SetScalars(htg.GetCellData().GetArray("Depth"))

# Adaptive surface filter
renderer = vtkRenderer()

surface = vtkAdaptiveDataSetSurfaceFilter()
surface.SetRenderer(renderer)
surface.SetInputConnection(ht_grid.GetOutputPort())
surface.SetViewPointDepend(False)
surface.Update()

pd = surface.GetOutput()
depth_range = pd.GetCellData().GetArray("Depth").GetRange()

# Mappers
vtkMapper.SetResolveCoincidentTopologyToPolygonOffset()

mapper_0 = vtkDataSetMapper()
mapper_0.SetInputConnection(surface.GetOutputPort())
mapper_0.SetScalarRange(depth_range)

mapper_1 = vtkDataSetMapper()
mapper_1.SetInputConnection(surface.GetOutputPort())
mapper_1.ScalarVisibilityOff()

# Actors
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetRepresentationToWireframe()
actor_1.GetProperty().SetColor(0.7, 0.7, 0.7)

# Camera
camera = vtkCamera()
center = pd.GetCenter()
camera.SetClippingRange(1.0, 100.0)
camera.SetFocalPoint(center[0] - 0.75, center[1], center[2])
camera.SetPosition(center[0] - 0.75, center[1], center[2] + 10.0)
camera.ParallelProjectionOn()
camera.SetParallelScale(1)

renderer.SetActiveCamera(camera)
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.SetWindowName("hypertreegrid binary2d adaptive dataset surface filter material")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

surface.SetViewPointDepend(True)
surface.Update()

interactor.Initialize()
interactor.Start()
