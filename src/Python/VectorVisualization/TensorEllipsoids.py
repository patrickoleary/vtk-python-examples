#!/usr/bin/env python

# Visualize stress tensors as ellipsoids using tensor glyphs with a Brewer color palette.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkPolyDataNormals,
    vtkTensorGlyph,
)
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkSphereSource,
)
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
red = (1.0, 0.0, 0.0)

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

# Source: sphere geometry for tensor ellipsoid glyphs
sphere = vtkSphereSource()
sphere.SetThetaResolution(8)
sphere.SetPhiResolution(8)

# Filter: tensor glyphs oriented and scaled by the stress tensor
tensor_ellipsoids = vtkTensorGlyph()
tensor_ellipsoids.SetInputConnection(pt_load.GetOutputPort())
tensor_ellipsoids.SetSourceConnection(sphere.GetOutputPort())
tensor_ellipsoids.SetScaleFactor(10)
tensor_ellipsoids.ClampScalingOn()

# Filter: compute normals for smooth shading
ellip_normals = vtkPolyDataNormals()
ellip_normals.SetInputConnection(tensor_ellipsoids.GetOutputPort())

# Lookup table: Brewer diverging spectral palette with logarithmic scaling
lut = vtkLookupTable()
color_series = vtkColorSeries()
color_series.SetNumberOfColors(8)
color_series.SetColorScheme(color_series.BREWER_DIVERGING_SPECTRAL_8)
lut.SetScaleToLog10()
color_series.BuildLookupTable(lut, color_series.ORDINAL)
lut.SetNanColor(1, 0, 0, 1)

# Mapper: map tensor ellipsoids to graphics primitives
tensor_mapper = vtkPolyDataMapper()
tensor_mapper.SetInputConnection(ellip_normals.GetOutputPort())
tensor_mapper.SetLookupTable(lut)
tensor_mapper.SetScalarRange(plane.GetOutput().GetScalarRange())

# Actor: display the tensor ellipsoids
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
cone_actor.GetProperty().SetColor(red)

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
render_window.SetWindowName("TensorEllipsoids")
render_window.SetSize(512, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
