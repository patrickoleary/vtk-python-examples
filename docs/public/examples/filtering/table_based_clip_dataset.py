#!/usr/bin/env python

# Demonstrate vtkTableBasedClipDataSet by reading an unstructured grid,
# clipping by one scalar array, then clipping the result by another,
# and rendering the doubly-clipped output.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersGeneral import vtkTableBasedClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read unstructured grid
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "can.vtu"))
reader.Update()

# First clip by ACCL scalar
clip_1 = vtkTableBasedClipDataSet()
clip_1.SetInputConnection(reader.GetOutputPort())
clip_1.SetValue(0)
clip_1.SetInputArrayToProcess(0, 0, 0, 0, "ACCL")

# Second clip by DISPL scalar
clip_2 = vtkTableBasedClipDataSet()
clip_2.SetInputConnection(clip_1.GetOutputPort())
clip_2.SetGenerateClipPointTypes(True)
clip_2.SetValue(0)
clip_2.SetInputArrayToProcess(0, 0, 0, 0, "DISPL")

# Extract surface for rendering
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(clip_2.GetOutputPort())

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("table based clip dataset")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
