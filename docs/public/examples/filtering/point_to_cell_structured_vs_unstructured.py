#!/usr/bin/env python

# Convert point data to cell data on both structured and unstructured grids
# using vtkPointDataToCellData, displayed in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import (
    vtkPointDataToCellData,
    vtkSimpleElevationFilter,
    vtkThreshold,
)
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 50

# Source: image volume with elevation scalars
image_volume = vtkImageData()
image_volume.SetDimensions(resolution, resolution, resolution)

elevation = vtkSimpleElevationFilter()
elevation.SetInputData(image_volume)
elevation.Update()

# Convert point data to cell data (structured)
pd_to_cd = vtkPointDataToCellData()
pd_to_cd.SetInputConnection(elevation.GetOutputPort())
pd_to_cd.SetCategoricalData(0)
pd_to_cd.Update()

# Convert to unstructured grid via threshold
extract = vtkThreshold()
extract.SetInputConnection(elevation.GetOutputPort())
extract.SetThresholdFunction(vtkThreshold.THRESHOLD_BETWEEN)
extract.SetLowerThreshold(-10000.0)
extract.SetUpperThreshold(10000.0)
extract.Update()

# Convert point data to cell data (unstructured)
pd_to_cd_2 = vtkPointDataToCellData()
pd_to_cd_2.SetInputData(extract.GetOutput())
pd_to_cd_2.SetCategoricalData(0)
pd_to_cd_2.Update()

scalar_range = pd_to_cd.GetOutput().GetCellData().GetScalars().GetRange()

# Geometry for structured result
geom = vtkGeometryFilter()
geom.SetInputConnection(pd_to_cd.GetOutputPort())

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(geom.GetOutputPort())
mapper_0.SetScalarRange(scalar_range)

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

# Geometry for unstructured result
geom_2 = vtkGeometryFilter()
geom_2.SetInputConnection(pd_to_cd_2.GetOutputPort())

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(geom_2.GetOutputPort())
mapper_1.SetScalarRange(scalar_range)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Two viewports with shared camera
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(0, 0, 0)
renderer_0.AddActor(actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0, 0, 0)
renderer_1.AddActor(actor_1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 300)
render_window.SetWindowName("point to cell structured vs unstructured")

# Scene
renderer_0.GetActiveCamera().SetPosition(1, 0, 0)
renderer_0.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().Zoom(1.25)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
