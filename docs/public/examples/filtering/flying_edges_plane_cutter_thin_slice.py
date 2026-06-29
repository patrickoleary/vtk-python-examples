#!/usr/bin/env python

# Cut a minimal single-voxel volume with a plane using
# vtkFlyingEdgesPlaneCutter with attribute interpolation.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPlane,
)
from vtkmodules.vtkFiltersCore import vtkFlyingEdgesPlaneCutter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a 2x2x2 image (single voxel) with scalar values 0-7
image = vtkImageData()
image.SetDimensions(2, 2, 2)
image.AllocateScalars(10, 1)

scalars = image.GetPointData().GetScalars()
scalars.InsertTuple1(0, 0.0)
scalars.InsertTuple1(1, 1.0)
scalars.InsertTuple1(2, 2.0)
scalars.InsertTuple1(3, 3.0)
scalars.InsertTuple1(4, 4.0)
scalars.InsertTuple1(5, 5.0)
scalars.InsertTuple1(6, 6.0)
scalars.InsertTuple1(7, 7.0)

# Cut plane
plane = vtkPlane()
plane.SetOrigin(0.5, 0.5, 0.5)
plane.SetNormal(1, 1, 1)

# Plane cutter with attribute interpolation
iso = vtkFlyingEdgesPlaneCutter()
iso.SetInputData(image)
iso.InterpolateAttributesOn()
iso.SetPlane(plane)
iso.Update()

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.SetScalarRange(iso.GetOutput().GetPointData().GetScalars().GetRange())

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(1, 0, 0)
iso_actor.GetProperty().SetOpacity(1)

# Outline
outline = vtkOutlineFilter()
outline.SetInputData(image)

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
render_window.SetSize(400, 400)
render_window.SetWindowName("flying edges plane cutter thin slice")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
