#!/usr/bin/env python

# Dice an STL model into pieces using vtkOBBDicer and display with
# an outline corner filter.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkOBBDicer
from vtkmodules.vtkFiltersSources import vtkOutlineCornerFilter
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read STL geometry
reader = vtkSTLReader()
reader.SetFileName(os.path.join(data_dir, "42400-IDGH.stl"))

# Dice into pieces
dicer = vtkOBBDicer()
dicer.SetInputConnection(reader.GetOutputPort())
dicer.SetNumberOfPointsPerPiece(1000)
dicer.Update()

iso_mapper = vtkDataSetMapper()
iso_mapper.SetInputConnection(dicer.GetOutputPort())
iso_mapper.SetScalarRange(0, dicer.GetNumberOfActualPieces())

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(0.7, 0.3, 0.3)

# Outline corners
outline = vtkOutlineCornerFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(0.5, 0.5, 0.6)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("dicer")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
