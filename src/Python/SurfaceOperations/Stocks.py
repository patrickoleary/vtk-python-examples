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
stock_files = [
    str(data_dir / "GE.vtk"),
    str(data_dir / "GM.vtk"),
    str(data_dir / "IBM.vtk"),
    str(data_dir / "DEC.vtk"),
]
stock_names = ["GE", "GM", "IBM", "DEC"]

# Renderer: top viewport shows closing price, bottom shows volume
top_renderer = vtkRenderer()
top_renderer.SetViewport(0.0, 0.4, 1.0, 1.0)
top_renderer.SetBackground(steel_blue)

bottom_renderer = vtkRenderer()
bottom_renderer.SetViewport(0.0, 0.0, 1.0, 0.4)
bottom_renderer.SetBackground(light_steel_blue)

renderers = [top_renderer, bottom_renderer]

z_position = 0.0
for stock_file, name in zip(stock_files, stock_names):
    # ---- Reader: load the stock polydata ----
    reader = vtkPolyDataReader()
    reader.SetFileName(stock_file)
    reader.Update()

    # ---- Source: text label for the stock name ----
    text_src = vtkVectorText()
    text_src.SetText(name)
    text_src.Update()

    num_points = reader.GetOutput().GetNumberOfPoints()
    name_index = int((num_points - 1) * 0.8)
    name_location = reader.GetOutput().GetPoint(name_index)
    label_x = name_location[0] * 0.15
    label_y = name_location[1] + 5.0
    label_z = z_position

    # ---- Filter: tube representation of the stock curve ----
    tube = vtkTubeFilter()
    tube.SetInputConnection(reader.GetOutputPort())
    tube.SetNumberOfSides(8)
    tube.SetRadius(0.5)
    tube.SetRadiusFactor(10000)

    # ---- Filter: transform to position in z and scale x ----
    transform = vtkTransform()
    transform.Translate(0, 0, z_position)
    transform.Scale(0.15, 1, 1)

    transform_filter = vtkTransformPolyDataFilter()
    transform_filter.SetInputConnection(tube.GetOutputPort())
    transform_filter.SetTransform(transform)

    for ren in renderers:
        label_mapper = vtkPolyDataMapper()
        label_mapper.SetInputConnection(text_src.GetOutputPort())

        label_actor = vtkFollower()
        label_actor.SetMapper(label_mapper)
        label_actor.SetPosition(label_x, label_y, label_z)
        label_actor.SetScale(2, 2, 2)
        label_actor.SetOrigin(text_src.GetOutput().GetCenter())

        stock_mapper = vtkPolyDataMapper()
        stock_mapper.SetInputConnection(transform_filter.GetOutputPort())
        stock_mapper.SetScalarRange(0, 8000)

        stock_actor = vtkActor()
        stock_actor.SetMapper(stock_mapper)

        ren.AddActor(stock_actor)
        ren.AddActor(label_actor)
        label_actor.SetCamera(ren.GetActiveCamera())

    z_position += 8.0

# Camera: configure top viewport (closing price view)
top_renderer.GetActiveCamera().SetViewAngle(5.0)
top_renderer.ResetCamera()
top_renderer.GetActiveCamera().Zoom(1.4)
top_renderer.ResetCameraClippingRange()

# Camera: configure bottom viewport (volume view from above)
bottom_renderer.GetActiveCamera().SetViewUp(0, 0, -1)
bottom_renderer.GetActiveCamera().SetPosition(0, 1, 0)
bottom_renderer.GetActiveCamera().SetViewAngle(5.0)
bottom_renderer.ResetCamera()
bottom_renderer.GetActiveCamera().Zoom(2.2)
bottom_renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(top_renderer)
render_window.AddRenderer(bottom_renderer)
render_window.SetWindowName("Stocks")
render_window.SetSize(500, 800)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
