#!/usr/bin/env python

# Demonstrate vtkReverseSense by clipping a cow, reflecting it, and
# reversing the normals so the reflected half renders correctly.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkClipPolyData,
    vtkPolyDataNormals,
    vtkReverseSense,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

named_colors = vtkNamedColors()
flesh_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("flesh", flesh_rgb)

# Read the cow model
cow_reader = vtkOBJReader()
cow_reader.SetFileName(os.path.join(data_dir, "Viewpoint", "cow.obj"))

# Clip by the x=0 plane
plane = vtkPlane()
plane.SetNormal(1, 0, 0)

cow_clipper = vtkClipPolyData()
cow_clipper.SetInputConnection(cow_reader.GetOutputPort())
cow_clipper.SetClipFunction(plane)

# Compute normals on the clipped half
cell_normals = vtkPolyDataNormals()
cell_normals.SetInputConnection(cow_clipper.GetOutputPort())
cell_normals.ComputePointNormalsOn()
cell_normals.ComputeCellNormalsOn()

# Reflect across x
reflect = vtkTransform()
reflect.Scale(-1, 1, 1)

cow_reflect = vtkTransformPolyDataFilter()
cow_reflect.SetTransform(reflect)
cow_reflect.SetInputConnection(cell_normals.GetOutputPort())

# Reverse the normals so reflected geometry renders correctly
cow_reverse = vtkReverseSense()
cow_reverse.SetInputConnection(cow_reflect.GetOutputPort())
cow_reverse.ReverseNormalsOn()
cow_reverse.ReverseCellsOff()

# Reflected half actor
reflected_mapper = vtkPolyDataMapper()
reflected_mapper.SetInputConnection(cow_reverse.GetOutputPort())

reflected_actor = vtkActor()
reflected_actor.SetMapper(reflected_mapper)
reflected_actor.GetProperty().SetDiffuseColor(flesh_rgb)
reflected_actor.GetProperty().SetDiffuse(0.8)
reflected_actor.GetProperty().SetSpecular(0.5)
reflected_actor.GetProperty().SetSpecularPower(30)
reflected_actor.GetProperty().FrontfaceCullingOn()

# Original clipped half actor
cow_mapper = vtkPolyDataMapper()
cow_mapper.SetInputConnection(cow_clipper.GetOutputPort())

cow_actor = vtkActor()
cow_actor.SetMapper(cow_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(reflected_actor)
renderer.AddActor(cow_actor)
renderer.SetBackground(0.1, 0.2, 0.4)
# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(320, 240)
render_window.SetWindowName("reverse normals")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().Azimuth(180)
renderer.GetActiveCamera().Dolly(1.75)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
