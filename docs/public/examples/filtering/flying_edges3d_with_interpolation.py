#!/usr/bin/env python

# Generate a 3D iso-surface from a sampled sphere using vtkFlyingEdges3D
# with attribute interpolation, colored by a cylinder implicit function.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkCylinder,
    vtkDataObject,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D
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

# Source: sample a sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)

sample = vtkSampleFunction()
sample.SetImplicitFunction(sphere)
sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
sample.SetSampleDimensions(100, 100, 100)

# Add a cylinder implicit function as an additional attribute
cylinder = vtkCylinder()
cylinder.SetRadius(0.1)
cylinder.SetAxis(1, 1, 1)

attr = vtkSampleImplicitFunctionFilter()
attr.SetInputConnection(sample.GetOutputPort())
attr.SetImplicitFunction(cylinder)
attr.ComputeGradientsOn()
attr.Update()

# Flying edges 3D iso-surface with attribute interpolation
iso = vtkFlyingEdges3D()
iso.SetInputConnection(attr.GetOutputPort())
iso.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "scalars")
iso.SetValue(0, 0.25)
iso.ComputeNormalsOn()
iso.ComputeGradientsOn()
iso.ComputeScalarsOn()
iso.InterpolateAttributesOn()
iso.Update()

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOn()
iso_mapper.SetScalarModeToUsePointFieldData()
iso_mapper.SelectColorArray("Implicit scalars")
iso_mapper.SetScalarRange(0, 0.3)

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(1, 1, 1)
iso_actor.GetProperty().SetOpacity(1)

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
renderer.AddActor(iso_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("flying edges3d with interpolation")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
