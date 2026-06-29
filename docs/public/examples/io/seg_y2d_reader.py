#!/usr/bin/env python

# Read five 2D SEG-Y seismic lines and render with a diverging color map.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOSegY import vtkSegYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "SegY")

diverging_ctf = vtkColorTransferFunction()
diverging_ctf.AddRGBPoint(-6.4, 0.23, 0.30, 0.75)
diverging_ctf.AddRGBPoint(0.0, 0.86, 0.86, 0.86)
diverging_ctf.AddRGBPoint(6.6, 0.70, 0.02, 0.15)

line_a_reader = vtkSegYReader()
line_a_reader.SetFileName(os.path.join(data_dir, "lineA.sgy"))
line_a_reader.Update()

line_b_reader = vtkSegYReader()
line_b_reader.SetFileName(os.path.join(data_dir, "lineB.sgy"))
line_b_reader.Update()

line_c_reader = vtkSegYReader()
line_c_reader.SetFileName(os.path.join(data_dir, "lineC.sgy"))
line_c_reader.Update()

line_d_reader = vtkSegYReader()
line_d_reader.SetFileName(os.path.join(data_dir, "lineD.sgy"))
line_d_reader.Update()

line_e_reader = vtkSegYReader()
line_e_reader.SetFileName(os.path.join(data_dir, "lineE.sgy"))
line_e_reader.Update()

# Mapper / Actor - line A
line_a_mapper = vtkDataSetMapper()
line_a_mapper.SetInputConnection(line_a_reader.GetOutputPort())
line_a_mapper.SetLookupTable(diverging_ctf)
line_a_mapper.SetColorModeToMapScalars()

line_a_actor = vtkActor()
line_a_actor.SetMapper(line_a_mapper)

# Mapper / Actor - line B
line_b_mapper = vtkDataSetMapper()
line_b_mapper.SetInputConnection(line_b_reader.GetOutputPort())
line_b_mapper.SetLookupTable(diverging_ctf)
line_b_mapper.SetColorModeToMapScalars()

line_b_actor = vtkActor()
line_b_actor.SetMapper(line_b_mapper)

# Mapper / Actor - line C
line_c_mapper = vtkDataSetMapper()
line_c_mapper.SetInputConnection(line_c_reader.GetOutputPort())
line_c_mapper.SetLookupTable(diverging_ctf)
line_c_mapper.SetColorModeToMapScalars()

line_c_actor = vtkActor()
line_c_actor.SetMapper(line_c_mapper)

# Mapper / Actor - line D
line_d_mapper = vtkDataSetMapper()
line_d_mapper.SetInputConnection(line_d_reader.GetOutputPort())
line_d_mapper.SetLookupTable(diverging_ctf)
line_d_mapper.SetColorModeToMapScalars()

line_d_actor = vtkActor()
line_d_actor.SetMapper(line_d_mapper)

# Mapper / Actor - line E
line_e_mapper = vtkDataSetMapper()
line_e_mapper.SetInputConnection(line_e_reader.GetOutputPort())
line_e_mapper.SetLookupTable(diverging_ctf)
line_e_mapper.SetColorModeToMapScalars()

line_e_actor = vtkActor()
line_e_actor.SetMapper(line_e_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(line_a_actor)
renderer.AddActor(line_b_actor)
renderer.AddActor(line_c_actor)
renderer.AddActor(line_d_actor)
renderer.AddActor(line_e_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("seg y2d reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(50)
renderer.GetActiveCamera().Roll(50)
renderer.GetActiveCamera().Zoom(1.2)

interactor.Initialize()
interactor.Start()
