#!/usr/bin/env python

# Visualize stress tensors as scaled and oriented principal axes using tensor glyphs.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkTensorGlyph
from vtkmodules.vtkFiltersGeneral import vtkAxes
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkImagingHybrid import vtkPointLoad
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_smoke = (0.961, 0.961, 0.961)
black = (0.0, 0.0, 0.0)
burly_wood = (0.871, 0.722, 0.529)

# Source: generate a tensor field from a simulated point load
pt_load = vtkPointLoad()
pt_load.SetLoadValue(100.0)
pt_load.SetSampleDimensions(6, 6, 6)
pt_load.ComputeEffectiveStressOn()
pt_load.SetModelBounds(-10, 10, -10, 10, -10, 10)

# Filter: extract a plane for scalar range reference
plane = vtkImageDataGeometryFilter()
plane.SetInputConnection(pt_load.GetOutputPort())
plane.SetExtent(2, 2, 0, 99, 0, 99)
plane.Update()

# Source: axes geometry for tensor glyphs
axes = vtkAxes()
axes.SetScaleFactor(0.5)

# Filter: tensor glyphs oriented and scaled by the stress tensor
tensor_axes = vtkTensorGlyph()
tensor_axes.SetInputConnection(pt_load.GetOutputPort())
tensor_axes.SetSourceConnection(axes.GetOutputPort())
tensor_axes.SetScaleFactor(10)
tensor_axes.ClampScalingOn()

# Lookup table: logarithmic color mapping
lut = vtkLookupTable()
lut.SetScaleToLog10()
lut.SetHueRange(0.6667, 0.0)
lut.Build()

# Mapper: map tensor axes to graphics primitives
tensor_mapper = vtkPolyDataMapper()
tensor_mapper.SetInputConnection(tensor_axes.GetOutputPort())
tensor_mapper.SetLookupTable(lut)
tensor_mapper.SetScalarRange(plane.GetOutput().GetScalarRange())

# Actor: display the tensor axes
tensor_actor = vtkActor()
tensor_actor.SetMapper(tensor_mapper)

# Filter: outline around the data volume
outline = vtkOutlineFilter()
outline.SetInputConnection(pt_load.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

# Source: cone indicating the application of the load
cone_source = vtkConeSource()
cone_source.SetRadius(0.5)
cone_source.SetHeight(2)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetPosition(0, 0, 11)
cone_actor.RotateY(90)
cone_actor.GetProperty().SetColor(burly_wood)

# Camera: configure the viewpoint
camera = vtkCamera()
camera.SetFocalPoint(0.113766, -1.13665, -1.01919)
camera.SetPosition(-29.4886, -63.1488, 26.5807)
camera.SetViewAngle(24.4617)
camera.SetViewUp(0.17138, 0.331163, 0.927879)
camera.SetClippingRange(1, 100)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(tensor_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(cone_actor)
renderer.SetBackground(white_smoke)
renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("TensorAxes")
render_window.SetSize(512, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
