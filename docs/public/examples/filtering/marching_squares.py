#!/usr/bin/env python

# Generate marching squares iso-contours on three orthogonal slices
# of a CT head volume using vtkMarchingSquares.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMergePoints
from vtkmodules.vtkFiltersCore import vtkMarchingSquares
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load 16-bit CT head volume
reader = vtkVolume16Reader()
reader.SetDataDimensions(64, 64)
reader.GetOutput().SetOrigin(0.0, 0.0, 0.0)
reader.SetDataByteOrderToLittleEndian()
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetImageRange(1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.Update()

locator = vtkMergePoints()

# XY slice contours
iso_xy = vtkMarchingSquares()
iso_xy.SetInputConnection(reader.GetOutputPort())
iso_xy.GenerateValues(2, 600, 1200)
iso_xy.SetImageRange(0, 32, 32, 63, 45, 45)
iso_xy.SetLocator(locator)

iso_xy_mapper = vtkPolyDataMapper()
iso_xy_mapper.SetInputConnection(iso_xy.GetOutputPort())
iso_xy_mapper.SetScalarRange(600, 1200)

iso_xy_actor = vtkActor()
iso_xy_actor.SetMapper(iso_xy_mapper)

# YZ slice contours
iso_yz = vtkMarchingSquares()
iso_yz.SetInputConnection(reader.GetOutputPort())
iso_yz.GenerateValues(2, 600, 1200)
iso_yz.SetImageRange(32, 32, 32, 63, 46, 92)

iso_yz_mapper = vtkPolyDataMapper()
iso_yz_mapper.SetInputConnection(iso_yz.GetOutputPort())
iso_yz_mapper.SetScalarRange(600, 1200)

iso_yz_actor = vtkActor()
iso_yz_actor.SetMapper(iso_yz_mapper)

# XZ slice contours
iso_xz = vtkMarchingSquares()
iso_xz.SetInputConnection(reader.GetOutputPort())
iso_xz.GenerateValues(2, 600, 1200)
iso_xz.SetImageRange(0, 32, 32, 32, 0, 46)

iso_xz_mapper = vtkPolyDataMapper()
iso_xz_mapper.SetInputConnection(iso_xz.GetOutputPort())
iso_xz_mapper.SetScalarRange(600, 1200)

iso_xz_actor = vtkActor()
iso_xz_actor.SetMapper(iso_xz_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.VisibilityOff()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_xy_actor)
renderer.AddActor(iso_yz_actor)
renderer.AddActor(iso_xz_actor)
renderer.SetBackground(0.9, 0.9, 0.9)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("marching squares")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(324.368, 284.266, -19.3293)
camera.SetFocalPoint(73.5683, 120.903, 70.7309)
camera.SetViewAngle(30)
camera.SetViewUp(-0.304692, -0.0563843, -0.950781)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
