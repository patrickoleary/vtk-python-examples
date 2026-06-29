#!/usr/bin/env python

# Test coincident topology offset for edges/vertices on cubes with different mappers.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet
from vtkmodules.vtkCommonExecutionModel import vtkTrivialProducer
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkLight,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Cube source
cube = vtkCubeSource()
rib = 1.0
cube.SetBounds(-rib / 2, rib / 2, -rib / 2, rib / 2, -rib / 2, rib / 2)
cube.SetCenter(0, 0, 0)
cube.Update()

# Rotate the cube
transform = vtkTransform()
transform.Identity()
transform.RotateX(45)
transform.RotateY(45)

transformer = vtkTransformPolyDataFilter()
transformer.SetInputConnection(cube.GetOutputPort())
transformer.SetTransform(transform)
transformer.Update()

# Multi-block for composite mapper
mbd = vtkMultiBlockDataSet()
mbd.SetNumberOfBlocks(1)
mbd.SetBlock(0, transformer.GetOutput())

source = vtkTrivialProducer()
source.SetOutput(mbd)

# Mappers
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(transformer.GetOutputPort())
poly_mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, 2)

mbd_mapper = vtkCompositePolyDataMapper()
mbd_mapper.SetInputConnection(source.GetOutputPort())
mbd_mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, 2)

# Property without lighting
p1 = vtkProperty()
p1.SetColor(1, 0, 0)
p1.LightingOff()
p1.SetAmbient(0.2)
p1.SetDiffuse(0.7)
p1.SetSpecular(0.4)
p1.SetSpecularPower(35)
p1.EdgeVisibilityOn()
p1.SetEdgeColor(1, 1, 1)
p1.VertexVisibilityOn()
p1.SetVertexColor(0, 1, 0)
p1.SetPointSize(4)

# Property with lighting
p2 = vtkProperty()
p2.DeepCopy(p1)
p2.LightingOn()

light = vtkLight()
light.SetPosition(1, 1, 1)

# Poly mapper — bottom (no lighting)
actor_poly_bot = vtkActor()
actor_poly_bot.SetMapper(poly_mapper)
actor_poly_bot.SetProperty(p1)

renderer_poly_bot = vtkRenderer()
renderer_poly_bot.AddActor(actor_poly_bot)
renderer_poly_bot.RemoveAllLights()
renderer_poly_bot.SetViewport(0, 0, 0.5, 0.5)

# Poly mapper — top (with lighting)
actor_poly_top = vtkActor()
actor_poly_top.SetMapper(poly_mapper)
actor_poly_top.SetProperty(p2)

renderer_poly_top = vtkRenderer()
renderer_poly_top.AddActor(actor_poly_top)
renderer_poly_top.RemoveAllLights()
renderer_poly_top.SetViewport(0, 0.5, 0.5, 1.0)

# Composite mapper — bottom (no lighting)
actor_mbd_bot = vtkActor()
actor_mbd_bot.SetMapper(mbd_mapper)
actor_mbd_bot.SetProperty(p1)

renderer_mbd_bot = vtkRenderer()
renderer_mbd_bot.AddActor(actor_mbd_bot)
renderer_mbd_bot.RemoveAllLights()
renderer_mbd_bot.SetViewport(0.5, 0, 1.0, 0.5)

# Composite mapper — top (with lighting)
actor_mbd_top = vtkActor()
actor_mbd_top.SetMapper(mbd_mapper)
actor_mbd_top.SetProperty(p2)

renderer_mbd_top = vtkRenderer()
renderer_mbd_top.AddActor(actor_mbd_top)
renderer_mbd_top.RemoveAllLights()
renderer_mbd_top.SetViewport(0.5, 0.5, 1.0, 1.0)

render_window = vtkRenderWindow()
render_window.SetSize(600, 400)
render_window.AddRenderer(renderer_poly_bot)
render_window.AddRenderer(renderer_poly_top)
render_window.AddRenderer(renderer_mbd_bot)
render_window.AddRenderer(renderer_mbd_top)
render_window.SetWindowName("topology resolution")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_poly_bot.AddLight(light)
renderer_poly_top.AddLight(light)
renderer_mbd_bot.AddLight(light)
renderer_mbd_top.AddLight(light)

interactor.Initialize()
interactor.Start()
