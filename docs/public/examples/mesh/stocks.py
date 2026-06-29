#!/usr/bin/env python

# Stock data visualization with closing price (top) and volume (bottom) views.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkFollower,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Colors (normalized RGB)
steel_blue = (0.275, 0.510, 0.706)
light_steel_blue = (0.690, 0.769, 0.871)

# Data files
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# --- Stock 0: GE (z=0.0) ---
ge_reader = vtkPolyDataReader()
ge_reader.SetFileName(str(data_dir / "GE.vtk"))
ge_reader.Update()

ge_text = vtkVectorText()
ge_text.SetText("GE")
ge_text.Update()

ge_num_points = ge_reader.GetOutput().GetNumberOfPoints()
ge_name_index = int((ge_num_points - 1) * 0.8)
ge_name_location = ge_reader.GetOutput().GetPoint(ge_name_index)
ge_label_x = ge_name_location[0] * 0.15
ge_label_y = ge_name_location[1] + 5.0

ge_tube = vtkTubeFilter()
ge_tube.SetInputConnection(ge_reader.GetOutputPort())
ge_tube.SetNumberOfSides(8)
ge_tube.SetRadius(0.5)
ge_tube.SetRadiusFactor(10000)

ge_transform = vtkTransform()
ge_transform.Translate(0, 0, 0.0)
ge_transform.Scale(0.15, 1, 1)

ge_transform_filter = vtkTransformPolyDataFilter()
ge_transform_filter.SetInputConnection(ge_tube.GetOutputPort())
ge_transform_filter.SetTransform(ge_transform)

ge_top_label_mapper = vtkPolyDataMapper()
ge_top_label_mapper.SetInputConnection(ge_text.GetOutputPort())

ge_top_label_actor = vtkFollower()
ge_top_label_actor.SetMapper(ge_top_label_mapper)
ge_top_label_actor.SetPosition(ge_label_x, ge_label_y, 0.0)
ge_top_label_actor.SetScale(2, 2, 2)
ge_top_label_actor.SetOrigin(ge_text.GetOutput().GetCenter())

ge_top_stock_mapper = vtkPolyDataMapper()
ge_top_stock_mapper.SetInputConnection(ge_transform_filter.GetOutputPort())
ge_top_stock_mapper.SetScalarRange(0, 8000)

ge_top_stock_actor = vtkActor()
ge_top_stock_actor.SetMapper(ge_top_stock_mapper)

ge_bottom_label_mapper = vtkPolyDataMapper()
ge_bottom_label_mapper.SetInputConnection(ge_text.GetOutputPort())

ge_bottom_label_actor = vtkFollower()
ge_bottom_label_actor.SetMapper(ge_bottom_label_mapper)
ge_bottom_label_actor.SetPosition(ge_label_x, ge_label_y, 0.0)
ge_bottom_label_actor.SetScale(2, 2, 2)
ge_bottom_label_actor.SetOrigin(ge_text.GetOutput().GetCenter())

ge_bottom_stock_mapper = vtkPolyDataMapper()
ge_bottom_stock_mapper.SetInputConnection(ge_transform_filter.GetOutputPort())
ge_bottom_stock_mapper.SetScalarRange(0, 8000)

ge_bottom_stock_actor = vtkActor()
ge_bottom_stock_actor.SetMapper(ge_bottom_stock_mapper)

# --- Stock 1: GM (z=8.0) ---
gm_reader = vtkPolyDataReader()
gm_reader.SetFileName(str(data_dir / "GM.vtk"))
gm_reader.Update()

gm_text = vtkVectorText()
gm_text.SetText("GM")
gm_text.Update()

gm_num_points = gm_reader.GetOutput().GetNumberOfPoints()
gm_name_index = int((gm_num_points - 1) * 0.8)
gm_name_location = gm_reader.GetOutput().GetPoint(gm_name_index)
gm_label_x = gm_name_location[0] * 0.15
gm_label_y = gm_name_location[1] + 5.0

gm_tube = vtkTubeFilter()
gm_tube.SetInputConnection(gm_reader.GetOutputPort())
gm_tube.SetNumberOfSides(8)
gm_tube.SetRadius(0.5)
gm_tube.SetRadiusFactor(10000)

gm_transform = vtkTransform()
gm_transform.Translate(0, 0, 8.0)
gm_transform.Scale(0.15, 1, 1)

gm_transform_filter = vtkTransformPolyDataFilter()
gm_transform_filter.SetInputConnection(gm_tube.GetOutputPort())
gm_transform_filter.SetTransform(gm_transform)

gm_top_label_mapper = vtkPolyDataMapper()
gm_top_label_mapper.SetInputConnection(gm_text.GetOutputPort())

gm_top_label_actor = vtkFollower()
gm_top_label_actor.SetMapper(gm_top_label_mapper)
gm_top_label_actor.SetPosition(gm_label_x, gm_label_y, 8.0)
gm_top_label_actor.SetScale(2, 2, 2)
gm_top_label_actor.SetOrigin(gm_text.GetOutput().GetCenter())

gm_top_stock_mapper = vtkPolyDataMapper()
gm_top_stock_mapper.SetInputConnection(gm_transform_filter.GetOutputPort())
gm_top_stock_mapper.SetScalarRange(0, 8000)

gm_top_stock_actor = vtkActor()
gm_top_stock_actor.SetMapper(gm_top_stock_mapper)

gm_bottom_label_mapper = vtkPolyDataMapper()
gm_bottom_label_mapper.SetInputConnection(gm_text.GetOutputPort())

gm_bottom_label_actor = vtkFollower()
gm_bottom_label_actor.SetMapper(gm_bottom_label_mapper)
gm_bottom_label_actor.SetPosition(gm_label_x, gm_label_y, 8.0)
gm_bottom_label_actor.SetScale(2, 2, 2)
gm_bottom_label_actor.SetOrigin(gm_text.GetOutput().GetCenter())

gm_bottom_stock_mapper = vtkPolyDataMapper()
gm_bottom_stock_mapper.SetInputConnection(gm_transform_filter.GetOutputPort())
gm_bottom_stock_mapper.SetScalarRange(0, 8000)

gm_bottom_stock_actor = vtkActor()
gm_bottom_stock_actor.SetMapper(gm_bottom_stock_mapper)

# --- Stock 2: IBM (z=16.0) ---
ibm_reader = vtkPolyDataReader()
ibm_reader.SetFileName(str(data_dir / "IBM.vtk"))
ibm_reader.Update()

ibm_text = vtkVectorText()
ibm_text.SetText("IBM")
ibm_text.Update()

ibm_num_points = ibm_reader.GetOutput().GetNumberOfPoints()
ibm_name_index = int((ibm_num_points - 1) * 0.8)
ibm_name_location = ibm_reader.GetOutput().GetPoint(ibm_name_index)
ibm_label_x = ibm_name_location[0] * 0.15
ibm_label_y = ibm_name_location[1] + 5.0

ibm_tube = vtkTubeFilter()
ibm_tube.SetInputConnection(ibm_reader.GetOutputPort())
ibm_tube.SetNumberOfSides(8)
ibm_tube.SetRadius(0.5)
ibm_tube.SetRadiusFactor(10000)

ibm_transform = vtkTransform()
ibm_transform.Translate(0, 0, 16.0)
ibm_transform.Scale(0.15, 1, 1)

ibm_transform_filter = vtkTransformPolyDataFilter()
ibm_transform_filter.SetInputConnection(ibm_tube.GetOutputPort())
ibm_transform_filter.SetTransform(ibm_transform)

ibm_top_label_mapper = vtkPolyDataMapper()
ibm_top_label_mapper.SetInputConnection(ibm_text.GetOutputPort())

ibm_top_label_actor = vtkFollower()
ibm_top_label_actor.SetMapper(ibm_top_label_mapper)
ibm_top_label_actor.SetPosition(ibm_label_x, ibm_label_y, 16.0)
ibm_top_label_actor.SetScale(2, 2, 2)
ibm_top_label_actor.SetOrigin(ibm_text.GetOutput().GetCenter())

ibm_top_stock_mapper = vtkPolyDataMapper()
ibm_top_stock_mapper.SetInputConnection(ibm_transform_filter.GetOutputPort())
ibm_top_stock_mapper.SetScalarRange(0, 8000)

ibm_top_stock_actor = vtkActor()
ibm_top_stock_actor.SetMapper(ibm_top_stock_mapper)

ibm_bottom_label_mapper = vtkPolyDataMapper()
ibm_bottom_label_mapper.SetInputConnection(ibm_text.GetOutputPort())

ibm_bottom_label_actor = vtkFollower()
ibm_bottom_label_actor.SetMapper(ibm_bottom_label_mapper)
ibm_bottom_label_actor.SetPosition(ibm_label_x, ibm_label_y, 16.0)
ibm_bottom_label_actor.SetScale(2, 2, 2)
ibm_bottom_label_actor.SetOrigin(ibm_text.GetOutput().GetCenter())

ibm_bottom_stock_mapper = vtkPolyDataMapper()
ibm_bottom_stock_mapper.SetInputConnection(ibm_transform_filter.GetOutputPort())
ibm_bottom_stock_mapper.SetScalarRange(0, 8000)

ibm_bottom_stock_actor = vtkActor()
ibm_bottom_stock_actor.SetMapper(ibm_bottom_stock_mapper)

# --- Stock 3: DEC (z=24.0) ---
dec_reader = vtkPolyDataReader()
dec_reader.SetFileName(str(data_dir / "DEC.vtk"))
dec_reader.Update()

dec_text = vtkVectorText()
dec_text.SetText("DEC")
dec_text.Update()

dec_num_points = dec_reader.GetOutput().GetNumberOfPoints()
dec_name_index = int((dec_num_points - 1) * 0.8)
dec_name_location = dec_reader.GetOutput().GetPoint(dec_name_index)
dec_label_x = dec_name_location[0] * 0.15
dec_label_y = dec_name_location[1] + 5.0

dec_tube = vtkTubeFilter()
dec_tube.SetInputConnection(dec_reader.GetOutputPort())
dec_tube.SetNumberOfSides(8)
dec_tube.SetRadius(0.5)
dec_tube.SetRadiusFactor(10000)

dec_transform = vtkTransform()
dec_transform.Translate(0, 0, 24.0)
dec_transform.Scale(0.15, 1, 1)

dec_transform_filter = vtkTransformPolyDataFilter()
dec_transform_filter.SetInputConnection(dec_tube.GetOutputPort())
dec_transform_filter.SetTransform(dec_transform)

dec_top_label_mapper = vtkPolyDataMapper()
dec_top_label_mapper.SetInputConnection(dec_text.GetOutputPort())

dec_top_label_actor = vtkFollower()
dec_top_label_actor.SetMapper(dec_top_label_mapper)
dec_top_label_actor.SetPosition(dec_label_x, dec_label_y, 24.0)
dec_top_label_actor.SetScale(2, 2, 2)
dec_top_label_actor.SetOrigin(dec_text.GetOutput().GetCenter())

dec_top_stock_mapper = vtkPolyDataMapper()
dec_top_stock_mapper.SetInputConnection(dec_transform_filter.GetOutputPort())
dec_top_stock_mapper.SetScalarRange(0, 8000)

dec_top_stock_actor = vtkActor()
dec_top_stock_actor.SetMapper(dec_top_stock_mapper)

dec_bottom_label_mapper = vtkPolyDataMapper()
dec_bottom_label_mapper.SetInputConnection(dec_text.GetOutputPort())

dec_bottom_label_actor = vtkFollower()
dec_bottom_label_actor.SetMapper(dec_bottom_label_mapper)
dec_bottom_label_actor.SetPosition(dec_label_x, dec_label_y, 24.0)
dec_bottom_label_actor.SetScale(2, 2, 2)
dec_bottom_label_actor.SetOrigin(dec_text.GetOutput().GetCenter())

dec_bottom_stock_mapper = vtkPolyDataMapper()
dec_bottom_stock_mapper.SetInputConnection(dec_transform_filter.GetOutputPort())
dec_bottom_stock_mapper.SetScalarRange(0, 8000)

dec_bottom_stock_actor = vtkActor()
dec_bottom_stock_actor.SetMapper(dec_bottom_stock_mapper)

# Renderer: top viewport shows closing price
top_renderer = vtkRenderer()
top_renderer.SetViewport(0.0, 0.4, 1.0, 1.0)
top_renderer.AddActor(ge_top_stock_actor)
top_renderer.AddActor(ge_top_label_actor)
top_renderer.AddActor(gm_top_stock_actor)
top_renderer.AddActor(gm_top_label_actor)
top_renderer.AddActor(ibm_top_stock_actor)
top_renderer.AddActor(ibm_top_label_actor)
top_renderer.AddActor(dec_top_stock_actor)
top_renderer.AddActor(dec_top_label_actor)
ge_top_label_actor.SetCamera(top_renderer.GetActiveCamera())
gm_top_label_actor.SetCamera(top_renderer.GetActiveCamera())
ibm_top_label_actor.SetCamera(top_renderer.GetActiveCamera())
dec_top_label_actor.SetCamera(top_renderer.GetActiveCamera())
top_renderer.SetBackground(steel_blue)

# Renderer: bottom viewport shows volume
bottom_renderer = vtkRenderer()
bottom_renderer.SetViewport(0.0, 0.0, 1.0, 0.4)
bottom_renderer.AddActor(ge_bottom_stock_actor)
bottom_renderer.AddActor(ge_bottom_label_actor)
bottom_renderer.AddActor(gm_bottom_stock_actor)
bottom_renderer.AddActor(gm_bottom_label_actor)
bottom_renderer.AddActor(ibm_bottom_stock_actor)
bottom_renderer.AddActor(ibm_bottom_label_actor)
bottom_renderer.AddActor(dec_bottom_stock_actor)
bottom_renderer.AddActor(dec_bottom_label_actor)
ge_bottom_label_actor.SetCamera(bottom_renderer.GetActiveCamera())
gm_bottom_label_actor.SetCamera(bottom_renderer.GetActiveCamera())
ibm_bottom_label_actor.SetCamera(bottom_renderer.GetActiveCamera())
dec_bottom_label_actor.SetCamera(bottom_renderer.GetActiveCamera())
bottom_renderer.SetBackground(light_steel_blue)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(top_renderer)
render_window.AddRenderer(bottom_renderer)
render_window.SetWindowName("stocks")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 800)

# Scene: configure cameras
top_renderer.GetActiveCamera().SetViewAngle(5.0)
top_renderer.ResetCamera()
top_renderer.GetActiveCamera().Zoom(1.4)
top_renderer.ResetCameraClippingRange()

bottom_renderer.GetActiveCamera().SetViewUp(0, 0, -1)
bottom_renderer.GetActiveCamera().SetPosition(0, 1, 0)
bottom_renderer.GetActiveCamera().SetViewAngle(5.0)
bottom_renderer.ResetCamera()
bottom_renderer.GetActiveCamera().Zoom(2.2)
bottom_renderer.ResetCameraClippingRange()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
