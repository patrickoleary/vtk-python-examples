#!/usr/bin/env python

# Clip multiple spheres with a plane using vtkPolyDataPlaneClipper,
# testing point data, cell data, and multiple capping loops.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkPointDataToCellData,
    vtkPolyDataPlaneClipper,
    vtkSimpleElevationFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 512

# Sphere 1 with point data (elevation)
sphere_1 = vtkSphereSource()
sphere_1.SetCenter(0.0, 0.0, 0.0)
sphere_1.SetRadius(0.25)
sphere_1.SetThetaResolution(2 * resolution)
sphere_1.SetPhiResolution(resolution)
sphere_1.Update()

elevation_1 = vtkSimpleElevationFilter()
elevation_1.SetInputConnection(sphere_1.GetOutputPort())

# Sphere 2 and 3 appended with cell data
sphere_2 = vtkSphereSource()
sphere_2.SetCenter(0.875, 0.0, 0.0)
sphere_2.SetRadius(0.35)
sphere_2.SetThetaResolution(2 * resolution)
sphere_2.SetPhiResolution(resolution)
sphere_2.Update()

sphere_3 = vtkSphereSource()
sphere_3.SetCenter(2.0, 0.0, 0.0)
sphere_3.SetRadius(0.5)
sphere_3.SetThetaResolution(2 * resolution)
sphere_3.SetPhiResolution(resolution)
sphere_3.Update()

append = vtkAppendPolyData()
append.AddInputConnection(sphere_2.GetOutputPort())
append.AddInputConnection(sphere_3.GetOutputPort())

elevation_2 = vtkSimpleElevationFilter()
elevation_2.SetInputConnection(append.GetOutputPort())

pd_to_cd = vtkPointDataToCellData()
pd_to_cd.SetInputConnection(elevation_2.GetOutputPort())
pd_to_cd.ProcessAllArraysOff()
pd_to_cd.AddPointDataArray("Elevation")
pd_to_cd.Update()

# Cut plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(0, 0, -1)

# Clipper 1: single sphere with point data
clipper_1 = vtkPolyDataPlaneClipper()
clipper_1.SetInputConnection(elevation_1.GetOutputPort())
clipper_1.SetPlane(plane)
clipper_1.SetBatchSize(10000)
clipper_1.CappingOn()
clipper_1.Update()

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(clipper_1.GetOutputPort())
mapper_1.SetScalarRange(clipper_1.GetOutput().GetPointData().GetScalars().GetRange())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

cap_mapper_1 = vtkPolyDataMapper()
cap_mapper_1.SetInputConnection(clipper_1.GetOutputPort(1))

cap_actor_1 = vtkActor()
cap_actor_1.SetMapper(cap_mapper_1)
cap_actor_1.GetProperty().SetColor(1, 0, 0)

# Clipper 2: appended spheres with cell data
clipper_2 = vtkPolyDataPlaneClipper()
clipper_2.SetInputConnection(pd_to_cd.GetOutputPort())
clipper_2.SetPlane(plane)
clipper_2.SetBatchSize(10000)
clipper_2.ClippingLoopsOff()
clipper_2.CappingOn()
clipper_2.Update()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(clipper_2.GetOutputPort())
mapper_2.SetScalarModeToUseCellFieldData()
mapper_2.SelectColorArray("Elevation")
mapper_2.SetScalarRange(clipper_2.GetOutput().GetCellData().GetArray("Elevation").GetRange())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

cap_mapper_2 = vtkPolyDataMapper()
cap_mapper_2.SetInputConnection(clipper_2.GetOutputPort(1))

cap_actor_2 = vtkActor()
cap_actor_2.SetMapper(cap_mapper_2)
cap_actor_2.GetProperty().SetColor(0, 1, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_1)
renderer.AddActor(cap_actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(cap_actor_2)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("plane clip spheres with capping")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(1, 1, 1)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
