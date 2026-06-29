#!/usr/bin/env python

# Clean polydata with ghost cells, merging duplicate points while
# preserving correct scalar values over ghost boundaries.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkCleanPolyData
from vtkmodules.vtkIOXML import vtkXMLPPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load partitioned polydata with ghost cells
reader = vtkXMLPPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "ghostBrokenScalars.pvtp"))
reader.Update()

# Filter: clean polydata by merging coincident points
clean_poly_data = vtkCleanPolyData()
clean_poly_data.SetInputData(reader.GetOutput())
clean_poly_data.SetPointMerging(True)
clean_poly_data.Update()

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(clean_poly_data.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("clean polydata with ghost cells")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
