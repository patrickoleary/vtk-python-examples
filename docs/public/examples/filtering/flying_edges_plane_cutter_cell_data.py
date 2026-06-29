#!/usr/bin/env python

# Cut a sampled sphere volume with a plane using vtkFlyingEdgesPlaneCutter,
# displaying interpolated point data and cell data in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdgesPlaneCutter,
    vtkPointDataToCellData,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 10

# Source: sample a sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)

sample = vtkSampleFunction()
sample.SetImplicitFunction(sphere)
sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.ComputeNormalsOff()
sample.Update()

# Convert point data to cell data
pd_to_cd = vtkPointDataToCellData()
pd_to_cd.SetInputConnection(sample.GetOutputPort())
pd_to_cd.PassPointDataOn()
pd_to_cd.Update()

# Cut plane
plane = vtkPlane()
plane.SetOrigin(-0.2, -0.2, -0.2)
plane.SetNormal(1, 1, 1)

# Plane cutter with attribute interpolation
cut = vtkFlyingEdgesPlaneCutter()
cut.SetInputConnection(pd_to_cd.GetOutputPort())
cut.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "scalars")
cut.SetPlane(plane)
cut.ComputeNormalsOff()
cut.InterpolateAttributesOn()
cut.Update()

# Point data display
cut_mapper = vtkPolyDataMapper()
cut_mapper.SetInputConnection(cut.GetOutputPort())

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)

# Cell data display
cell_cut_mapper = vtkPolyDataMapper()
cell_cut_mapper.SetInputConnection(cut.GetOutputPort())
cell_cut_mapper.SetScalarModeToUseCellData()

cell_cut_actor = vtkActor()
cell_cut_actor.SetMapper(cell_cut_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Two viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(0, 0, 0)
renderer_0.AddActor(outline_actor)
renderer_0.AddActor(cut_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0, 0, 0)
renderer_1.AddActor(outline_actor)
renderer_1.AddActor(cell_cut_actor)


# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 300)
render_window.SetWindowName("flying edges plane cutter cell data")

# Scene
renderer_1.ResetCamera()
renderer_0.SetActiveCamera(renderer_1.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
