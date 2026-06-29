#!/usr/bin/env python

# Demonstrate vtkCompositePolyDataMapper with overlapping multiblock cells.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOXML import vtkXMLMultiBlockDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read overlapping multiblock data
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkXMLMultiBlockDataReader()
reader.SetFileName(os.path.join(data_dir, "overlap_faces.vtm"))
reader.Update()

# Mapper
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())
mapper.SelectColorArray("SpatioTemporalHarmonics")

actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("composite data overlapping cells")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
