#!/usr/bin/env python

# Demonstrate vtkTensorGlyph by generating a point-load tensor field,
# creating tensor ellipsoids from a sphere source, and rendering them
# with an outline and a cone indicating the load application point.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkTensorGlyph
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkSphereSource
from vtkmodules.vtkImagingHybrid import vtkPointLoad
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkLogLookupTable,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Generate tensor field from point load
pt_load = vtkPointLoad()
pt_load.SetLoadValue(100.0)
pt_load.SetSampleDimensions(6, 6, 6)
pt_load.ComputeEffectiveStressOn()
pt_load.SetModelBounds(-10, 10, -10, 10, -10, 10)

# Extract a plane of data for scalar range
plane = vtkImageDataGeometryFilter()
plane.SetInputConnection(pt_load.GetOutputPort())
plane.SetExtent(2, 2, 0, 99, 0, 99)
plane.Update()

# Generate tensor ellipsoids
sphere = vtkSphereSource()
sphere.SetThetaResolution(8)
sphere.SetPhiResolution(8)

ellipsoids = vtkTensorGlyph()
ellipsoids.SetInputConnection(pt_load.GetOutputPort())
ellipsoids.SetSourceConnection(sphere.GetOutputPort())
ellipsoids.SetScaleFactor(10)
ellipsoids.ClampScalingOn()

ellip_normals = vtkPolyDataNormals()
ellip_normals.SetInputConnection(ellipsoids.GetOutputPort())

# Log lookup table and mapper
lookup_table = vtkLogLookupTable()
lookup_table.SetHueRange(0.6667, 0.0)

ellip_mapper = vtkPolyDataMapper()
ellip_mapper.SetInputConnection(ellip_normals.GetOutputPort())
ellip_mapper.SetLookupTable(lookup_table)
ellip_mapper.SetScalarRange(plane.GetOutput().GetScalarRange())

ellip_actor = vtkActor()
ellip_actor.SetMapper(ellip_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(pt_load.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Cone indicating point of load application
cone_src = vtkConeSource()
cone_src.SetRadius(0.5)
cone_src.SetHeight(2)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_src.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetPosition(0, 0, 11)
cone_actor.RotateY(90)
cone_actor.GetProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ellip_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(cone_actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("ten ellip")

# Scene
camera = vtkCamera()
camera.SetFocalPoint(0.113766, -1.13665, -1.01919)
camera.SetPosition(-29.4886, -63.1488, 26.5807)
camera.SetViewAngle(24.4617)
camera.SetViewUp(0.17138, 0.331163, 0.927879)
camera.SetClippingRange(1, 100)
renderer.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
