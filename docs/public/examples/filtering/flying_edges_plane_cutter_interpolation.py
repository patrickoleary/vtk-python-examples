#!/usr/bin/env python

# Cut a sampled sphere volume with a plane using vtkFlyingEdgesPlaneCutter
# with attribute interpolation, displaying cylinder implicit scalars and
# hedgehog vectors.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkCylinder,
    vtkDataObject,
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdgesPlaneCutter,
    vtkHedgeHog,
    vtkMaskPoints,
)
from vtkmodules.vtkFiltersGeneral import vtkSampleImplicitFunctionFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 100

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

# Add cylinder implicit function as extra attribute
cylinder = vtkCylinder()
cylinder.SetRadius(0.1)
cylinder.SetAxis(1, 1, 1)

attr = vtkSampleImplicitFunctionFilter()
attr.SetInputConnection(sample.GetOutputPort())
attr.SetImplicitFunction(cylinder)
attr.ComputeGradientsOn()
attr.Update()

# Cut plane
plane = vtkPlane()
plane.SetOrigin(-0.2, -0.2, -0.2)
plane.SetNormal(1, 1, 1)

# Plane cutter with attribute interpolation
cut = vtkFlyingEdgesPlaneCutter()
cut.SetInputConnection(attr.GetOutputPort())
cut.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "scalars")
cut.SetPlane(plane)
cut.ComputeNormalsOff()
cut.InterpolateAttributesOn()
cut.Update()

# Mapper colored by implicit scalars
cut_mapper = vtkPolyDataMapper()
cut_mapper.SetInputConnection(cut.GetOutputPort())
cut_mapper.SetScalarModeToUsePointFieldData()
cut_mapper.SelectColorArray("Implicit scalars")

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)
cut_actor.GetProperty().SetColor(1, 1, 1)
cut_actor.GetProperty().SetOpacity(1)

# Hedgehog vectors from masked points
mask_pts = vtkMaskPoints()
mask_pts.SetOnRatio(25)
mask_pts.SetInputConnection(cut.GetOutputPort())

hedgehog = vtkHedgeHog()
hedgehog.SetInputConnection(mask_pts.GetOutputPort())
hedgehog.SetVectorModeToUseVector()
hedgehog.SetScaleFactor(0.05)

hedgehog_mapper = vtkPolyDataMapper()
hedgehog_mapper.SetInputConnection(hedgehog.GetOutputPort())

hedgehog_actor = vtkActor()
hedgehog_actor.SetMapper(hedgehog_mapper)
hedgehog_actor.GetProperty().SetColor(1, 1, 1)
hedgehog_actor.GetProperty().SetOpacity(1)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(cut_actor)
renderer.AddActor(hedgehog_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("flying edges plane cutter interpolation")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
