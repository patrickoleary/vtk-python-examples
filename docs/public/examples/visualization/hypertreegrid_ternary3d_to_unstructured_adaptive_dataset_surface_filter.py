#!/usr/bin/env python
# Demonstrate vtkAdaptiveDataSetSurfaceFilter on a 3D ternary HyperTreeGrid converted to unstructured grid.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkHyperTreeGrid
from vtkmodules.vtkFiltersHybrid import vtkAdaptiveDataSetSurfaceFilter
from vtkmodules.vtkFiltersHyperTree import vtkHyperTreeGridToUnstructuredGrid
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

# HyperTreeGrid source: 3D ternary
ht_grid = vtkHyperTreeGridSource()
ht_grid.SetMaxDepth(5)
ht_grid.SetDimensions(4, 4, 3)
ht_grid.SetGridScale(1.5, 1.0, 0.7)
ht_grid.SetBranchFactor(3)
ht_grid.SetDescriptor(
    "RRR .R. .RR ..R ..R .R.|R.......................... ........................... "
    "........................... .............R............. ....RR.RR........R......... "
    ".....RRRR.....R.RR......... ........................... ........................... "
    "...........................|........................... ........................... "
    "........................... ...RR.RR.......RR.......... ........................... "
    "RR......................... ........................... ........................... "
    "........................... ........................... ........................... "
    "........................... ........................... "
    "............RRR............|........................... ........................... "
    ".......RR.................. ........................... ........................... "
    "........................... ........................... ........................... "
    "........................... ........................... "
    "...........................|........................... ..........................."
)
ht_grid.Update()

htg = vtkHyperTreeGrid.SafeDownCast(ht_grid.GetOutput())
htg.GetCellData().SetScalars(htg.GetCellData().GetArray("Depth"))

# Convert to unstructured grid
htg2ug = vtkHyperTreeGridToUnstructuredGrid()
htg2ug.SetInputConnection(ht_grid.GetOutputPort())

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
bd = [0.0] * 6
pd.GetBounds(bd)
camera = vtkCamera()
camera.SetClippingRange(1.0, 100.0)
camera.SetFocalPoint(pd.GetCenter())
camera.SetPosition(-0.8 * bd[1], 2.1 * bd[3], -4.8 * bd[5])

renderer.SetActiveCamera(camera)
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.SetWindowName("hypertreegrid ternary3d to unstructured adaptive dataset surface filter")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

surface.SetViewPointDepend(True)
surface.Update()

interactor.Initialize()
interactor.Start()
