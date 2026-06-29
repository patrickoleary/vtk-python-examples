#!/usr/bin/env python

# Demonstrate vtkThresholdTextureCoords on PLOT3D blunt fin data
# with three threshold modes: upper, lower, and between.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkFiltersTexture import vtkThresholdTextureCoords
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read PLOT3D blunt fin data
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
output = plot3d_reader.GetOutput().GetBlock(0)

# Wall geometry
wall = vtkStructuredGridGeometryFilter()
wall.SetInputData(output)
wall.SetExtent(0, 100, 0, 0, 0, 100)

wall_map = vtkPolyDataMapper()
wall_map.SetInputConnection(wall.GetOutputPort())
wall_map.ScalarVisibilityOff()

wall_actor = vtkActor()
wall_actor.SetMapper(wall_map)
wall_actor.GetProperty().SetColor(0.8, 0.8, 0.8)

# Fin geometry
fin = vtkStructuredGridGeometryFilter()
fin.SetInputData(output)
fin.SetExtent(0, 100, 0, 100, 0, 0)

fin_map = vtkPolyDataMapper()
fin_map.SetInputConnection(fin.GetOutputPort())
fin_map.ScalarVisibilityOff()

fin_actor = vtkActor()
fin_actor.SetMapper(fin_map)
fin_actor.GetProperty().SetColor(0.8, 0.8, 0.8)

# Texture for threshold visualization
tmap = vtkStructuredPointsReader()
tmap.SetFileName(os.path.join(data_dir, "texThres2.vtk"))

texture = vtkTexture()
texture.SetInputConnection(tmap.GetOutputPort())
texture.InterpolateOff()
texture.RepeatOff()

# Plane 1: threshold by upper
plane_1 = vtkStructuredGridGeometryFilter()
plane_1.SetInputData(output)
plane_1.SetExtent(10, 10, 0, 100, 0, 100)

thresh_1 = vtkThresholdTextureCoords()
thresh_1.SetInputConnection(plane_1.GetOutputPort())
thresh_1.ThresholdByUpper(1.5)

plane_1_map = vtkDataSetMapper()
plane_1_map.SetInputConnection(thresh_1.GetOutputPort())
plane_1_map.SetScalarRange(output.GetScalarRange())

plane_1_actor = vtkActor()
plane_1_actor.SetMapper(plane_1_map)
plane_1_actor.SetTexture(texture)
plane_1_actor.GetProperty().SetOpacity(0.999)

# Plane 2: threshold by lower
plane_2 = vtkStructuredGridGeometryFilter()
plane_2.SetInputData(output)
plane_2.SetExtent(30, 30, 0, 100, 0, 100)

thresh_2 = vtkThresholdTextureCoords()
thresh_2.SetInputConnection(plane_2.GetOutputPort())
thresh_2.ThresholdByLower(1.5)

plane_2_map = vtkDataSetMapper()
plane_2_map.SetInputConnection(thresh_2.GetOutputPort())
plane_2_map.SetScalarRange(output.GetScalarRange())

plane_2_actor = vtkActor()
plane_2_actor.SetMapper(plane_2_map)
plane_2_actor.SetTexture(texture)
plane_2_actor.GetProperty().SetOpacity(0.999)

# Plane 3: threshold between
plane_3 = vtkStructuredGridGeometryFilter()
plane_3.SetInputData(output)
plane_3.SetExtent(35, 35, 0, 100, 0, 100)

thresh_3 = vtkThresholdTextureCoords()
thresh_3.SetInputConnection(plane_3.GetOutputPort())
thresh_3.ThresholdBetween(1.5, 1.8)

plane_3_map = vtkDataSetMapper()
plane_3_map.SetInputConnection(thresh_3.GetOutputPort())
plane_3_map.SetScalarRange(output.GetScalarRange())

plane_3_actor = vtkActor()
plane_3_actor.SetMapper(plane_3_map)
plane_3_actor.SetTexture(texture)
plane_3_actor.GetProperty().SetOpacity(0.999)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(wall_actor)
renderer.AddActor(fin_actor)
renderer.AddActor(plane_1_actor)
renderer.AddActor(plane_2_actor)
renderer.AddActor(plane_3_actor)
renderer.SetBackground(1, 1, 1)


# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("texture threshold outline")

# Scene
camera = vtkCamera()
camera.SetClippingRange(1.51176, 75.5879)
camera.SetFocalPoint(2.33749, 2.96739, 3.61023)
camera.SetPosition(10.8787, 5.27346, 15.8687)
camera.SetViewAngle(30)
camera.SetViewUp(-0.0610856, 0.987798, -0.143262)
renderer.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
