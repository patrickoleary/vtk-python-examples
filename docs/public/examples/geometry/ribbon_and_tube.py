#!/usr/bin/env python

# Demonstrate vtkRibbonFilter and vtkTubeFilter by reading polyline data,
# applying ribbon and tube filters with texture coordinates, and rendering
# with a ruler texture side by side.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersModeling import vtkRibbonFilter
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read polyline data
reader = vtkPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "vtk.vtk"))

# Read ruler texture
png_reader = vtkPNGReader()
png_reader.SetFileName(os.path.join(data_dir, "ruler.png"))

texture = vtkTexture()
texture.SetInputConnection(png_reader.GetOutputPort())
texture.InterpolateOn()

# Ribbon filter
ribbon = vtkRibbonFilter()
ribbon.SetInputConnection(reader.GetOutputPort())
ribbon.SetWidth(0.1)
ribbon.SetGenerateTCoordsToUseLength()
ribbon.SetTextureLength(1.0)
ribbon.UseDefaultNormalOn()
ribbon.SetDefaultNormal(0, 0, 1)

ribbon_mapper = vtkPolyDataMapper()
ribbon_mapper.SetInputConnection(ribbon.GetOutputPort())

ribbon_actor = vtkActor()
ribbon_actor.SetMapper(ribbon_mapper)
ribbon_actor.GetProperty().SetColor(1, 1, 0)
ribbon_actor.SetTexture(texture)

# Tube filter
tuber = vtkTubeFilter()
tuber.SetInputConnection(reader.GetOutputPort())
tuber.SetRadius(0.1)
tuber.SetNumberOfSides(12)
tuber.SetGenerateTCoordsToUseLength()
tuber.SetTextureLength(0.5)
tuber.CappingOn()

tube_mapper = vtkPolyDataMapper()
tube_mapper.SetInputConnection(tuber.GetOutputPort())

tube_actor = vtkActor()
tube_actor.SetMapper(tube_mapper)
tube_actor.GetProperty().SetColor(1, 1, 0)
tube_actor.SetTexture(texture)
tube_actor.AddPosition(5, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ribbon_actor)
renderer.AddActor(tube_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(900, 350)
render_window.SetWindowName("ribbon and tube")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(4)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
